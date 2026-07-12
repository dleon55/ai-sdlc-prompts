# 4.5 — Versionado y deprecación de API

## Descripción

Prompt para diseñar la estrategia de versionado y deprecación de una API cuando su contrato debe cambiar: esquema de numeración de versiones, ventana de compatibilidad hacia atrás, calendario de deprecación con hitos concretos y guía de migración para los consumidores. Produce el plan de evolución del contrato, no el código que lo implementa.

**Cuándo usarlo:** cuando un cambio en una API rompe (o puede romper) el contrato existente con sus consumidores — renombrar/eliminar campos, cambiar tipos, modificar autenticación, cambiar códigos de estado o semántica de un endpoint — y hace falta decidir cómo introducirlo sin dejar a los clientes sin aviso. Es más específico y táctico que `04-04-adr-decisiones-arquitectura`: un ADR documenta y justifica una decisión arquitectónica en general, mientras que este prompt resuelve exclusivamente la evolución del contrato de una API (numeración, ventanas, comunicación). Úsalo también como paso especializado después de `04-01-diseno-solucion` cuando el diseño resultante expone o modifica una superficie de API pública o consumida por otros sistemas.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño |
| Riesgo esperado | bajo-medio — el prompt solo produce un documento de estrategia, pero un plan de deprecación mal calibrado (ventana insuficiente, comunicación deficiente) puede romper integraciones reales de consumidores si se ejecuta tal cual sin revisión |
| Entradas requeridas | endpoint(s) u operación afectada, naturaleza del cambio propuesto, consumidores conocidos de la API (internos/externos, si se conocen), política de versionado existente del proyecto (si existe), SLA o acuerdos de soporte vigentes con consumidores |
| Herramientas permitidas | lectura de la especificación de API existente (OpenAPI/Swagger, GraphQL SDL, contratos), changelogs previos y documentación de consumidores; solo redacción del documento de estrategia — no modifica código ni configuración de la API |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | detener y escalar si no se puede determinar si el cambio es breaking o no; detener si se desconoce por completo la base de consumidores y el prompt no puede señalar explícitamente ese vacío; nunca proponer eliminar una versión sin período de aviso definido |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada cambio clasificado explícitamente como breaking o no-breaking con justificación; hitos de fecha (anuncio, ventana de soporte dual, fin de soporte) definidos aunque sean estimados; nota explícita cuando los consumidores o su volumen de uso son desconocidos |
| Siguiente prompt recomendado | `09-06-coordinacion-breaking-changes` para notificar y coordinar con los equipos y consumidores afectados una vez definida la estrategia de versionado |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña la estrategia de versionado y deprecación para el/los cambio(s) de contrato de API descritos, de forma que los consumidores existentes tengan una ruta de migración clara y un tiempo razonable para adoptarla.

Inputs requeridos:
- endpoint(s) u operación afectada: [RUTA / OPERACIÓN]
- cambio propuesto: [DESCRIPCIÓN DEL CAMBIO]
- consumidores conocidos: [INTERNOS / EXTERNOS / DESCONOCIDO]
- esquema de versionado actual del proyecto (si existe): [URI PATH / HEADER / QUERY PARAM / NINGUNO]
- SLA o acuerdos de soporte vigentes: [SI EXISTEN]

Pasos:

1. CLASIFICA EL CAMBIO
   Determina si el cambio es breaking o no-breaking respecto al contrato actual.
   Ejemplos de breaking: eliminar/renombrar un campo, cambiar un tipo de dato, endurecer
   validación, cambiar el mecanismo de autenticación, cambiar un código de estado esperado,
   cambiar el orden o la semántica de una operación.
   Ejemplos de no-breaking: agregar un campo opcional, agregar un endpoint nuevo, relajar
   una validación, agregar un valor nuevo a un enum ya tolerado como abierto.
   Si hay duda razonable, trata el cambio como breaking.

2. ELIGE Y JUSTIFICA EL ESQUEMA DE VERSIONADO
   Evalúa las opciones en el contexto de esta API específica y justifica la elegida:
   - versionado en la URI (/v1/, /v2/)
   - versionado por header (Accept-Version, X-API-Version)
   - versionado por query param
   - content negotiation (media type versionado)
   Si el proyecto ya tiene un esquema establecido, úsalo salvo justificación explícita para cambiarlo.

3. DEFINE EL CALENDARIO DE DEPRECACIÓN
   Con hitos concretos (fecha o "días desde el anuncio"):
   - fecha de anuncio de la nueva versión / deprecación de la anterior
   - inicio de la ventana de soporte dual (ambas versiones activas)
   - fecha de "sunset" (fin de soporte de la versión vieja)
   - duración mínima de la ventana de soporte dual, justificada según el tipo de consumidor
     (una API pública de terceros requiere más tiempo que un servicio interno del mismo equipo)

4. DEFINE COMPATIBILIDAD HACIA ATRÁS Y VIABILIDAD DE UN ADAPTADOR
   - qué significa "compatible hacia atrás" para este cambio específico
   - si es viable evitar el breaking change por completo con un adaptador/shim
     (mapeo de campos, valor por defecto, capa de traducción) en lugar de una nueva versión mayor
   - si el adaptador introduce deuda técnica, indícalo y con qué fecha de retiro

5. REDACTA EL AVISO DE DEPRECACIÓN Y LA ENTRADA DE CHANGELOG
   - texto del aviso de deprecación (para changelog, README de la API o encabezado HTTP
     `Deprecation` / `Sunset` según RFC 8594 si aplica)
   - guía de migración: qué debe cambiar el consumidor, con ejemplo de request/response
     antes y después

6. IDENTIFICA CONSUMIDORES Y CANALES DE COMUNICACIÓN
   - lista de consumidores conocidos y su criticidad
   - si no hay forma de identificarlos (API pública sin registro de clientes), decláralo
     explícitamente y no asumas bajo impacto
   - canales de aviso: email, changelog público, banner en documentación, header HTTP,
     notificación in-app, issue/PR a los repos consumidores conocidos

7. DEFINE MONITOREO DE USO DE LA VERSIÓN VIEJA
   - métrica o log a instrumentar para medir tráfico a la versión deprecada
   - umbral de tráfico residual que se considera "seguro para retirar"
   - qué hacer si al llegar la fecha de sunset todavía hay tráfico significativo
     (extender ventana vs. retirar de todas formas, y quién decide)

8. RESUME RIESGOS Y DECISIÓN FINAL
   - riesgo residual de seguir el calendario propuesto
   - condiciones bajo las que este plan debería re-evaluarse

Restricciones:
- nunca elimines o marques como retirada una versión sin un período mínimo de aviso
  apropiado a la base de consumidores de esta API (mayor para consumidores externos
  o desconocidos que para servicios internos del mismo equipo)
- nunca propongas romper un contrato en silencio: todo breaking change requiere un
  incremento de versión mayor o una señal explícita de breaking change
- si los consumidores o su volumen de uso son desconocidos, dilo explícitamente en la
  salida en vez de asumir bajo impacto o baja criticidad
- este prompt diseña la estrategia; no modifica código de la API, configuración de
  gateway/infraestructura ni ejecuta despliegues

Entrega:
- clasificación del cambio (breaking / no-breaking) con justificación
- esquema de versionado elegido y justificación
- calendario de deprecación con hitos (ver `## Salida esperada`)
- definición de compatibilidad hacia atrás y evaluación de adaptador/shim
- texto del aviso de deprecación y guía de migración con ejemplos antes/después
- lista de consumidores identificados (o declaración explícita de que se desconocen) y canales de comunicación
- plan de monitoreo de uso de la versión vieja durante la ventana de sunset
```

---

## Uso con fórmula estándar

```text
Usa el prompt de versionado y deprecación de API y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA ACTUAL]
- ambiente: [DEV / QA / PROD]
- componentes: [API / ENDPOINT(S) AFECTADOS]
- documentos a revisar: especificación OpenAPI/GraphQL, changelog previo, documentación de consumidores, ADRs relacionados
- objetivo puntual de salida: estrategia de versionado y calendario de deprecación con guía de migración
- nivel de profundidad: alto
```

---

## Salida esperada

| Cambio | Tipo (breaking/no-breaking) | Versión nueva | Fecha de anuncio | Fin de soporte dual (sunset) | Acción del consumidor |
|---|---|---|---|---|---|
| Renombrar `user_id` a `userId` en `GET /v1/orders` y cambiar autenticación de API key a OAuth2 | breaking | v2 (`/v2/orders`, header `Accept-Version: 2`) | 2026-07-15 | 2026-10-15 (90 días de soporte dual) | Migrar clientes a `/v2/orders`, actualizar parsing del campo `userId` y reemplazar la API key por un flujo OAuth2 client_credentials antes del 2026-10-15; ver guía de migración en el changelog |

### Ejemplo de aviso de deprecación (changelog / header HTTP)

```http
Deprecation: version="1", date="2026-07-15"
Sunset: date="2026-10-15"
Link: <https://docs.example.com/migracion-v2>; rel="deprecation"
```

### Antes / después (ejemplo de migración)

```json
// v1 (deprecada, retiro 2026-10-15)
{
  "user_id": "abc123",
  "order_total": 49.90
}
```

```json
// v2 (vigente)
{
  "userId": "abc123",
  "orderTotal": 49.90
}
```
