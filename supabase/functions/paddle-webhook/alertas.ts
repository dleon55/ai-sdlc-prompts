// Alertas operativas de cobro para la Edge Function del webhook de Paddle
// (issue #232, T5). Una sola función, `alertar({clave, detalle})`, con dos
// salidas, ambas opcionales y nunca bloqueantes:
//
//   1. Log estructurado nivel error (siempre). Es lo que se ve en
//      Supabase → Edge Functions → paddle-webhook → Logs.
//   2. POST JSON a ALERTAS_WEBHOOK_URL si la variable existe. El cuerpo
//      lleva `text` (Slack) y `content` (Discord) además de los campos
//      estructurados, para que sirva con cualquiera sin adaptador.
//
// Por qué existe: antes, un `apply_paddle_subscription_event` que fallaba
// devolvía 500 y Paddle reintentaba en silencio. Si el error era
// permanente (migración sin aplicar, user_id ausente) el cliente pagaba y
// no recibía acceso, y nadie se enteraba hasta que escribía a soporte.
//
// Deduplicación: la misma clave + id no se reenvía durante una hora. Un
// webhook que Paddle reintenta cada pocos minutos generaría decenas de
// avisos idénticos por un solo incidente. La ventana vive en memoria del
// aislado de Deno: si Supabase recicla el aislado, se vuelve a avisar, que
// es el lado seguro del error.
//
// Nunca lanza: una alerta que tumba al webhook que la emite es peor que
// ninguna alerta. Cada salida está envuelta y el resultado se devuelve
// como un estado, para que las pruebas lo comprueben sin red.
//
// Este módulo no toca `Deno.*` a propósito: recibe fetch/reloj/log por
// inyección y así se ejecuta tal cual en Node para las pruebas
// (tests/js/test_alertas_runtime.js), donde no hay runtime de Deno.

export type ClaveAlerta = "webhook_error" | "reembolso";

export type ValorDetalle = string | number | boolean | null | undefined;
export type DetalleAlerta = Record<string, ValorDetalle>;

export type ResultadoAlerta = "enviada" | "deduplicada" | "solo_log" | "fallo_webhook";

export interface OpcionesAlertador {
  /** Destino del POST. Vacío o ausente = solo log. */
  webhookUrl?: string;
  /** Inyectable para pruebas; por defecto el fetch global. */
  fetchImpl?: typeof fetch;
  /** Reloj inyectable (ms). Por defecto Date.now. */
  ahora?: () => number;
  /** Sumidero del log estructurado. Por defecto console.error. */
  log?: (mensaje: string, datos: Record<string, unknown>) => void;
  /** Slug que identifica al producto en un canal compartido. */
  producto?: string;
}

export const VENTANA_DEDUP_MS = 60 * 60 * 1000;

// Claves que jamás deben viajar en una alerta aunque un llamador las pase
// por descuido. Se filtra por nombre y no por valor porque el valor de un
// secreto no tiene forma reconocible; el nombre sí.
const CLAVES_PROHIBIDAS = /secret|token|password|authorization|signature|service_role|api_key|apikey/i;
const MAX_LARGO_VALOR = 500;

export function limpiarDetalle(detalle: DetalleAlerta): DetalleAlerta {
  const limpio: DetalleAlerta = {};
  for (const [clave, valor] of Object.entries(detalle)) {
    if (CLAVES_PROHIBIDAS.test(clave)) continue;
    if (typeof valor === "string" && valor.length > MAX_LARGO_VALOR) {
      limpio[clave] = valor.slice(0, MAX_LARGO_VALOR) + "…";
    } else {
      limpio[clave] = valor;
    }
  }
  return limpio;
}

function claveDedup(clave: ClaveAlerta, detalle: DetalleAlerta): string {
  const id = detalle.event_id ?? detalle.id ?? "";
  return `${clave}:${String(id)}`;
}

export function crearAlertador(opciones: OpcionesAlertador = {}) {
  const webhookUrl = (opciones.webhookUrl ?? "").trim();
  const fetchImpl = opciones.fetchImpl ?? globalThis.fetch;
  const ahora = opciones.ahora ?? (() => Date.now());
  const log = opciones.log ?? ((mensaje, datos) => console.error(mensaje, JSON.stringify(datos)));
  const producto = opciones.producto ?? "ai-sdlc-pro";
  const recientes = new Map<string, number>();

  return async function alertar(
    entrada: { clave: ClaveAlerta; detalle: DetalleAlerta },
  ): Promise<ResultadoAlerta> {
    try {
      const detalle = limpiarDetalle(entrada.detalle);
      const t = ahora();
      const k = claveDedup(entrada.clave, detalle);

      // Purga perezosa: sin temporizadores, que en un aislado efímero no
      // tienen garantía de correr.
      for (const [clave, visto] of recientes) {
        if (t - visto > VENTANA_DEDUP_MS) recientes.delete(clave);
      }
      const visto = recientes.get(k);
      if (visto !== undefined && t - visto <= VENTANA_DEDUP_MS) {
        return "deduplicada";
      }
      recientes.set(k, t);

      const fecha = new Date(t).toISOString();
      const resumen = `[${producto}] ${entrada.clave} — ${describir(detalle)}`;
      log(`ALERTA ${entrada.clave}`, { producto, clave: entrada.clave, detalle, fecha });

      if (!webhookUrl) return "solo_log";

      try {
        const respuesta = await fetchImpl(webhookUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            producto,
            clave: entrada.clave,
            detalle,
            fecha,
            text: resumen,
            content: resumen,
          }),
        });
        if (!respuesta.ok) {
          log("ALERTA webhook respondió con error", { status: respuesta.status, clave: entrada.clave });
          return "fallo_webhook";
        }
        return "enviada";
      } catch (error) {
        log("ALERTA webhook inalcanzable", { clave: entrada.clave, error: mensajeDe(error) });
        return "fallo_webhook";
      }
    } catch (error) {
      // Último recurso: que nada de lo anterior tumbe al llamador.
      try {
        console.error("alertar() falló", mensajeDe(error));
      } catch {
        // ignorado a propósito
      }
      return "solo_log";
    }
  };
}

function describir(detalle: DetalleAlerta): string {
  const partes: string[] = [];
  for (const [clave, valor] of Object.entries(detalle)) {
    if (valor === undefined || valor === null || valor === "") continue;
    partes.push(`${clave}=${String(valor)}`);
  }
  return partes.join(" ") || "(sin detalle)";
}

export function mensajeDe(error: unknown): string {
  if (error instanceof Error) return error.message;
  if (typeof error === "string") return error;
  try {
    return JSON.stringify(error);
  } catch {
    return String(error);
  }
}
