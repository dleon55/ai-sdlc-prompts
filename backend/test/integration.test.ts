// Pruebas de integracion contra un Postgres real (DATABASE_URL). Se
// saltan automaticamente si la variable no esta configurada -- no hay
// todavia un servicio de Postgres en CI (eso es un cambio de
// .github/workflows/deploy.yml para una fase posterior, ver
// docs/PLAN_MIGRACION_SUPABASE_A_LOCAL.md §5); localmente, con
// backend/docker-compose.yml levantado (o el Postgres nativo de
// desarrollo), SI corren y ejercitan el esquema real.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const tieneDb = Boolean(process.env.DATABASE_URL);

test("esquema + checkTrialStatus + aislamiento por usuario", { skip: !tieneDb }, async (t) => {
  const { pool } = await import("../src/db.ts");
  const { checkTrialStatus } = await import("../src/routes/trial.ts");

  const here = path.dirname(fileURLToPath(import.meta.url));
  const schemaSql = readFileSync(path.join(here, "..", "src", "schema.sql"), "utf8");
  await pool.query(schemaSql);

  await t.test("checkTrialStatus autocrea la fila de prueba si no existe", async () => {
    const { rows } = await pool.query<{ id: string }>(
      `insert into users (github_id, github_login) values ($1, 'test-integration-1')
       on conflict (github_id) do update set github_login = excluded.github_login
       returning id`,
      ["test-integration-user-1"],
    );
    const userId = rows[0]!.id;

    const status = await checkTrialStatus(userId);
    assert.equal(status.active, true);
    assert.equal(status.subscribed, false);
    assert.ok(status.expires_at);

    const { rows: trialRows } = await pool.query("select 1 from user_trial where user_id = $1", [userId]);
    assert.equal(trialRows.length, 1);
  });

  await t.test("checkTrialStatus reporta subscribed cuando hay suscripcion activa", async () => {
    const { rows } = await pool.query<{ id: string }>(
      `insert into users (github_id, github_login) values ($1, 'test-integration-2')
       on conflict (github_id) do update set github_login = excluded.github_login
       returning id`,
      ["test-integration-user-2"],
    );
    const userId = rows[0]!.id;

    await pool.query(
      `insert into subscriptions (user_id, paddle_subscription_id, paddle_customer_id, status, current_period_end)
       values ($1, 'sub_integration_1', 'ctm_integration_1', 'active', now() + interval '1 month')`,
      [userId],
    );

    const status = await checkTrialStatus(userId);
    assert.equal(status.active, true);
    assert.equal(status.subscribed, true);
  });

  await t.test("apply_paddle_subscription_event es idempotente por event_id", async () => {
    const { rows } = await pool.query<{ id: string }>(
      `insert into users (github_id, github_login) values ($1, 'test-integration-3')
       on conflict (github_id) do update set github_login = excluded.github_login
       returning id`,
      ["test-integration-user-3"],
    );
    const userId = rows[0]!.id;

    const args = [
      "evt_integration_1",
      "subscription.created",
      new Date().toISOString(),
      userId,
      "sub_integration_2",
      "ctm_integration_2",
      "active",
      new Date(Date.now() + 2592000000).toISOString(),
    ];
    const first = await pool.query("select apply_paddle_subscription_event($1,$2,$3,$4,$5,$6,$7,$8) as applied", args);
    const second = await pool.query("select apply_paddle_subscription_event($1,$2,$3,$4,$5,$6,$7,$8) as applied", args);
    assert.equal(first.rows[0].applied, true);
    assert.equal(second.rows[0].applied, false);
  });

  await pool.end();
});
