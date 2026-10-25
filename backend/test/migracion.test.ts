// Prueba end-to-end de scripts/migrar-datos-supabase.ts contra dos bases
// de Postgres de verdad: una que imita el esquema minimo de Supabase
// (auth.users + auth.identities + las tablas propias) como "origen", y
// otra con nuestro backend/src/schema.sql real como "destino". Se salta
// si no hay DATABASE_URL (mismo criterio que test/integration.test.ts).
//
// Esto prueba la LOGICA del script (orden de FK, conservacion de UUID,
// idempotencia) con datos de prueba -- NO reemplaza la verificacion
// manual contra la Supabase real de produccion que el propio script pide
// antes de --apply (el supuesto sobre auth.identities.identity_data no
// se puede verificar aqui, solo con datos reales).
import test from "node:test";
import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import pg from "pg";

const run = promisify(execFile);
const tieneDb = Boolean(process.env.DATABASE_URL);

test("migrar-datos-supabase.ts: dry-run cuenta sin escribir, --apply conserva UUID y es idempotente", { skip: !tieneDb }, async (t) => {
  const baseUrl = new URL(process.env.DATABASE_URL!);
  const admin = new pg.Pool({ connectionString: process.env.DATABASE_URL });

  const nombreOrigen = "ai_sdlc_migracion_test_origen";
  const nombreDestino = "ai_sdlc_migracion_test_destino";

  await admin.query(`drop database if exists ${nombreOrigen}`);
  await admin.query(`drop database if exists ${nombreDestino}`);
  await admin.query(`create database ${nombreOrigen}`);
  await admin.query(`create database ${nombreDestino}`);
  await admin.end();

  const urlOrigen = new URL(baseUrl.toString());
  urlOrigen.pathname = `/${nombreOrigen}`;
  const urlDestino = new URL(baseUrl.toString());
  urlDestino.pathname = `/${nombreDestino}`;

  const origen = new pg.Pool({ connectionString: urlOrigen.toString() });
  const destino = new pg.Pool({ connectionString: urlDestino.toString() });

  t.after(async () => {
    await origen.end().catch(() => {});
    await destino.end().catch(() => {});
    const admin2 = new pg.Pool({ connectionString: process.env.DATABASE_URL });
    await admin2.query(`drop database if exists ${nombreOrigen}`);
    await admin2.query(`drop database if exists ${nombreDestino}`);
    await admin2.end();
  });

  // Imita el esquema minimo de Supabase que el script lee.
  await origen.query(`
    create schema auth;
    create table auth.users (id uuid primary key, email text, created_at timestamptz not null default now());
    create table auth.identities (user_id uuid references auth.users(id), provider text, provider_id text, identity_data jsonb);
    create table projects (id uuid primary key, user_id uuid, name text, is_default boolean, vars jsonb, updated_at timestamptz);
    create table project_prompt_state (project_id uuid, prompt_id text, used_at timestamptz, custom_additions text, ai_output text, updated_at timestamptz);
    create table user_trial (user_id uuid, trial_started_at timestamptz, trial_expires_at timestamptz, renewed_count int);
    create table feedback (id uuid primary key, user_id uuid, rating int, comments text, created_at timestamptz);
    create table subscriptions (user_id uuid, paddle_subscription_id text, paddle_customer_id text, status text, current_period_end timestamptz, last_event_occurred_at timestamptz, created_at timestamptz, updated_at timestamptz);
    create table paddle_webhook_events (event_id text primary key, event_type text, occurred_at timestamptz, received_at timestamptz, processed_at timestamptz);
    create table prompt_copy_stats (prompt_id text primary key, copy_count int, updated_at timestamptz);
  `);

  const userId = "11111111-1111-1111-1111-111111111111";
  await origen.query(`insert into auth.users (id, email) values ($1, 'test@example.com')`, [userId]);
  await origen.query(
    `insert into auth.identities (user_id, provider, provider_id, identity_data)
     values ($1, 'github', '999999', '{"user_name": "usuario-de-prueba"}'::jsonb)`,
    [userId],
  );
  const projectId = "22222222-2222-2222-2222-222222222222";
  await origen.query(
    `insert into projects (id, user_id, name, is_default, vars, updated_at) values ($1, $2, 'Proyecto migrado', true, '{}'::jsonb, now())`,
    [projectId, userId],
  );
  await origen.query(
    `insert into subscriptions (user_id, paddle_subscription_id, paddle_customer_id, status, current_period_end, created_at, updated_at)
     values ($1, 'sub_real_123', 'ctm_real_123', 'active', now() + interval '1 month', now(), now())`,
    [userId],
  );

  // Esquema real del destino.
  const here = path.dirname(fileURLToPath(import.meta.url));
  const schemaSql = readFileSync(path.join(here, "..", "src", "schema.sql"), "utf8");
  await destino.query(schemaSql);

  const scriptPath = path.join(here, "..", "scripts", "migrar-datos-supabase.ts");
  const env = {
    ...process.env,
    SUPABASE_DATABASE_URL: urlOrigen.toString(),
    DATABASE_URL: urlDestino.toString(),
  };

  await t.test("dry-run no escribe nada en el destino", async () => {
    const { stdout } = await run(
      process.execPath,
      ["--experimental-strip-types", "--no-warnings", scriptPath],
      { env },
    );
    assert.match(stdout, /dry-run/);
    const { rows } = await destino.query("select count(*)::int as n from users");
    assert.equal(rows[0]!.n, 0);
  });

  await t.test("--apply conserva el mismo UUID de usuario y de proyecto", async () => {
    await run(process.execPath, ["--experimental-strip-types", "--no-warnings", scriptPath, "--apply"], { env });

    const { rows: usuarios } = await destino.query("select id, github_id, github_login from users");
    assert.equal(usuarios.length, 1);
    assert.equal(usuarios[0]!.id, userId);
    assert.equal(usuarios[0]!.github_id, "999999");
    assert.equal(usuarios[0]!.github_login, "usuario-de-prueba");

    const { rows: proyectos } = await destino.query("select id, user_id from projects");
    assert.equal(proyectos.length, 1);
    assert.equal(proyectos[0]!.id, projectId);

    const { rows: subs } = await destino.query("select paddle_subscription_id from subscriptions where user_id = $1", [userId]);
    assert.equal(subs[0]!.paddle_subscription_id, "sub_real_123");
  });

  await t.test("--apply es idempotente: re-correrlo no duplica ni falla", async () => {
    await run(process.execPath, ["--experimental-strip-types", "--no-warnings", scriptPath, "--apply"], { env });
    const { rows } = await destino.query("select count(*)::int as n from users");
    assert.equal(rows[0]!.n, 1);
  });

  await t.test("sin --sincronizar, un cambio posterior en el origen NO pisa el destino", async () => {
    await origen.query(`update projects set name = 'Renombrado en Supabase', updated_at = now() + interval '1 minute' where id = $1`, [projectId]);
    await run(process.execPath, ["--experimental-strip-types", "--no-warnings", scriptPath, "--apply"], { env });
    const { rows } = await destino.query("select name from projects where id = $1", [projectId]);
    assert.equal(rows[0]!.name, "Proyecto migrado");
  });

  await t.test("--sincronizar actualiza solo si el origen es mas reciente, y el contador toma el mayor", async () => {
    await origen.query(`insert into prompt_copy_stats values ('p-1', 7, now())`);
    await destino.query(`insert into prompt_copy_stats values ('p-1', 9, now()) on conflict (prompt_id) do update set copy_count = 9`);
    await run(process.execPath, ["--experimental-strip-types", "--no-warnings", scriptPath, "--apply", "--fase2", "--sincronizar"], { env });
    const { rows } = await destino.query("select name from projects where id = $1", [projectId]);
    assert.equal(rows[0]!.name, "Renombrado en Supabase");
    const { rows: stats } = await destino.query("select copy_count from prompt_copy_stats where prompt_id = 'p-1'");
    assert.equal(stats[0]!.copy_count, 9, "el destino ya tenia mas copias: no se baja");

    // Un cambio local mas reciente en el destino no lo pisa el origen.
    await destino.query(`update projects set name = 'Editado ya en el backend', updated_at = now() + interval '1 hour' where id = $1`, [projectId]);
    await run(process.execPath, ["--experimental-strip-types", "--no-warnings", scriptPath, "--apply", "--fase2", "--sincronizar"], { env });
    const { rows: r2 } = await destino.query("select name from projects where id = $1", [projectId]);
    assert.equal(r2[0]!.name, "Editado ya en el backend");
  });

  await t.test("--fase2 no copia prueba, feedback ni pagos", async () => {
    const segundo = "55555555-5555-5555-5555-555555555555";
    await origen.query(`insert into auth.users (id, email) values ($1, 'b@example.com')`, [segundo]);
    await origen.query(`insert into auth.identities values ($1, 'github', '888888', '{"user_name": "segunda"}'::jsonb)`, [segundo]);
    await origen.query(
      `insert into subscriptions (user_id, paddle_subscription_id, status, created_at, updated_at) values ($1, 'sub_fase2', 'active', now(), now())`,
      [segundo],
    );
    const { stdout } = await run(process.execPath, ["--experimental-strip-types", "--no-warnings", scriptPath, "--apply", "--fase2"], { env });
    assert.match(stdout, /Fase 2/);
    assert.doesNotMatch(stdout, /subscriptions/);
    const { rows } = await destino.query("select count(*)::int as n from subscriptions where user_id = $1", [segundo]);
    assert.equal(rows[0]!.n, 0);
    const { rows: u } = await destino.query("select count(*)::int as n from users where id = $1", [segundo]);
    assert.equal(u[0]!.n, 1);
  });

  await t.test("una fila huerfana se omite con aviso y no aborta la migracion", async () => {
    await origen.query(
      `insert into projects (id, user_id, name, is_default, vars, updated_at) values ('66666666-6666-6666-6666-666666666666', '77777777-7777-7777-7777-777777777777', 'Huerfano', false, '{}'::jsonb, now())`,
    );
    const { stdout, stderr } = await run(process.execPath, ["--experimental-strip-types", "--no-warnings", scriptPath, "--apply", "--fase2"], { env });
    assert.match(stderr, /fila omitida/);
    assert.match(stdout, /omitidas/);
    const { rows } = await destino.query("select count(*)::int as n from projects where name = 'Huerfano'");
    assert.equal(rows[0]!.n, 0);
  });
});
