import type { NextFunction, Request, Response } from "express";
import { readSession, type SessionPayload } from "./session.ts";
import { asincrono } from "../asincrono.ts";

declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Express {
    interface Request {
      session?: SessionPayload;
    }
  }
}

// Carga la sesion si existe, pero nunca bloquea la request -- usado en
// rutas publicas que se comportan distinto con/sin sesion (ej.
// prompt-stats, que hoy acepta tanto anon como authenticated).
export const loadSession = asincrono(async (req: Request, _res: Response, next: NextFunction) => {
  req.session = (await readSession(req)) ?? undefined;
  next();
});

// Equivalente a las politicas RLS que exigen `auth.uid()`: sin sesion
// valida, 401 antes de tocar la base de datos.
export const requireAuth = asincrono(async (req: Request, res: Response, next: NextFunction) => {
  const session = await readSession(req);
  if (!session) {
    res.status(401).json({ error: "No autenticado" });
    return;
  }
  req.session = session;
  next();
});
