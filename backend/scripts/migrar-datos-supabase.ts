// Migra los datos reales de Supabase hacia el Postgres propio de este
// backend -- Fase 3 (la de mayor riesgo) de
// docs/PLAN_MIGRACION_SUPABASE_A_LOCAL.md §4. NO SE HA EJECUTADO TODAVIA
// contra datos reales: este script se escribio y se probo con datos de
// PRUEBA (ver test/migracion.test.ts), no contra la instancia real de
// Supabase de produccion -- quien lo corra por primera vez contra datos
// reales debe seguir el checklist de verificacion de la seccion "ANTES DE
// CORRER CONTRA PRODUCCION" mas abajo.
//
// Critico (ver plan §4.1): conserva los MISMOS UUID de usuario que ya
// tiene Supabase. Paddle ya guarda ese UUID en custom_data.user_id para
// cada suscripcion activa -- si aqui se generaran UUID nuevos, los
// webhooks futuros de renovacion de clientes que YA PAGAN dejarian de
// encontrar a su usuario (el mismo caso de falla que
// apply_paddle_subscription_event ya detecta y por el que responde 500
// a proposito, ver supabase/subscriptions.sql lineas 120-148).
//
// SUPUESTO SIN VERIFICAR contra la instancia real de Supabase (marcar
// como verificado o corregir antes de usar con --apply): la identidad de
// GitHub de cada usuario vive en `auth.identities` (provider='github'),
// con `provider_id` = id numerico de GitHub (como string) y
// `identity_data->>'user_name'` = login de GitHub. Esta es la forma
// estandar en que GoTrue guarda el perfil de un proveedor OAuth, pero
// nunca se confirmo leyendo una fila real -- antes de --apply, correr la
// consulta de verificacion de la seccion siguiente y comparar contra un
// usuario real conocido.
//
// Idempotente a proposito (se puede re-correr sin duplicar ni fallar si
// se interrumpe a medias): cada insert usa `on conflict (...) do
// nothing`, nunca sobreescribe una fila que ya exista en el destino.
//
// Uso:
//   SUPABASE_DATABASE_URL=postgres://...  DATABASE_URL=postgres://... \
//     node --experimental-strip-types --no-warnings scripts/migrar-datos-supabase.ts
//   (agregar --apply para escribir de verdad; sin esa bandera, solo
//   cuenta filas en el origen y simula, sin tocar el destino)
//
// Banderas de la Fase 2 (login todavia en Supabase, solo datos sin dinero):
//   --fase2       copia solo users, projects, project_prompt_state y
//                 prompt_copy_stats. La prueba, el feedback y los pagos
//                 siguen viviendo en Supabase hasta la Fase 3: copiarlos
//                 ahora dejaria en el destino una foto que se desfasa con
//                 cada webhook.
//   --sincronizar en vez de "do nothing", actualiza las filas que ya
//                 existen cuando el origen es mas reciente (updated_at); en
//                 los contadores de copias gana el mayor. Sirve para
//                 re-correrlo despues del corte, mientras queden paginas
//                 viejas abiertas escribiendo en Supabase. No propaga
//                 borrados: un proyecto borrado en Supabase tras la carga
//                 inicial sigue en el destino.

import pg from "pg";

const APLICAR = process.argv.includes("--apply");
const FASE2 = process.argv.includes("--fase2");
const SINCRONIZAR = process.argv.includes("--sincronizar");

function requerida(nombre: string): string {
  const valor = process.env[nombre];
  if (!valor) {
    console.error(`Falta la variable de entorno ${nombre}`);
    process.exit(1);
  }
  return valor;
}

const origen = new pg.Pool({ connectionString: requerida("SUPABASE_DATABASE_URL") });
const destino = new pg.Pool({ connectionString: requerida("DATABASE_URL") });

interface ResumenTabla {
  tabla: string;
  filasOrigen: number;
  // Con --sincronizar incluye las filas actualizadas, no solo las nuevas.
  filasInsertadas: number;
  omitidas?: number;
}

const resumen: ResumenTabla[] = [];

async function migrarUsers(): Promise<Map<string, string>> {
  // ANTES DE --apply: correr esto a mano contra Supabase y comparar con
  // un usuario real conocido (su login de GitHub real) para confirmar
  // que `provider_id` e `identity_data->>'user_name'` son lo que se
  // espera:
  //
  //   select u.id, i.provider_id, i.identity_data->>'user_name' as login
  //   from auth.users u join auth.identities i
  //     on i.user_id = u.id and i.provider = 'github'
  //   limit 5;
  const { rows } = await origen.query<{
    id: string;
    github_id: string;
    github_login: string;
    email: string | null;
    created_at: string;
  }>(
    `select u.id, i.provider_id as github_id, i.identity_data->>'user_name' as github_login,
            u.email, u.created_at
     from auth.users u
     join auth.identities i on i.user_id = u.id and i.provider = 'github'`,
  );

  let insertadas = 0;
  for (const row of rows) {
    if (!row.github_id || !row.github_login) {
      console.warn(`usuario ${row.id} sin provider_id/login de GitHub -- se omite, revisar a mano`);
      continue;
    }
    if (APLICAR) {
      const { rowCount } = await destino.query(
        `insert into users (id, github_id, github_login, email, created_at)
         values ($1, $2, $3, $4, $5)
         on conflict (id) do ${SINCRONIZAR
           ? "update set github_login = excluded.github_login, email = excluded.email where (users.github_login, users.email) is distinct from (excluded.github_login, excluded.email)"
           : "nothing"}`,
        [row.id, row.github_id, row.github_login, row.email, row.created_at],
      );
      insertadas += rowCount ?? 0;
    }
  }
  resumen.push({ tabla: "users", filasOrigen: rows.length, filasInsertadas: insertadas });

  return new Map(rows.map((r) => [r.id, r.id]));
}

// `alActualizar`: la clausula `do update ...` que se usa con --sincronizar.
// Sin ella (o sin la bandera) el conflicto se resuelve con `do nothing`.
async function copiarTabla(
  tabla: string,
  columnas: string[],
  conflictoPor: string,
  alActualizar?: string,
): Promise<void> {
  const { rows } = await origen.query(`select ${columnas.join(", ")} from ${tabla}`);
  const resolucion = SINCRONIZAR && alActualizar ? alActualizar : "do nothing";

  let insertadas = 0;
  let omitidas = 0;
  if (APLICAR) {
    for (const row of rows) {
      const valores = columnas.map((c) => row[c]);
      const marcadores = columnas.map((_, i) => `$${i + 1}`);
      try {
        const { rowCount } = await destino.query(
          `insert into ${tabla} (${columnas.join(", ")})
           values (${marcadores.join(", ")})
           on conflict (${conflictoPor}) ${resolucion}`,
          valores,
        );
        insertadas += rowCount ?? 0;
      } catch (error) {
        // 23503: la fila apunta a un usuario o proyecto que no se migro (por
        // ejemplo, un usuario sin identidad de GitHub, que migrarUsers omite).
        // Se avisa y se sigue: una fila huerfana no debe abortar el resto.
        if ((error as { code?: string }).code === "23503") {
          omitidas += 1;
          console.warn(`${tabla}: fila omitida por referencia inexistente (${columnas[0]}=${String(row[columnas[0]!])})`);
          continue;
        }
        throw error;
      }
    }
  }
  resumen.push({ tabla, filasOrigen: rows.length, filasInsertadas: insertadas, ...(omitidas ? { omitidas } : {}) });
}

async function main() {
  console.log(APLICAR ? "Modo: APLICANDO cambios de verdad." : "Modo: solo lectura (dry-run). Pasa --apply para escribir.");
  if (FASE2) console.log("Alcance: Fase 2 (users, projects, project_prompt_state, prompt_copy_stats).");
  if (SINCRONIZAR) console.log("Conflictos: se actualizan las filas cuyo origen es mas reciente.");

  // Orden por dependencia de foreign key: users primero, luego lo que
  // depende de ella, projects antes de project_prompt_state.
  await migrarUsers();
  await copiarTabla(
    "projects",
    ["id", "user_id", "name", "is_default", "vars", "updated_at"],
    "id",
    `do update set name = excluded.name, is_default = excluded.is_default, vars = excluded.vars,
       updated_at = excluded.updated_at
     where projects.user_id = excluded.user_id and projects.updated_at < excluded.updated_at`,
  );
  await copiarTabla(
    "project_prompt_state",
    ["project_id", "prompt_id", "used_at", "custom_additions", "ai_output", "updated_at"],
    "project_id, prompt_id",
    `do update set used_at = excluded.used_at, custom_additions = excluded.custom_additions,
       ai_output = excluded.ai_output, updated_at = excluded.updated_at
     where project_prompt_state.updated_at < excluded.updated_at`,
  );
  await copiarTabla(
    "prompt_copy_stats",
    ["prompt_id", "copy_count", "updated_at"],
    "prompt_id",
    `do update set copy_count = greatest(prompt_copy_stats.copy_count, excluded.copy_count),
       updated_at = greatest(prompt_copy_stats.updated_at, excluded.updated_at)
     where prompt_copy_stats.copy_count < excluded.copy_count`,
  );
  if (FASE2) {
    await cerrar();
    return;
  }
  await copiarTabla(
    "user_trial",
    ["user_id", "trial_started_at", "trial_expires_at", "renewed_count"],
    "user_id",
  );
  await copiarTabla("feedback", ["id", "user_id", "rating", "comments", "created_at"], "id");
  await copiarTabla(
    "subscriptions",
    [
      "user_id",
      "paddle_subscription_id",
      "paddle_customer_id",
      "status",
      "current_period_end",
      "last_event_occurred_at",
      "created_at",
      "updated_at",
    ],
    "user_id",
  );
  await copiarTabla(
    "paddle_webhook_events",
    ["event_id", "event_type", "occurred_at", "received_at", "processed_at"],
    "event_id",
  );
  await cerrar();
}

async function cerrar(): Promise<void> {
  console.log("\nResumen:");
  console.table(resumen);

  if (!APLICAR) {
    console.log("\nEsto fue un dry-run -- no se escribio nada en el destino. Revisa los conteos y corre de nuevo con --apply.");
  } else if (!FASE2) {
    console.log("\nVerifica manualmente: toma 3-5 usuarios con subscriptions.status='active' en el destino y confirma que su paddle_subscription_id coincide con el de Supabase (ver plan §4.2 paso 5).");
  }

  await origen.end();
  await destino.end();
}

main().catch((error) => {
  console.error("La migracion fallo:", error);
  process.exitCode = 1;
});
