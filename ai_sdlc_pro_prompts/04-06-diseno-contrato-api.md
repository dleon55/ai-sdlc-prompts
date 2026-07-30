# 4.6 — Diseño de contrato de API: endpoints, esquemas y semántica de interfaz

## Descripción

Prompt para diseñar el contrato de una API nueva (o un conjunto nuevo de endpoints/operaciones) desde cero: convenciones, catálogo de operaciones con sus esquemas de request/response, matriz de errores, autenticación/autorización por operación y reglas transversales (paginación, idempotencia, rate limiting). Produce la especificación del contrato, no el código que lo implementa.

**Cuándo usarlo:** después del diseño de solución (`04-01`) cuando este expone una API nueva, o como paso independiente cuando el requerimiento es explícitamente diseñar una interfaz. Distinto de `04-05-versionado-deprecacion-api`, que evoluciona el contrato de una API **ya existente**: este prompt diseña el contrato desde cero, antes de que exista ningún consumidor.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | medio — un contrato mal diseñado (inconsistente, sin manejo de errores completo, sin estrategia de paginación o versionado desde el inicio) es costoso de corregir una vez que existen consumidores reales integrados; el prompt no implementa ni despliega nada por sí mismo |
| Entradas requeridas | diseño de solución (`04-01`) si existe, casos de uso relacionados (`04-03`) si existen, consumidores previstos (internos/externos), estilo de API (REST/GraphQL/gRPC/otro), convenciones ya existentes en el proyecto si las hay |
| Herramientas permitidas | lectura de diseño, casos de uso y contratos existentes — sin ejecución ni cambios; produce una especificación de contrato en texto, no código ni configuración de gateway |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si el estilo de API (REST/GraphQL/gRPC) no está definido y no puede inferirse de convenciones ya existentes en el proyecto, preguntar antes de asumir uno; ninguna operación puede quedar sin su matriz de errores definida |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada operación del catálogo declara método/ruta (o su equivalente en el estilo elegido), autenticación requerida, esquema de request, esquema de response de éxito y matriz de errores; toda desviación de una convención ya existente en el proyecto queda declarada explícitamente |
| Siguiente prompt recomendado | `04-05-versionado-deprecacion-api` cuando este contrato deba evolucionar más adelante; `05-01-plan-implementacion` para planificar la construcción; `07-02-pruebas-integracion` para diseñar las pruebas del contrato |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña el contrato completo de la API o del conjunto de endpoints/operaciones descrito: convenciones, catálogo de operaciones con esquemas de request/response, matriz de errores, autenticación/autorización y reglas transversales.

Entradas:
- diseño de solución relacionado: [PEGAR O REFERENCIA A 04-01, O "no existe aún"]
- casos de uso relacionados: [PEGAR O REFERENCIA A 04-03, O "no existen aún"]
- consumidores previstos: [INTERNOS / EXTERNOS / AMBOS]
- estilo de API: [REST / GraphQL / gRPC / OTRO]
- convenciones existentes del proyecto: [PEGAR O "ninguna, es la primera API del proyecto"]

Actividades:
1. CONVENCIONES GENERALES
   Define o reutiliza las convenciones del contrato: naming (camelCase/snake_case), plural/singular en rutas o tipos, formato de fecha/hora y zona horaria, estrategia de versionado desde el día uno (aunque sea v1 implícito). Si el proyecto ya tiene una API previa, reutiliza sus convenciones; cualquier apartamiento debe declararse explícitamente como desviación, no introducirse en silencio.

2. CATÁLOGO DE OPERACIONES
   Para cada operación (endpoint REST, query/mutation GraphQL, RPC gRPC, según el estilo elegido): propósito, método+ruta u operación equivalente, esquema de request (parámetros, query, body) con tipo y si es requerido u opcional, esquema de response de éxito, y matriz de errores (código + condición que lo dispara + payload de error). Ninguna operación puede quedar sin su matriz de errores.

3. AUTENTICACIÓN Y AUTORIZACIÓN
   Para cada operación, define si es pública, requiere autenticación, o requiere un rol/scope específico. Si la política requerida para una operación sensible no está clara, márcala explícitamente como "[DECISIÓN PENDIENTE: verificar con seguridad]" en vez de asumir un nivel de acceso.

4. REGLAS TRANSVERSALES
   Define paginación (cursor vs. offset y por qué), filtrado y ordenamiento soportados, rate limiting, idempotencia en operaciones de escritura (¿se requiere una idempotency key?), y formato uniforme de fecha/hora.

5. CONSISTENCIA CON CONVENCIONES EXISTENTES
   Si el proyecto ya expone otra API, compara el nuevo contrato contra sus convenciones y señala cualquier inconsistencia detectada — no la resuelvas en silencio adoptando un estilo distinto sin declararlo.

6. DECISIONES PENDIENTES
   Señala explícitamente con "[DECISIÓN PENDIENTE: razón]" cualquier aspecto que el negocio o seguridad aún no ha definido (ej. límites exactos de rate limiting, política de retención de datos expuestos).

Restricciones:
- ninguna operación puede quedar sin su comportamiento de error definido (código + payload) — una operación sin camino de error declarado se reporta como incompleta, no se omite silenciosamente,
- no inventes convenciones nuevas si el proyecto ya tiene un estilo establecido — reutilízalo; si te apartas de él, decláralo explícitamente como una desviación a validar,
- no asumas por omisión el nivel de autenticación/autorización de una operación sensible — si no está claro, márcalo como "[DECISIÓN PENDIENTE: verificar con seguridad]",
- este prompt produce una especificación de contrato en texto (estilo OpenAPI/schema descriptivo); no genera código, no configura infraestructura de gateway ni despliega nada.

Salida:
0. Bloque JSON de metadatos (claves: status, endpoint_count, pending_decisions_count, confidence_score [0.0 a 1.0]).
1. Convenciones generales del contrato.
2. Catálogo de operaciones: Operación | Método/ruta o equivalente | Auth requerida | Request schema | Response (éxito) | Matriz de errores
3. Reglas transversales: paginación, filtrado/ordenamiento, rate limiting, idempotencia, formato de fecha/hora.
4. Desviaciones respecto a convenciones existentes del proyecto (si las hay).
5. Decisiones pendientes de validar con negocio o seguridad.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de diseño de contrato de API y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA OBJETIVO]
- componentes: [SERVICIO(S) QUE EXPONDRÁN LA API]
- documentos a revisar: diseño de solución (04-01), casos de uso (04-03), convenciones de API existentes
- objetivo puntual de salida: catálogo de endpoints con esquemas de request/response y matriz de errores
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen del contrato |
| Convenciones (1) | Naming, formato de fecha, estrategia de versionado desde el inicio |
| Catálogo de operaciones (2) | Cada operación con su esquema completo de request/response y errores |
| Reglas transversales (3) | Paginación, rate limiting, idempotencia, ordenamiento/filtrado |
| Desviaciones (4) | Inconsistencias señaladas frente a convenciones ya existentes, si las hay |
| Decisiones pendientes (5) | Aspectos no definidos aún por negocio o seguridad |

### Ejemplo (fragmento)

```json
{
  "status": "diseñado_con_pendientes",
  "endpoint_count": 6,
  "pending_decisions_count": 1,
  "confidence_score": 0.75
}
```

| Operación | Método/ruta | Auth requerida | Request | Response (éxito) | Errores |
|---|---|---|---|---|---|
| Crear pedido | `POST /v1/orders` | Autenticada (usuario final) | `{ "items": [{ "sku": string, "qty": int }], "shippingAddressId": string }` | `201` `{ "orderId": string, "status": "pending", "total": number }` | `400` datos inválidos · `401` no autenticado · `409` `idempotency-key` repetida con payload distinto · `422` `sku` inexistente |
| Cancelar pedido | `POST /v1/orders/{orderId}/cancel` | Autenticada + dueño del pedido o rol `support` | (sin body) | `200` `{ "orderId": string, "status": "cancelled" }` | `401` no autenticado · `403` no es dueño ni tiene rol `support` · `404` pedido inexistente · `409` pedido ya enviado, no cancelable |
