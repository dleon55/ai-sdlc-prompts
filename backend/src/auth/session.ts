// Sesion propia (reemplaza el JWT que hoy emite GoTrue). Ver
// docs/PLAN_MIGRACION_SUPABASE_A_LOCAL.md §2.1: pasar de localStorage a
// una cookie httpOnly es una mejora de seguridad real (cierra el robo de
// token por XSS), a cambio de necesitar proteccion CSRF explicita
// (SameSite=Lax la cubre para esta app: no hay formularios cross-site que
// deban mutar estado, y el webhook de Paddle no usa esta cookie).
import { SignJWT, jwtVerify } from "jose";
import { parse as parseCookieHeader, serialize as serializeCookie } from "cookie";
import type { Request, Response } from "express";
import { pool } from "../db.ts";
import { verificarTokenSupabase, type IdentidadSupabase } from "./supabase.ts";

const SESSION_COOKIE_NAME = "ai_sdlc_session";
const SESSION_TTL_SECONDS = 30 * 24 * 60 * 60; // 30 dias

function signingKey(): Uint8Array {
  const secret = process.env.JWT_SIGNING_SECRET;
  if (!secret || secret.length < 16) {
    throw new Error(
      "JWT_SIGNING_SECRET no configurado o demasiado corto (ver backend/.env.example)",
    );
  }
  return new TextEncoder().encode(secret);
}

export interface SessionPayload {
  userId: string;
  githubLogin: string;
}

export async function issueSessionCookie(res: Response, payload: SessionPayload): Promise<void> {
  const token = await new SignJWT({ githubLogin: payload.githubLogin })
    .setProtectedHeader({ alg: "HS256" })
    .setSubject(payload.userId)
    .setIssuedAt()
    .setExpirationTime(`${SESSION_TTL_SECONDS}s`)
    .sign(signingKey());

  res.setHeader(
    "Set-Cookie",
    serializeCookie(SESSION_COOKIE_NAME, token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: SESSION_TTL_SECONDS,
    }),
  );
}

export function clearSessionCookie(res: Response): void {
  res.setHeader(
    "Set-Cookie",
    serializeCookie(SESSION_COOKIE_NAME, "", {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: 0,
    }),
  );
}

// Usuarios de Supabase que ya tienen fila en users en este proceso: la
// fila se asegura una vez, no en cada peticion.
const usuariosAsegurados = new Set<string>();

// Un usuario que se registra en Supabase DESPUES de la migracion no tiene
// fila en users, y projects la exige (foreign key). Se crea con el mismo
// UUID; si ya existe, se refrescan login y correo.
async function asegurarUsuario(identidad: IdentidadSupabase): Promise<void> {
  if (usuariosAsegurados.has(identidad.userId)) return;
  await pool.query(
    `insert into users (id, github_id, github_login, email)
     values ($1, $2, $3, $4)
     on conflict (id) do update set
       github_login = excluded.github_login,
       email = coalesce(excluded.email, users.email)`,
    [identidad.userId, identidad.githubId, identidad.githubLogin, identidad.email],
  );
  usuariosAsegurados.add(identidad.userId);
}

// Fase 2: sin cookie propia, se acepta el access_token de Supabase en
// Authorization: Bearer. Un header no viaja solo como una cookie, asi que
// esta via no necesita proteccion CSRF.
async function sesionDesdeSupabase(req: Request): Promise<SessionPayload | null> {
  const auth = req.headers.authorization;
  if (!auth || !auth.startsWith("Bearer ")) return null;
  const identidad = await verificarTokenSupabase(auth.slice("Bearer ".length).trim());
  if (!identidad) return null;
  await asegurarUsuario(identidad);
  return { userId: identidad.userId, githubLogin: identidad.githubLogin };
}

export async function readSession(req: Request): Promise<SessionPayload | null> {
  const header = req.headers.cookie;
  const cookies = header ? parseCookieHeader(header) : {};
  const token = cookies[SESSION_COOKIE_NAME];
  if (!token) return sesionDesdeSupabase(req);

  try {
    const { payload } = await jwtVerify(token, signingKey());
    if (typeof payload.sub !== "string" || typeof payload.githubLogin !== "string") {
      return null;
    }
    return { userId: payload.sub, githubLogin: payload.githubLogin };
  } catch {
    // Firma invalida, vencido, o corrupto -- tratar como sin sesion, nunca
    // lanzar (un token roto no debe tumbar la request).
    return null;
  }
}
