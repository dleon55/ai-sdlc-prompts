// A donde vuelve el usuario tras iniciar sesion (?volver= en /api/auth/login).
//
// Solo se acepta una ruta RELATIVA del propio sitio: empieza por una sola
// "/", sin esquema, sin "//" (eso seria otro dominio para el navegador),
// sin barras invertidas ni caracteres de control. Cualquier otra cosa cae a
// "/". Sin esta validacion, /api/auth/login?volver=https://malicioso.example
// convertiria el login en un redirector abierto con la marca del sitio.
const RUTA_SEGURA = /^\/(?![\/\\])[A-Za-z0-9._~!$&'()*+,;=:@%\/?-]*$/;

export function rutaDeVuelta(valor: unknown): string {
  if (typeof valor !== "string" || valor.length > 200) return "/";
  return RUTA_SEGURA.test(valor) && !valor.includes("\\") ? valor : "/";
}
