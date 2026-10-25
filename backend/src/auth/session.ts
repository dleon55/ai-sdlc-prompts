// Sesion propia: JWT firmado en una cookie httpOnly. Que el script de la
// pagina no pueda leerla cierra el robo de sesion por XSS, a cambio de
// necesitar proteccion CSRF explicita
// (SameSite=Lax la cubre para esta app: no hay formularios cross-site que
// deban mutar estado, y el webhook de Paddle no usa esta cookie).
import { SignJWT, jwtVerify } from "jose";
import { parse as parseCookieHeader, serialize as serializeCookie } from "cookie";
import type { Request, Response } from "express";

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

export async function readSession(req: Request): Promise<SessionPayload | null> {
  const header = req.headers.cookie;
  if (!header) return null;
  const cookies = parseCookieHeader(header);
  const token = cookies[SESSION_COOKIE_NAME];
  if (!token) return null;

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
