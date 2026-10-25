import type { NextFunction, Request, RequestHandler, Response } from "express";

// Express 4 no atrapa las promesas rechazadas de un manejador `async`: el
// rechazo queda sin manejar y Node termina el proceso. Con esto, un fallo
// de base de datos (Postgres reiniciando, una consulta con un parametro
// invalido) tumbaba el backend entero en vez de responder 500 a esa sola
// peticion. Todo manejador o middleware `async` se registra envuelto aqui
// (lo vigila test/asincrono.test.ts), para que el rechazo llegue a
// manejadorDeErrores como cualquier error sincrono.
export function asincrono(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<unknown>,
): RequestHandler {
  return (req, res, next) => {
    fn(req, res, next).catch(next);
  };
}

// Ultimo middleware de la app. Responde un 500 generico, sin detalles
// internos. Si la respuesta ya empezo a enviarse no se puede cambiar el
// estado: se delega en Express, que cierra la conexion.
export function manejadorDeErrores(err: unknown, _req: Request, res: Response, next: NextFunction): void {
  console.error("Error no manejado:", err);
  if (res.headersSent) {
    next(err);
    return;
  }
  res.status(500).json({ error: "Error interno" });
}
