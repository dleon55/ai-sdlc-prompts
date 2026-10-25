// Fase 2 de docs/PLAN_MIGRACION_SUPABASE_A_LOCAL.md: el login SIGUE en
// Supabase mientras la prueba y los pagos sigan alli (Fase 3). Para que el
// usuario tenga una sola sesion, este backend acepta el access_token de
// Supabase (Authorization: Bearer) en las rutas de datos ya migradas.
//
// Supabase firma esos tokens con ES256 y publica la clave publica en
// <SUPABASE_URL>/auth/v1/.well-known/jwks.json: verificar no requiere
// ningun secreto. El `sub` es el UUID de auth.users, el mismo que la
// migracion conserva en users.id (plan §4.1).
//
// Sin SUPABASE_URL esta via queda apagada y solo vale la cookie propia.
import { createRemoteJWKSet, jwtVerify, type JWTVerifyGetKey } from "jose";

export interface IdentidadSupabase {
  userId: string;
  githubId: string;
  githubLogin: string;
  email: string | null;
}

let obtenerClave: JWTVerifyGetKey | null = null;
let emisor: string | null = null;

function configuracion(): { clave: JWTVerifyGetKey; iss: string } | null {
  const url = process.env.SUPABASE_URL?.trim().replace(/\/+$/, "");
  if (!url) return null;
  const iss = `${url}/auth/v1`;
  if (!obtenerClave || emisor !== iss) {
    obtenerClave = createRemoteJWKSet(new URL(`${iss}/.well-known/jwks.json`));
    emisor = iss;
  }
  return { clave: obtenerClave, iss };
}

// Solo para pruebas: sustituye la descarga de claves por un juego local.
export function usarClavesDePrueba(clave: JWTVerifyGetKey, iss: string): void {
  obtenerClave = clave;
  emisor = iss;
}

function texto(valor: unknown): string | null {
  return typeof valor === "string" && valor.trim() ? valor : null;
}

// Devuelve la identidad si el token es un access_token valido de Supabase
// de un usuario de GitHub; null en cualquier otro caso (vencido, firma
// invalida, otro emisor, anonimo, sin identidad de GitHub). Nunca lanza.
export async function verificarTokenSupabase(token: string): Promise<IdentidadSupabase | null> {
  const conf = emisor && obtenerClave ? { clave: obtenerClave, iss: emisor } : configuracion();
  if (!conf) return null;
  try {
    const { payload } = await jwtVerify(token, conf.clave, {
      issuer: conf.iss,
      audience: "authenticated",
      algorithms: ["ES256"],
    });
    const userId = texto(payload.sub);
    const meta = (payload.user_metadata ?? {}) as Record<string, unknown>;
    const githubId = texto(meta.provider_id);
    const githubLogin = texto(meta.user_name) ?? texto(meta.preferred_username);
    if (!userId || !githubId || !githubLogin || payload.role !== "authenticated") return null;
    return { userId, githubId, githubLogin, email: texto(payload.email) };
  } catch {
    return null;
  }
}
