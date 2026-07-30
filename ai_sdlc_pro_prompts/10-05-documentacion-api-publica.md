# 10.5 — Documentación pública de API para desarrolladores externos

## Descripción

Prompt para producir la documentación pública de referencia de una API ya diseñada e implementada: guía de inicio rápido, referencia de endpoints con ejemplos reales, guías de casos de uso, versionado visible y límites de uso — dirigida a desarrolladores externos que integran contra la API, no a los ingenieros que la construyen. Distinto de `04-06-diseno-contrato-api` (diseño del contrato, para ingenieros, declara explícitamente que no produce documentación) y de `10-01-documentacion-tecnica` (documentación técnica interna del repositorio).

**Cuándo usarlo:** después de que el contrato de API ya está diseñado (`04-06`) e implementado, antes de exponerlo a consumidores externos (partners, clientes, terceros).

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo-medio — documentación pública incorrecta o desactualizada genera tickets de soporte y fricción de adopción para integradores externos, pero el prompt no ejecuta ni modifica la API en sí |
| Entradas requeridas | contrato de API ya implementado (referencia a `04-06` o especificación real), audiencia objetivo (desarrolladores externos/partners/clientes), ejemplos de uso reales si existen |
| Herramientas permitidas | lectura del contrato y del código de la API existente — sin ejecutar nada |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si el comportamiento a documentar no puede verificarse contra la implementación real (el contrato de diseño quedó desactualizado respecto al código), detente y señala la discrepancia en vez de documentar el diseño teórico como si fuera el comportamiento real |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada endpoint documentado incluye ejemplo de request/response verificado, mecanismo de autenticación, y al menos un ejemplo de error con causa y acción recomendada |
| Siguiente prompt recomendado | `10-03-release-changelog` cuando la API tenga una nueva versión que anunciar a los consumidores |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Produce la documentación pública de referencia de la API descrita, dirigida a desarrolladores externos que la integran, verificada contra el comportamiento real de la implementación.

Entradas:
- contrato de API ya implementado: [PEGAR O REFERENCIA A 04-06 U OTRA ESPECIFICACIÓN]
- audiencia objetivo: [DESARROLLADORES EXTERNOS / PARTNERS / CLIENTES]
- ejemplos de uso reales: [PEGAR O "generar ejemplos representativos"]

Actividades:
1. GETTING STARTED
   Documenta cómo autenticarse y un primer request de ejemplo completo, de principio a fin, que un desarrollador externo pueda ejecutar sin contexto adicional.

2. REFERENCIA DE ENDPOINTS
   Para cada endpoint: descripción en lenguaje claro (sin jerga interna del equipo), parámetros con tipo y si son requeridos, ejemplo real de request y response, y códigos de error con qué significan específicamente para el consumidor.

3. GUÍAS DE CASOS DE USO
   Más allá de la referencia plana, documenta 2-3 flujos típicos completos paso a paso (ej. "cómo procesar un reembolso de principio a fin usando esta API").

4. VERSIONADO Y DEPRECACIÓN VISIBLE
   Documenta el esquema de versionado vigente y, si hay un cambio de contrato en curso, referencia la estrategia de `04-05-versionado-deprecacion-api` en términos que el consumidor externo entienda (qué debe cambiar y para cuándo).

5. LÍMITES Y CUOTAS
   Documenta el rate limiting y cualquier cuota de uso en términos que el consumidor externo pueda planificar (ej. "300 requests/minuto por API key", no solo el código de error 429).

6. CHANGELOG RECIENTE
   Resume los cambios recientes de la API relevantes para consumidores externos.

Restricciones:
- nunca documentes un comportamiento sin verificarlo contra el contrato o el código real — si hay discrepancia entre lo diseñado y lo implementado, señálala explícitamente en vez de documentar la versión "ideal" como si fuera el comportamiento real,
- usa siempre lenguaje dirigido al consumidor externo (qué necesita hacer, qué obtiene como resultado) — nunca jerga interna del equipo o nombres de componentes internos que el consumidor no puede ver,
- todo código de error documentado debe explicar la causa probable y la acción recomendada para el consumidor, no solo el código HTTP desnudo,
- nunca publiques credenciales reales, tokens de ejemplo funcionales, ni datos de producción reales en los ejemplos — usa siempre placeholders claramente marcados como tales.

Salida:
0. Bloque JSON de metadatos (claves: status, endpoints_documented, examples_count, confidence_score [0.0 a 1.0]).
1. Getting started: autenticación y primer request de ejemplo.
2. Referencia de endpoints con ejemplos de request/response y errores.
3. Guías de casos de uso completos.
4. Versionado y deprecación visible para el consumidor.
5. Límites y cuotas de uso.
6. Changelog reciente relevante para consumidores.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de documentación pública de API y adáptalo a:
- repositorio: [NOMBRE O URL]
- componentes: [SERVICIO(S) QUE EXPONEN LA API]
- documentos a revisar: contrato de API (04-06), código de la API implementada, changelog previo
- objetivo puntual de salida: documentación de referencia pública lista para publicar
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen de la documentación |
| Getting started (1) | Autenticación y primer request ejecutable de principio a fin |
| Referencia de endpoints (2) | Cada endpoint con ejemplos verificados de request/response y errores |
| Guías de casos de uso (3) | Flujos completos documentados paso a paso |
| Versionado (4) | Esquema vigente y cambios en curso, en términos del consumidor |
| Límites y cuotas (5) | Rate limiting explicado en términos planificables |
| Changelog (6) | Cambios recientes relevantes para consumidores externos |

### Ejemplo (fragmento)

```json
{
  "status": "documentado_con_discrepancia",
  "endpoints_documented": 9,
  "examples_count": 14,
  "confidence_score": 0.79
}
```

| Endpoint | Descripción | Ejemplo de error |
|---|---|---|
| `POST /v1/orders` | Crea un nuevo pedido para el usuario autenticado | `422 { "error": "sku_not_found", "message": "El SKU 'ABC-123' no existe en el catálogo. Verifica el identificador antes de reintentar." }` |

| Sección | Ejemplo de contenido |
|---|---|
| Discrepancia detectada | El contrato de diseño (`04-06`) declara que `GET /v1/orders/{id}` requiere solo autenticación de usuario, pero la implementación real exige además el scope `orders:read` — documentado según el comportamiento real verificado en el código, y señalado como desviación a corregir en el contrato de diseño |
