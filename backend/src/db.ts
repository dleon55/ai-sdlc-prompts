import { Pool, type PoolClient } from "pg";

// A proposito, sin validar DATABASE_URL aqui: este modulo lo importan
// tambien rutas (paddle.ts, projects.ts, etc.) que a su vez importan
// pruebas de logica pura (ej. test/webhookSignature.test.ts) que nunca
// llegan a ejecutar una query. `pg.Pool` no se conecta en el constructor
// -- si DATABASE_URL falta, el error real aparece claro y tarde, en el
// primer intento de `pool.query()`/`pool.connect()`, no al cargar el modulo.
export const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export async function withTransaction<T>(
  fn: (client: PoolClient) => Promise<T>,
): Promise<T> {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const result = await fn(client);
    await client.query("COMMIT");
    return result;
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    client.release();
  }
}
