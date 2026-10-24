import { Router } from "express";
import { parse as parseCookieHeader, serialize as serializeCookie } from "cookie";
import { authorizeUrl, exchangeCodeForUser, generateState } from "../auth/github.ts";
import { clearSessionCookie, issueSessionCookie, readSession } from "../auth/session.ts";
import { pool } from "../db.ts";

export const authRouter = Router();

const STATE_COOKIE_NAME = "ai_sdlc_oauth_state";
const STATE_COOKIE_TTL_SECONDS = 10 * 60; // la vuelta completa a GitHub y de regreso no deberia tardar mas

// GET /api/auth/login -- inicia el flujo. El `state` viaja tanto a GitHub
// como en una cookie propia de corta duracion; el callback exige que
// coincidan (si no, CSRF: alguien podria mandar a la victima un callback
// con un `code` que no es el suyo).
authRouter.get("/login", (req, res) => {
  const state = generateState();
  res.setHeader(
    "Set-Cookie",
    serializeCookie(STATE_COOKIE_NAME, state, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: STATE_COOKIE_TTL_SECONDS,
    }),
  );
  res.redirect(authorizeUrl(state));
});

authRouter.get("/callback", async (req, res) => {
  const frontendUrl = process.env.FRONTEND_URL ?? "/";
  const code = typeof req.query.code === "string" ? req.query.code : null;
  const state = typeof req.query.state === "string" ? req.query.state : null;
  const cookies = parseCookieHeader(req.headers.cookie ?? "");
  const expectedState = cookies[STATE_COOKIE_NAME];

  if (!code || !state || !expectedState || state !== expectedState) {
    res.status(401).send("Login invalido o vencido -- intenta de nuevo.");
    return;
  }

  try {
    const githubUser = await exchangeCodeForUser(code);

    const { rows } = await pool.query<{ id: string }>(
      `insert into users (github_id, github_login, email)
       values ($1, $2, $3)
       on conflict (github_id) do update set
         github_login = excluded.github_login,
         email = excluded.email
       returning id`,
      [githubUser.githubId, githubUser.githubLogin, githubUser.email],
    );
    const userId = rows[0]!.id;

    await issueSessionCookie(res, { userId, githubLogin: githubUser.githubLogin });
    res.redirect(frontendUrl);
  } catch (error) {
    console.error("GitHub OAuth callback fallo:", error);
    res.status(502).send("No se pudo completar el login con GitHub -- intenta de nuevo.");
  }
});

// GET /api/auth/session -- equivalente a client.auth.getSession() del
// SDK de Supabase: siempre 200, con user:null si no hay sesion.
authRouter.get("/session", async (req, res) => {
  const session = await readSession(req);
  res.json({ user: session ? { id: session.userId, githubLogin: session.githubLogin } : null });
});

authRouter.post("/logout", (_req, res) => {
  clearSessionCookie(res);
  res.status(204).end();
});
