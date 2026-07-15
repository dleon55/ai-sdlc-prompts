# 16.2 — Diagnóstico y primera respuesta a incidente de soporte

## Descripción

Prompt para guiar el diagnóstico sistemático de un ticket de soporte ya triado: reproducir el problema, aislar la causa probable, revisar incidentes conocidos y artículos de base de conocimiento (KB), y clasificar el hallazgo. A partir de ese diagnóstico, redacta la primera respuesta al usuario o cliente con los próximos pasos y una expectativa de tiempo realista. No aplica ningún fix en producción ni modifica código o configuración: es diagnóstico y comunicación.

**Cuándo usarlo:** inmediatamente después de que un ticket fue clasificado y priorizado por `16-01-triage-tickets-soporte`. Diferencia con prompts relacionados: `16-01-triage-tickets-soporte` decide **qué** ticket atender primero y con qué severidad, sin investigar la causa; este prompt investiga **por qué** ocurre el problema y comunica el estado al usuario, sin tocar producción. Si el diagnóstico confirma que se trata de un bug real que requiere cambio de código, este prompt se detiene y escala a `03-01-incidentes-github` o `11-01-troubleshooting` para la investigación técnica de ejecución; si el ticket resulta ser un incidente de producción con impacto significativo, escala a `11-04-incident-response` en su lugar.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis/comunicación |
| Riesgo esperado | medio — un diagnóstico apresurado o una respuesta al cliente mal calibrada (promesa de tiempo no realista, tono inadecuado, causa mal comunicada) puede dañar la relación con el cliente o comprometer una expectativa de SLA, aunque el prompt en sí no aplica cambios al sistema |
| Entradas requeridas | ticket ya triado con prioridad y severidad asignadas (salida de `16-01`), pasos de reproducción reportados por el usuario, entorno afectado, evidencia disponible (logs, capturas, mensajes de error), acceso de lectura a incidentes conocidos y artículos de KB, SLA o tiempo de respuesta acordado con el cliente |
| Herramientas permitidas | lectura de logs, dashboards de monitoreo, historial de incidentes y base de conocimiento; redacción de la respuesta al usuario — prohibido aplicar cambios de código, configuración, despliegues, rollbacks o cualquier modificación en el sistema o en producción |
| Autonomía permitida | A0 — Analizar (diagnóstico: reproducir, aislar causa probable, revisar KB); A1 — Proponer (redactar la primera respuesta al usuario); nunca A2/A3 — este prompt no ejecuta ni publica cambios en el sistema |
| Criterios de detención | detener y escalar a un prompt de ejecución/ingeniería (`03-01-incidentes-github` o `11-01-troubleshooting`) si el diagnóstico confirma un bug de código que requiere cambio; detener y escalar a `11-04-incident-response` si se trata de un incidente de producción con impacto significativo; si el problema no es reproducible con la evidencia disponible, no prometer causa ni fecha de resolución — marcar el diagnóstico como de baja confianza y pedir más evidencia al usuario |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada hipótesis de causa cita la evidencia real que la respalda (log, paso de reproducción, artículo de KB o incidente previo referenciado); la primera respuesta al usuario nunca promete una fecha de resolución que no esté respaldada por el SLA acordado o por una estimación explícita marcada como tal |
| Siguiente prompt recomendado | `16-01-triage-tickets-soporte` (paso previo, si aún no se ha triado el ticket); `03-01-incidentes-github` u `11-01-troubleshooting` si el diagnóstico confirma un bug real que requiere cambio de código; `11-04-incident-response` si escala a incidente de producción con impacto significativo |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como Especialista de Soporte Técnico L2 responsable del diagnóstico de incidentes ya triados. Reproduce el problema reportado, aísla la causa más probable con evidencia real, revisa incidentes conocidos y la base de conocimiento, y redacta la primera respuesta al usuario con próximos pasos y una expectativa de tiempo realista. No apliques ningún cambio en el sistema.

Entradas:
- ticket triado: [ID DEL TICKET, PRIORIDAD Y SEVERIDAD ASIGNADAS EN 16-01]
- síntoma reportado por el usuario: [DESCRIPCIÓN TAL COMO LA ESCRIBIÓ EL USUARIO/CLIENTE]
- pasos de reproducción reportados: [PASOS, O "no proporcionados" SI APLICA]
- entorno afectado: [PRODUCCIÓN / STAGING / VERSIÓN DE APP / NAVEGADOR / DISPOSITIVO]
- evidencia disponible: [LOGS, CAPTURAS DE PANTALLA, MENSAJES DE ERROR, ID DE TRANSACCIÓN — o "ninguna" si aplica]
- fuentes de conocimiento a revisar: [BASE DE KB, HISTORIAL DE INCIDENTES SIMILARES, CHANGELOG RECIENTE]
- SLA o tiempo de respuesta acordado con el cliente: [ej: PRIMERA RESPUESTA EN 4H / RESOLUCIÓN EN 2 DÍAS HÁBILES]

Pasos:

1. CONFIRMAR CONTEXTO DEL TICKET TRIADO
   Verifica que el ticket cuenta con prioridad y severidad ya asignadas. Si no las tiene, indícalo explícitamente y recomienda pasar primero por el triage (`16-01-triage-tickets-soporte`) antes de continuar.

2. INTENTO DE REPRODUCCIÓN
   Con los pasos de reproducción reportados y el entorno indicado, intenta reproducir el problema (o describe con precisión qué se necesitaría para reproducirlo si no puedes ejecutarlo directamente). Documenta el resultado: reproducido / no reproducido / reproducido parcialmente, con la evidencia obtenida en cada intento.

3. REVISIÓN DE CONOCIDOS Y BASE DE CONOCIMIENTO (KB)
   Busca en el historial de incidentes y en la KB si existe un caso igual o similar ya documentado. Si existe, cita la referencia exacta (ID de incidente o artículo de KB) y su solución o workaround conocido.

4. AISLAMIENTO DE LA CAUSA PROBABLE
   A partir de la reproducción, los logs disponibles y los conocidos revisados, formula una o varias hipótesis de causa probable, cada una respaldada por evidencia concreta (no especules sin evidencia). Ordena las hipótesis de más a menos probable.

5. CLASIFICACIÓN DEL DIAGNÓSTICO
   Clasifica el hallazgo en una de estas categorías: (a) bug de código confirmado — requiere cambio de código, (b) problema de configuración o datos — puede resolverse sin cambio de código, (c) error de uso del usuario — requiere solo explicación, (d) duplicado de un incidente ya conocido con workaround existente, (e) no reproducible — se necesita más evidencia.

6. DECISIÓN DE ESCALAMIENTO
   Si la clasificación es (a) bug de código confirmado, señala explícitamente que este prompt se detiene aquí y que el diagnóstico debe pasar a un prompt de ejecución/ingeniería (`03-01-incidentes-github` o `11-01-troubleshooting`) para implementar el fix. Si el entorno es PRODUCCIÓN y el impacto es significativo (afecta a múltiples usuarios o una función crítica), señala que corresponde escalar a `11-04-incident-response` en lugar de continuar como ticket de soporte estándar.

7. PRIMERA RESPUESTA AL USUARIO/CLIENTE
   Redacta la primera respuesta dirigida al usuario o cliente, en tono profesional y empático, que incluya: (1) confirmación de que el problema fue entendido y está siendo investigado, (2) un resumen del hallazgo en lenguaje no técnico apropiado para el destinatario, (3) el próximo paso concreto (workaround si existe, o la escalación planeada), (4) una expectativa de tiempo alineada con el SLA acordado o marcada explícitamente como estimación si no hay SLA formal.

8. RESUMEN EJECUTIVO INTERNO
   Resume para el equipo interno: clasificación del diagnóstico, evidencia clave, decisión de escalamiento (si aplica) y el compromiso de tiempo comunicado al usuario.

Restricciones:
- nunca apliques, sugieras aplicar de forma automática, ni ejecutes un cambio de código, configuración, despliegue o rollback en ningún ambiente — este prompt diagnostica y comunica, no repara.
- nunca prometas al usuario una causa raíz confirmada ni una fecha de resolución que no esté respaldada por evidencia real o por el SLA acordado; si el diagnóstico es de baja confianza, dilo explícitamente en la respuesta al usuario en vez de sonar más seguro de lo que la evidencia permite.
- si el problema no pudo reproducirse con la evidencia disponible, no asumas una causa: pide al usuario la evidencia adicional específica que falta (logs, pasos exactos, capturas) en la primera respuesta.
- si la clasificación indica bug de código confirmado, detén el flujo de este prompt en el paso de escalamiento — no continúes proponiendo o describiendo el fix de código como si fuera parte de este prompt.
- distingue siempre en la salida qué es evidencia real (log, KB, reproducción) de qué es hipótesis sin confirmar.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de diagnóstico y primera respuesta a incidente de soporte y adáptalo a:
- repositorio/producto: [NOMBRE O URL]
- ticket triado: [ID, PRIORIDAD, SEVERIDAD — salida de 16-01]
- síntoma reportado: [DESCRIPCIÓN DEL USUARIO]
- entorno afectado: [PRODUCCIÓN / STAGING / VERSIÓN]
- evidencia disponible: [LOGS / CAPTURAS / "ninguna"]
- SLA acordado: [ej: primera respuesta en 4h]
- documentos a revisar: base de conocimiento (KB), historial de incidentes similares, changelog reciente
- objetivo puntual de salida: diagnóstico clasificado con evidencia y borrador de primera respuesta al usuario
- nivel de profundidad: medio
```

---

## Salida esperada

| Paso | Resultado | Evidencia citada | Clasificación |
|---|---|---|---|
| Reproducción | Reproducido en staging siguiendo los pasos del usuario, error 500 al confirmar checkout con cupón vencido | log de aplicación `req_id=8841af`, captura adjunta por el usuario | reproducido |
| Causa probable | La validación de cupones no verifica la fecha de expiración antes de aplicar el descuento en el paso de confirmación | log de aplicación + comparación con commit reciente en el módulo de cupones (changelog) | bug de código confirmado |
| Conocidos/KB | No existe incidente previo idéntico; existe artículo de KB sobre cupones inválidos que no cubre este caso | búsqueda en KB (sin resultado exacto) | no aplica workaround conocido |
| Decisión de escalamiento | Se detiene el diagnóstico aquí; requiere cambio de código en el módulo de validación de cupones | clasificación (a) | escalar a `03-01-incidentes-github` / `11-01-troubleshooting` |

> Nota: la tabla completa debe incluir una fila por cada paso relevante del diagnóstico (reproducción, KB, causa probable, clasificación, decisión de escalamiento), citando siempre la evidencia real usada. Si algún paso no cuenta con evidencia suficiente, la fila correspondiente debe decir explícitamente "sin evidencia — diagnóstico de baja confianza" en vez de inventar una causa.

### Borrador de primera respuesta al usuario

> Hola [NOMBRE DEL USUARIO], gracias por reportarlo. Confirmamos el error al aplicar un cupón vencido durante el checkout y ya identificamos la causa en nuestro sistema de validación de cupones. Nuestro equipo de ingeniería está trabajando en la corrección. Como próximo paso, te recomendamos completar la compra sin el cupón mientras resolvemos el problema, o contactarnos para aplicar el descuento manualmente. Esperamos tener una actualización antes de [PLAZO SEGÚN SLA ACORDADO O ESTIMACIÓN EXPLÍCITA]. Te avisaremos apenas esté resuelto.

### Resumen ejecutivo

- **Diagnóstico:** [CLASIFICACIÓN] — [RESUMEN DE UNA LÍNEA DE LA CAUSA PROBABLE].
- **Evidencia clave:** [LOGS / REPRODUCCIÓN / KB CITADOS].
- **Decisión de escalamiento:** [NINGUNA / ESCALA A 03-01 O 11-01 / ESCALA A 11-04-INCIDENT-RESPONSE].
- **Compromiso comunicado al usuario:** [PRÓXIMO PASO Y PLAZO], alineado con el SLA acordado: [SÍ / NO — SI NO, MARCADO COMO ESTIMACIÓN].
- **Riesgos residuales:** [diagnóstico no reproducible, evidencia insuficiente, SLA en riesgo de incumplimiento].
