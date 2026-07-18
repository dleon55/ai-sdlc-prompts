# 16.1 — Triage y clasificación de tickets de soporte

## Descripción

Prompt para triar y clasificar un ticket o lote de tickets de soporte entrante: determina severidad/prioridad con evidencia, calcula el SLA aplicable según la política vigente, identifica si el ticket es un duplicado o un problema ya conocido, y propone el equipo/responsable de primera asignación. No diagnostica la causa raíz ni resuelve el ticket, no cambia su estado, no lo reasigna ni notifica al cliente: solo clasifica y enruta con evidencia trazable.

**Cuándo usarlo:** al recibir uno o varios tickets nuevos (soporte, mesa de ayuda, canal de incidentes de cliente) que necesitan severidad, SLA y equipo asignados antes de que alguien intervenga. Diferencia con prompts relacionados: este prompt (`16-01`) solo clasifica y enruta, nunca interviene sobre el ticket; `16-02-diagnostico-respuesta-incidente-soporte` es el prompt que sí interviene después del triage — diagnostica la causa, propone o ejecuta una respuesta al ticket ya clasificado por este prompt. Si el resultado de este triage indica severidad crítica con indicios de incidente de producción más amplio, considera además `11-04-incident-response` para la coordinación del incidente.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis/clasificación |
| Riesgo esperado | medio — una severidad o SLA mal calculados pueden retrasar la atención de un ticket crítico o saturar al equipo equivocado con falsos positivos, pero el triage no aplica cambios al sistema, solo clasifica y enruta; el riesgo se materializa únicamente si la clasificación propuesta se usa sin revisión humana para decidir la atención real |
| Entradas requeridas | texto y metadatos del ticket o lote de tickets (título, descripción, reportante, timestamp, entorno, adjuntos/logs si existen), tabla o política de SLA vigente por severidad, acceso de lectura al historial de tickets o base de conocimiento para detectar duplicados/problemas conocidos, reglas de enrutamiento o estructura de equipos de soporte |
| Herramientas permitidas | lectura y búsqueda en el sistema de tickets, base de conocimiento e historial de incidentes previos; la salida es una clasificación y propuesta de enrutamiento en texto/tabla — no cambia el estado del ticket, no lo asigna, no lo cierra ni envía comunicaciones al cliente o al equipo |
| Autonomía permitida | A0 — Analizar (lectura del ticket, búsqueda de duplicados/conocidos); A1 — Proponer (severidad, SLA y equipo propuestos); nunca A2/A3 — este prompt no asigna el ticket, no cambia su estado ni ejecuta ninguna acción sobre el sistema de tickets |
| Criterios de detención | detener y pedir más información si el ticket no tiene datos suficientes para determinar severidad (sin descripción, sin impacto ni entorno indicado) — no inventar una severidad plausible; marcar como "posible duplicado, no confirmado" si la coincidencia con un ticket previo no es clara, en vez de darlo por cerrado; si el ticket contiene indicios de incidente de seguridad o fuga de datos, detener el triage rutinario y escalar de inmediato según el protocolo de seguridad vigente en vez de continuar clasificando como ticket ordinario |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada severidad/prioridad cita el/los campo(s) del ticket o criterio de la matriz de impacto/urgencia que la sustenta; cada SLA citado referencia la política o tabla de SLA usada; cada marca de duplicado/conocido cita el ID del ticket o entrada de base de conocimiento coincidente y el criterio de coincidencia (mismo error, mismo componente, mismo usuario/entorno, etc.) |
| Siguiente prompt recomendado | `16-02-diagnostico-respuesta-incidente-soporte` para diagnosticar la causa y responder/resolver el ticket ya clasificado; `11-04-incident-response` si el triage revela un incidente de producción de alcance mayor al de un ticket individual |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como Analista de Soporte especializado en triage. Clasifica el ticket o lote de tickets indicado por severidad/prioridad, determina el SLA aplicable según la política vigente, identifica si es un duplicado o un problema ya conocido, y propone el equipo o responsable de primera asignación. No diagnostiques la causa raíz, no resuelvas el ticket, no cambies su estado ni lo asignes realmente: tu salida es una clasificación propuesta con evidencia, para revisión humana o del siguiente prompt del flujo.

Entradas:
- ticket(s) a clasificar: [TEXTO/EXPORT DEL TICKET O LOTE DE TICKETS — título, descripción, reportante, timestamp, entorno, adjuntos/logs si existen]
- política de SLA vigente: [TABLA DE SLA POR SEVERIDAD/PRIORIDAD — tiempos de primera respuesta y resolución por nivel]
- fuente para detectar duplicados/conocidos: [HISTORIAL DE TICKETS, BASE DE CONOCIMIENTO, LISTA DE PROBLEMAS CONOCIDOS — o "no disponible" si aplica]
- reglas de enrutamiento/estructura de equipos: [MAPA DE EQUIPOS POR COMPONENTE/PRODUCTO/ÁREA, O CRITERIO DE ASIGNACIÓN VIGENTE]
- canal de origen del ticket: [EMAIL / PORTAL DE SOPORTE / CHAT / API / OTRO]

Pasos:

1. INGESTA Y NORMALIZACIÓN
   Para cada ticket, extrae los campos relevantes (título, descripción, componente/producto afectado, entorno, usuario/cliente afectado, timestamp de reporte, adjuntos o logs referenciados). Si un campo crítico falta, indícalo explícitamente en vez de asumirlo.

2. VERIFICACIÓN DE INDICIOS DE SEGURIDAD
   Antes de invertir esfuerzo en la clasificación estándar, verifica si el ticket contiene indicios de incidente de seguridad o exposición de datos (credenciales expuestas, acceso no autorizado reportado, fuga de datos sospechada). Si los hay, detén el triage rutinario de ese ticket de inmediato y márcalo para escalamiento de seguridad en vez de continuar con los pasos siguientes.

3. CLASIFICACIÓN DE SEVERIDAD/PRIORIDAD
   Determina la severidad (ej: crítica/alta/media/baja) y prioridad usando una matriz de impacto x urgencia explícita: impacto (cuántos usuarios/clientes afectados, si hay pérdida de datos o de ingreso, si hay bloqueo total vs. degradación) y urgencia (si existe workaround, si empeora con el tiempo). Cita el campo o indicio concreto del ticket que sustenta cada nivel asignado — nunca asignes severidad sin evidencia textual del ticket.

4. DETERMINACIÓN DEL SLA APLICABLE
   A partir de la severidad/prioridad asignada, aplica la política de SLA vigente para determinar el tiempo de primera respuesta y de resolución objetivo. Si la política de SLA no cubre el caso o no fue provista, indícalo explícitamente en vez de inventar un SLA.

5. DETECCIÓN DE DUPLICADO O PROBLEMA CONOCIDO
   Busca en el historial de tickets o base de conocimiento provista si existe un ticket previo o un problema conocido que coincida (mismo error/mensaje, mismo componente, mismo entorno o patrón). Si encuentras una coincidencia razonable, cita el ID del ticket/entrada coincidente y el criterio de coincidencia. Si la coincidencia es parcial o incierta, márcalo como "posible duplicado, no confirmado" — nunca lo declares duplicado confirmado sin evidencia clara.

6. PROPUESTA DE EQUIPO/RESPONSABLE DE PRIMERA ASIGNACIÓN
   Según el componente/producto afectado y las reglas de enrutamiento provistas, propone el equipo o responsable que debería recibir el ticket en primera instancia. Si las reglas de enrutamiento no cubren el componente identificado, señálalo como "sin regla de enrutamiento definida" en vez de asignar un equipo por defecto sin justificación.

7. SEÑALIZACIÓN DE CASOS AMBIGUOS O INCOMPLETOS
   Lista aparte los tickets donde falte información suficiente para clasificar con confianza (severidad, SLA o equipo), y qué información específica falta para completar el triage.

8. RESUMEN EJECUTIVO Y TABLA CONSOLIDADA
   Resume el lote clasificado: cuántos tickets por severidad, cuántos duplicados/conocidos detectados, cuántos con información insuficiente, y cuántos escalados por indicios de seguridad.

Restricciones:
- este prompt solo clasifica y enruta; nunca cambia el estado del ticket, no lo asigna realmente, no lo cierra, no genera ni envía respuestas al cliente ni al equipo de soporte.
- nunca asignes severidad, SLA o equipo sin citar la evidencia concreta (campo del ticket, entrada de la política de SLA, o regla de enrutamiento) que sustenta la decisión.
- nunca declares un ticket como duplicado confirmado sin una coincidencia clara y citada; ante duda, usa "posible duplicado, no confirmado".
- si falta información crítica para clasificar un ticket (severidad, entorno, impacto), indícalo explícitamente y no fabriques una clasificación plausible para completar la tabla.
- si el ticket contiene indicios de incidente de seguridad o fuga de datos, detén el triage rutinario y escala de inmediato según el protocolo de seguridad vigente; no lo trates como un ticket de soporte ordinario.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de triage y clasificación de tickets de soporte y adáptalo a:
- repositorio/producto: [NOMBRE O URL]
- ticket(s) a clasificar: [EXPORT O PEGADO DEL TICKET/LOTE]
- política de SLA vigente: [TABLA DE SLA POR SEVERIDAD]
- fuente de duplicados/conocidos: [HISTORIAL DE TICKETS / BASE DE CONOCIMIENTO O "no disponible"]
- reglas de enrutamiento: [MAPA DE EQUIPOS POR COMPONENTE]
- canal de origen: [EMAIL / PORTAL / CHAT / API]
- objetivo puntual de salida: severidad, SLA, duplicado/conocido y equipo propuesto por ticket
- nivel de profundidad: medio
```

---

## Salida esperada

| Ticket ID | Severidad/Prioridad | SLA aplicable | ¿Duplicado/Conocido? | Equipo propuesto | Evidencia/Justificación |
|---|---|---|---|---|---|
| TCK-4821 | Alta (impacto: ~200 usuarios no pueden iniciar sesión; urgencia: sin workaround reportado) | Primera respuesta 1h, resolución 8h (política SLA nivel "Alta") | Posible duplicado de TCK-4790 (mismo componente "auth-service", mismo mensaje de error "token expirado prematuramente") — no confirmado, requiere revisión humana | Equipo Plataforma/Auth (regla: componente auth-service → Plataforma) | Descripción del ticket indica bloqueo total de login desde las 09:14; sin workaround mencionado; coincidencia parcial de mensaje de error con TCK-4790 |

> Nota: la tabla completa debe incluir una fila por cada ticket del lote, y una sección separada para tickets con información insuficiente (listando el dato faltante) y para tickets escalados por indicios de seguridad (con el motivo del escalamiento, sin detallar la vulnerabilidad en un canal no seguro).

### Resumen ejecutivo

- **Tickets clasificados:** [N] — [X críticos, Y altos, Z medios, W bajos].
- **Duplicados/conocidos detectados:** [N] — [lista de IDs coincidentes, con nivel de confianza confirmado/no confirmado].
- **Tickets con información insuficiente:** [N] — [dato faltante por ticket].
- **Tickets escalados por indicios de seguridad:** [N] — [motivo del escalamiento, sin exponer detalles sensibles].
- **Siguiente acción recomendada:** enviar los tickets clasificados a `16-02-diagnostico-respuesta-incidente-soporte` para diagnóstico y respuesta, priorizando por severidad y SLA.
</content>
