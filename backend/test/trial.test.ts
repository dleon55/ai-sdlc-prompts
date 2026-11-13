// Tope de renovaciones de la prueba Pro (spec E1, 13-nov-2026).
// Las de configuracion son logica pura y corren siempre; las de la regla
// usan un Postgres real (DATABASE_URL), como integration.test.ts, y se
// saltan sin el.
import test from "node:test";
import assert from "node:assert/strict";
import {
  parseGraceUntil,
  parseMaxRenewals,
  renewalsLeft,
  trialPolicyFromEnv,
} from "../src/routes/trial.ts";

const tieneDb = Boolean(process.env.DATABASE_URL);

test("TRIAL_MAX_RENEWALS: 1 por omision, entero >= 0, invalido cae al valor por omision", () => {
  assert.equal(parseMaxRenewals(undefined), 1);
  assert.equal(parseMaxRenewals(""), 1);
  assert.equal(parseMaxRenewals("0"), 0);
  assert.equal(parseMaxRenewals(" 3 "), 3);
  assert.equal(parseMaxRenewals("-1"), 1);
  assert.equal(parseMaxRenewals("dos"), 1);
});

test("TRIAL_GRACE_UNTIL: 30-nov-2026 fin del dia en Mexico por omision; vacio/off la desactiva", () => {
  assert.equal(parseGraceUntil(undefined)!.toISOString(), "2026-12-01T05:59:59.999Z");
  assert.equal(parseGraceUntil("2026-12-15")!.toISOString(), "2026-12-16T05:59:59.999Z");
  assert.equal(parseGraceUntil(""), null);
  assert.equal(parseGraceUntil("off"), null);
  assert.equal(parseGraceUntil("basura")!.toISOString(), "2026-12-01T05:59:59.999Z");
  const p = trialPolicyFromEnv({});
  assert.equal(p.maxRenewals, 1);
  assert.ok(p.graceUntil);
});

test("renewalsLeft: base + cortesia mientras no venza la fecha y no se haya usado", () => {
  const sinCortesia = { maxRenewals: 1, graceUntil: null };
  assert.equal(renewalsLeft(0, false, sinCortesia), 1);
  assert.equal(renewalsLeft(1, false, sinCortesia), 0);
  assert.equal(renewalsLeft(9, false, sinCortesia), 0);
  const conCortesia = { maxRenewals: 1, graceUntil: new Date("2026-12-01T05:59:59.999Z") };
  const antes = new Date("2026-11-20T12:00:00Z");
  const despues = new Date("2026-12-02T00:00:00Z");
  assert.equal(renewalsLeft(9, false, conCortesia, antes), 1);
  assert.equal(renewalsLeft(9, true, conCortesia, antes), 0);
  assert.equal(renewalsLeft(9, false, conCortesia, despues), 0);
  assert.equal(renewalsLeft(0, false, conCortesia, antes), 2);
});

test("POST /feedback: tope, ventana de 48 h, suscripcion, cortesia y concurrencia", { skip: !tieneDb }, async (t) => {
  const { pool } = await import("../src/db.ts");
  const { renewTrialWithFeedback, checkTrialStatus } = await import("../src/routes/trial.ts");
  const { aplicarEsquema } = await import("./esquema.ts");
  await aplicarEsquema(pool);

  const sinCortesia = { maxRenewals: 1, graceUntil: null };
  const conCortesia = { maxRenewals: 1, graceUntil: new Date(Date.now() + 7 * 86400000) };
  const cortesiaVencida = { maxRenewals: 1, graceUntil: new Date(Date.now() - 86400000) };

  const prefijo = "test-trial-tope-";
  await pool.query("delete from users where github_id like $1", [`${prefijo}%`]);

  let n = 0;
  async function usuario(): Promise<string> {
    n += 1;
    const { rows } = await pool.query<{ id: string }>(
      "insert into users (github_id, github_login) values ($1, $1) returning id",
      [`${prefijo}${n}`],
    );
    return rows[0]!.id;
  }
  async function vencer(userId: string) {
    await pool.query("update user_trial set trial_expires_at = now() - interval '1 day' where user_id = $1", [userId]);
  }
  async function feedbacks(userId: string): Promise<number> {
    const { rows } = await pool.query<{ n: string }>("select count(*) as n from feedback where user_id = $1", [userId]);
    return Number(rows[0]!.n);
  }
  async function prueba(userId: string) {
    const { rows } = await pool.query<{ renewed_count: number; vence: string }>(
      "select renewed_count, trial_expires_at as vence from user_trial where user_id = $1",
      [userId],
    );
    return rows[0]!;
  }

  await t.test("usuario nuevo: 7 dias + 1 renovacion; la siguiente es 409 renewal_limit", async () => {
    const u = await usuario();
    let estado = await checkTrialStatus(u, sinCortesia);
    assert.equal(estado.renewals_left, 1);
    assert.equal(estado.max_renewals, 1);

    await vencer(u);
    const r1 = await renewTrialWithFeedback(u, 5, "bien", sinCortesia);
    assert.equal(r1.renewed, true);
    assert.equal(r1.renewed && r1.renewals_left, 0);
    assert.equal(r1.renewed && r1.courtesy, false);
    estado = await checkTrialStatus(u, sinCortesia);
    assert.equal(estado.active, true);
    assert.equal(estado.renewals_left, 0);

    await vencer(u);
    const r2 = await renewTrialWithFeedback(u, 4, "otra", sinCortesia);
    assert.equal(r2.renewed, false);
    assert.equal(!r2.renewed && r2.reason, "renewal_limit");
    assert.equal(!r2.renewed && r2.renewals_used, 1);
    assert.equal(!r2.renewed && r2.max, 1);
    assert.equal((await checkTrialStatus(u, sinCortesia)).active, false);
    assert.equal(await feedbacks(u), 2, "el feedback se guarda aunque no renueve");
  });

  await t.test("con mas de 48 h de prueba: 409 trial_active y no extiende nada", async () => {
    const u = await usuario();
    const antes = await prueba(u);
    const r = await renewTrialWithFeedback(u, 3, null, sinCortesia);
    assert.equal(!r.renewed && r.reason, "trial_active");
    const despues = await prueba(u);
    assert.equal(despues.renewed_count, 0);
    assert.equal(new Date(despues.vence).getTime(), new Date(antes.vence).getTime());
    assert.equal(await feedbacks(u), 1);
  });

  await t.test("dentro de las ultimas 48 h si renueva", async () => {
    const u = await usuario();
    await pool.query("update user_trial set trial_expires_at = now() + interval '1 day' where user_id = $1", [u]);
    const r = await renewTrialWithFeedback(u, 5, null, sinCortesia);
    assert.equal(r.renewed, true);
  });

  await t.test("suscrito: 409 subscribed, sin tocar la prueba", async () => {
    const u = await usuario();
    await pool.query(
      `insert into subscriptions (user_id, paddle_subscription_id, paddle_customer_id, status, current_period_end)
       values ($1, $2, 'ctm_trial_tope', 'active', now() + interval '1 month')`,
      [u, `sub_trial_tope_${u}`],
    );
    await vencer(u);
    const r = await renewTrialWithFeedback(u, 5, "pago", sinCortesia);
    assert.equal(!r.renewed && r.reason, "subscribed");
    assert.equal((await prueba(u)).renewed_count, 0);
    assert.equal(await feedbacks(u), 1);
    const estado = await checkTrialStatus(u, sinCortesia);
    assert.equal(estado.subscribed, true);
    assert.equal(estado.renewals_left, null);
  });

  await t.test("dos POST simultaneos con 1 restante: una sola renovacion", async () => {
    const u = await usuario();
    await vencer(u);
    const [a, b] = await Promise.all([
      renewTrialWithFeedback(u, 5, "a", sinCortesia),
      renewTrialWithFeedback(u, 5, "b", sinCortesia),
    ]);
    assert.equal([a, b].filter((r) => r.renewed).length, 1);
    assert.equal((await prueba(u)).renewed_count, 1);
    assert.equal(await feedbacks(u), 2);
  });

  await t.test("cortesia: quien ya agoto (usuario actual) renueva UNA vez mas antes de la fecha", async () => {
    const u = await usuario();
    // Usuario de antes del tope: ya renovo 6 veces.
    await pool.query("update user_trial set renewed_count = 6 where user_id = $1", [u]);
    assert.equal((await checkTrialStatus(u, conCortesia)).renewals_left, 1);
    await vencer(u);
    const r1 = await renewTrialWithFeedback(u, 5, null, conCortesia);
    assert.equal(r1.renewed, true);
    assert.equal(r1.renewed && r1.courtesy, true);
    assert.equal(r1.renewed && r1.renewals_left, 0);

    await vencer(u);
    const r2 = await renewTrialWithFeedback(u, 5, null, conCortesia);
    assert.equal(!r2.renewed && r2.reason, "renewal_limit");
  });

  await t.test("cortesia vencida: quien ya agoto recibe 409 renewal_limit", async () => {
    const u = await usuario();
    await pool.query("update user_trial set renewed_count = 3 where user_id = $1", [u]);
    await vencer(u);
    const r = await renewTrialWithFeedback(u, 5, null, cortesiaVencida);
    assert.equal(!r.renewed && r.reason, "renewal_limit");
    assert.equal((await checkTrialStatus(u, cortesiaVencida)).renewals_left, 0);
  });

  await t.test("usuario actual con prueba vigente conserva su semana", async () => {
    const u = await usuario();
    await pool.query("update user_trial set renewed_count = 8 where user_id = $1", [u]);
    const estado = await checkTrialStatus(u, sinCortesia);
    assert.equal(estado.active, true);
    assert.equal(estado.renewals_left, 0);
  });

  await pool.query("delete from users where github_id like $1", [`${prefijo}%`]);
  await pool.end();
});
