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

import pg from "pg";

const APLICAR = process.argv.includes("--apply");

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
  filasInsertadas: number;
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
         on conflict (id) do nothing`,
        [row.id, row.github_id, row.github_login, row.email, row.created_at],
      );
      insertadas += rowCount ?? 0;
    }
  }
  resumen.push({ tabla: "users", filasOrigen: rows.length, filasInsertadas: insertadas });

  return new Map(rows.map((r) => [r.id, r.id]));
}

async function copiarTabla(
  tabla: string,
  columnas: string[],
  conflictoPor: string,
): Promise<void> {
  const { rows } = await origen.query(`select ${columnas.join(", ")} from ${tabla}`);

  let insertadas = 0;
  if (APLICAR) {
    for (const row of rows) {
      const valores = columnas.map((c) => row[c]);
      const marcadores = columnas.map((_, i) => `$${i + 1}`);
      const { rowCount } = await destino.query(
        `insert into ${tabla} (${columnas.join(", ")})
         values (${marcadores.join(", ")})
         on conflict (${conflictoPor}) do nothing`,
        valores,
      );
      insertadas += rowCount ?? 0;
    }
  }
  resumen.push({ tabla, filasOrigen: rows.length, filasInsertadas: insertadas });
}

async function main() {
  console.log(APLICAR ? "Modo: APLICANDO cambios de verdad." : "Modo: solo lectura (dry-run). Pasa --apply para escribir.");

  // Orden por dependencia de foreign key: users primero, luego lo que
  // depende de ella, projects antes de project_prompt_state.
  await migrarUsers();
  await copiarTabla("projects", ["id", "user_id", "name", "is_default", "vars", "updated_at"], "id");
  await copiarTabla(
    "project_prompt_state",
    ["project_id", "prompt_id", "used_at", "custom_additions", "ai_output", "updated_at"],
    "project_id, prompt_id",
  );
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
  await copiarTabla("prompt_copy_stats", ["prompt_id", "copy_count", "updated_at"], "prompt_id");

  console.log("\nResumen:");
  console.table(resumen);

  if (!APLICAR) {
    console.log("\nEsto fue un dry-run -- no se escribio nada en el destino. Revisa los conteos y corre de nuevo con --apply.");
  } else {
    console.log("\nVerifica manualmente: toma 3-5 usuarios con subscriptions.status='active' en el destino y confirma que su paddle_subscription_id coincide con el de Supabase (ver plan §4.2 paso 5).");
  }

  await origen.end();
  await destino.end();
}

main().catch((error) => {
  console.error("La migracion fallo:", error);
  process.exitCode = 1;
});
