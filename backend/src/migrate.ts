// Aplica backend/src/schema.sql contra DATABASE_URL. Idempotente (todo el
// esquema usa `create table if not exists` / `create or replace function`),
// asi que correrlo de nuevo contra una base ya migrada no hace nada.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { pool } from "./db.ts";

const here = path.dirname(fileURLToPath(import.meta.url));
const schemaSql = readFileSync(path.join(here, "schema.sql"), "utf8");

async function main() {
  await pool.query(schemaSql);
  console.log("Esquema aplicado correctamente.");
  await pool.end();
}

main().catch((error) => {
  console.error("Fallo al aplicar el esquema:", error);
  process.exitCode = 1;
});
