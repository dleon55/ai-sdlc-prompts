# 9.6 — Coordinación de breaking changes con equipos externos

## Descripción

Prompt para coordinar la comunicación de un breaking change ya decidido con los equipos, servicios y consumidores externos que dependen del contrato afectado: identifica a quién impacta, redacta el mensaje (qué cambia, por qué, cronograma, ruta de migración), elige el canal y la vía de escalamiento por audiencia, y hace seguimiento de la confirmación de preparación de cada consumidor antes de que el cambio salga a producción. No diseña el cambio técnico ni la estrategia de versionado — coordina su salida hacia afuera.

**Cuándo usarlo:** cuando un cambio rompe (o puede romper) un contrato del que dependen otros equipos, servicios o consumidores externos, y hace falta coordinar la comunicación de salida antes de desplegar, no solo el diseño técnico del cambio. Este prompt es distinto de `06-03-coordinacion-programa-multiagente`: aquel coordina una flota de agentes IA trabajando en paralelo DENTRO de un mismo programa de desarrollo; este coordina la COMUNICACIÓN HACIA AFUERA, a equipos y consumidores que no forman parte de ese programa y que pueden no usar agentes IA en absoluto. También es distinto — y posterior — a `04-05-versionado-deprecacion-api`: aquel diseña la estrategia de versionado y el calendario de deprecación del contrato (qué es breaking, ventanas de compatibilidad, hitos de fecha); este ejecuta la notificación real a cada afectado y el seguimiento de su preparación una vez que ese plan ya existe.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | operación/coordinación — redacta la comunicación y hace seguimiento de la preparación de los consumidores; no ejecuta el breaking change en sí ni la estrategia de versionado que lo respalda |
| Riesgo esperado | medio-alto — si los consumidores no son notificados correctamente o no reciben tiempo suficiente de migración, el breaking change les provoca caídas reales cuando se despliegue; prevenir exactamente eso es el objetivo de este prompt |
| Entradas requeridas | plan de versionado/deprecación ya definido (de `04-05-versionado-deprecacion-api` u otro documento equivalente), lista conocida de equipos/servicios/consumidores que dependen del contrato, fecha objetivo del corte o release, canales de comunicación disponibles por audiencia |
| Herramientas permitidas | lectura de documentación de consumidores, contratos de API/esquemas/eventos, changelogs previos, tickets de soporte y canales de comunicación existentes; redacción de comunicados, calendario de aviso y checklist de seguimiento — no envía mensajes reales, no modifica ningún sistema consumidor ni ejecuta el corte |
| Autonomía permitida | A1 — Proponer (redacta la comunicación, el calendario de aviso y el checklist de preparación; el envío real de la comunicación, la escalación directa a un consumidor y la decisión de proceder con el corte requieren aprobación humana o del equipo responsable) |
| Criterios de detención | detener y escalar si no puede confirmarse la lista completa de consumidores afectados — declararla incompleta en vez de tratarla como cerrada; detener si no hay fecha mínima de aviso definida por audiencia; nunca recomendar proceder con el corte si un consumidor de alto impacto no ha confirmado explícitamente su preparación |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada consumidor/equipo listado con impacto, canal usado, fecha límite y estado de confirmación citando la fuente concreta (mensaje enviado, respuesta recibida, ticket, ack en canal); nota explícita cuando la lista de consumidores es incompleta o no verificable |
| Siguiente prompt recomendado | `09-04-promotion-checklist` una vez confirmada la preparación externa, para ejecutar el checklist de despliegue real del cambio |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Coordina la comunicación de este breaking change con todos los equipos, servicios y consumidores externos afectados, y haz seguimiento de su preparación hasta confirmar que están listos antes de la fecha del corte.

Inputs requeridos:
- cambio y plan de versionado/deprecación de referencia: [REFERENCIA A 04-05 U OTRO DOCUMENTO]
- contrato afectado: [API / ESQUEMA / EVENTO / FORMATO DE ARCHIVO / OTRO]
- naturaleza del breaking change: [QUÉ CAMBIA EXACTAMENTE]
- fecha objetivo del corte o release: [FECHA]
- consumidores conocidos hasta ahora: [LISTA, O "DESCONOCIDA / PARCIAL"]
- canales de comunicación disponibles: [SLACK INTERNO / CHANGELOG PÚBLICO / EMAIL / ACCOUNT MANAGER / STATUS PAGE / OTRO]

Pasos:
1. Identifica cada equipo, servicio o consumidor externo que depende del contrato que se va a romper, a partir de fuentes verificables (logs de uso de API, registros de suscriptores, documentación de integración, tickets de soporte previos, contratos comerciales). No asumas que la lista inicial provista está completa: señala explícitamente qué parte de la base de consumidores no puedes verificar con las fuentes disponibles.
2. Clasifica a cada equipo/consumidor identificado por severidad de impacto (crítico / alto / medio / bajo, según qué tan central es el contrato roto para su operación) y por dificultad de migración estimada (trivial / moderada / compleja), distinguiendo consumidores internos de externos y, entre los externos, clientes con contrato comercial de integraciones informales.
3. Redacta la comunicación base: qué cambia exactamente, por qué se hace el cambio, el cronograma completo (fecha de aviso, ventana de convivencia si existe, fecha de corte), los pasos concretos de migración con ejemplos de antes/después si aplica, y a quién contactar con preguntas. Evita lenguaje ambiguo sobre fechas ("próximamente", "en las próximas semanas") — usa fechas exactas.
4. Elige el canal y la vía de escalamiento apropiados por audiencia: un canal interno de Slack o un comentario en el issue puede bastar para un equipo interno; un consumidor externo grande o con contrato comercial requiere contacto directo (account manager, email dedicado) además de cualquier aviso general (changelog público, status page); no dependas de un único canal para audiencias de alto impacto.
5. Define el período mínimo de aviso apropiado para cada audiencia, no un único plazo genérico: los equipos internos con acceso directo al código y visibilidad de la migración suelen necesitar menos tiempo de anticipación que consumidores externos que dependen de sus propios ciclos de release. Si se conoce la capacidad de migración declarada por un consumidor específico, ese es el piso, no una referencia opcional.
6. Diseña un mecanismo concreto de seguimiento de confirmación por consumidor (checklist con estado individual, formulario de ack, respuesta requerida en el ticket, etc.) — "se envió el correo" no es evidencia de que un consumidor está listo; necesitas una confirmación explícita de su parte o evidencia técnica de que ya migró.
7. Define qué ocurre con cada consumidor que no confirme preparación antes de la fecha límite: corte duro igualmente, extensión puntual del plazo, o excepción por consumidor (por ejemplo, mantener el contrato viejo activo solo para ese cliente por tiempo limitado) — la decisión y su costo deben quedar explícitos, no implícitos.
8. Prepara una plantilla de comunicación de pausa o rollback para usar si el corte debe posponerse después de haber sido anunciado, de forma que no se tenga que improvisar esa comunicación bajo presión si aparece un bloqueo de último momento.

Restricciones:
- nunca asumas que el silencio equivale a confirmación de preparación — una notificación no leída, o sin respuesta, no es evidencia de que el consumidor está listo,
- nunca definas una fecha límite más corta que la capacidad de migración declarada por la audiencia, si esa información está disponible — negociar un plazo más corto requiere acuerdo explícito de esa audiencia, no una decisión unilateral,
- este prompt redacta la comunicación y hace seguimiento de la preparación; no ejecuta el breaking change, no despliega el cambio ni modifica ningún sistema del consumidor,
- si no puedes verificar la lista completa de consumidores afectados, dilo explícitamente en la entrega en vez de presentar una lista parcial como si fuera completa,
- no marques a un consumidor como "listo" por inferencia (por ejemplo, porque "seguramente ya lo vieron") — solo por confirmación explícita de su parte o evidencia técnica verificable de migración.

Entrega:
- lista de equipos/servicios/consumidores identificados, con impacto, dificultad de migración y fuente que respalda cada dato, incluyendo la nota explícita de qué parte de la base no pudo verificarse,
- comunicación redactada (qué cambia, por qué, cronograma, pasos de migración, contacto de dudas), adaptada por audiencia si el contenido difiere sustancialmente,
- canal y vía de escalamiento asignados por audiencia,
- fecha límite de aviso por audiencia, justificando por qué ese plazo es suficiente,
- mecanismo de seguimiento de confirmación y tabla de estado por consumidor (ver `## Salida esperada`),
- plan de manejo para consumidores no listos a la fecha límite (corte / extensión / excepción),
- plantilla de comunicación de pausa o rollback lista para usar si el corte se pospone.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de coordinación de breaking changes y adáptalo a:
- repositorio: [NOMBRE O URL]
- cambio o plan de versionado de referencia: [REFERENCIA A ISSUE/PR/04-05]
- contrato afectado: [API / ESQUEMA / EVENTO / OTRO]
- consumidores conocidos: [LISTA, O "PARCIAL/DESCONOCIDA"]
- fecha objetivo del corte: [FECHA]
- documentos a revisar: plan de versionado y deprecación, changelog, documentación de integración de consumidores, tickets de soporte previos
- objetivo puntual de salida: comunicación redactada por audiencia + tabla de seguimiento de confirmación de preparación
- nivel de profundidad: alto
```

---

## Salida esperada

| Consumidor/Equipo | Impacto | Dificultad de migración | Canal | Fecha límite | Estado de confirmación |
|---|---|---|---|---|---|
| Equipo de Pagos (interno) | Alto — consume el endpoint `/v1/orders` directamente en el flujo de checkout | Moderada — requiere actualizar el cliente HTTP interno | Slack #eng-pagos + comentario en issue #512 | 2026-07-25 | 🟢 Confirmado — ack en Slack el 2026-07-14, PR de migración abierto |
| Cliente externo ACME Corp (contrato comercial) | Crítico — integración batch nocturna sobre el mismo endpoint | Compleja — su ciclo de release es mensual | Account manager (contacto directo) + email a soporte@acme | 2026-08-15 | 🟡 En espera — email enviado 2026-07-12, sin respuesta aún |
| Consumidores anónimos vía API pública | Desconocido — no hay registro de API keys por consumidor en este contrato legado | No estimable | Changelog público + banner en status page | 2026-08-15 (mismo corte que ACME, como piso mínimo) | 🔴 No verificable — base de consumidores no identificable con las fuentes actuales; se declara explícitamente como riesgo abierto |
| Equipo de Reporting (interno) | Bajo — usa un campo derivado que no cambia de forma directa | Trivial | Comentario en issue #512 | 2026-07-20 | 🟢 Confirmado — sin acción requerida de su parte |
