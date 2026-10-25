// Direccion en la que escucha el backend.
//
// Por defecto solo loopback: en la VM, nginx es la unica puerta publica y
// llega al backend por 127.0.0.1. Sin direccion explicita, Express escucha
// en todas las interfaces y la unica barrera pasaria a ser el cortafuegos.
// HOST permite otra interfaz (por ejemplo 0.0.0.0 dentro de un contenedor)
// solo cuando se pide a proposito.
export function direccionDeEscucha(env: Record<string, string | undefined>): string {
  const host = env.HOST?.trim();
  return host ? host : "127.0.0.1";
}
