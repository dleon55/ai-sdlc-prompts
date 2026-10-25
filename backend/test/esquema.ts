// Aplica src/schema.sql bajo un bloqueo de Postgres. node --test corre los
// archivos en paralelo y varias pruebas comparten la misma base: dos
// `create table if not exists` simultaneos chocan en el catalogo
// (duplicate key en pg_type). El bloqueo los pone en fila.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import type pg from "pg";

const LLAVE_BLOQUEO = 24_102_026;
const esquema = readFileSync(path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "src", "schema.sql"), "utf8");

export async function aplicarEsquema(pool: pg.Pool): Promise<void> {
  const cliente = await pool.connect();
  try {
    await cliente.query("select pg_advisory_lock($1)", [LLAVE_BLOQUEO]);
    await cliente.query(esquema);
  } finally {
    await cliente.query("select pg_advisory_unlock($1)", [LLAVE_BLOQUEO]).catch(() => {});
    cliente.release();
  }
}
