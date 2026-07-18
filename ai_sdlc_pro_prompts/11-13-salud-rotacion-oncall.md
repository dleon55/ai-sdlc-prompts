# 11.13 — Auditoría de salud de rotación on-call

## Descripción

Prompt para auditar la salud de un esquema de guardia (on-call) ya en operación: distribución real de pages/alertas por persona (horario laboral, nocturno, fin de semana), equidad frente al esquema de rotación configurado, correlación con señales de fatiga o rotación de personal, y recomendación de rebalanceo — sin ejecutar cambios en el esquema. Distinto de `17-04-reporte-capacidad-equipo` (capacidad de backlog comprometido vs. disponibilidad) y de `11-04-incident-response` (ejecución de un incidente puntual).

**Cuándo usarlo:** periódicamente como salud del esquema de guardia, o cuando el equipo reporta fatiga, quejas de inequidad en la rotación, o señales de alta rotación de personal en roles con guardia.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | bajo — el prompt solo analiza y recomienda; no modifica el esquema de guardia ni reasigna turnos. El riesgo es que un esquema de guardia inequitativo no detectado a tiempo contribuya a burnout o rotación de personal, que sí tiene costo real |
| Entradas requeridas | historial de pages/alertas del periodo (quién recibió, timestamp, franja horaria), esquema de rotación configurado (quién está de guardia cuándo), periodo a evaluar, señales cualitativas de burnout o quejas si existen (opcional) |
| Herramientas permitidas | lectura del historial de pages, el esquema de rotación configurado y, si existen, encuestas o señales de clima del equipo; no modifica el esquema de guardia ni reasigna turnos — produce el análisis y recomendación |
| Autonomía permitida | A0 — Analizar (distribución real de pages, equidad de la rotación); A1 — Proponer (recomendación de rebalanceo); nunca A2/A3 — el cambio real del esquema de guardia requiere decisión y ejecución humana del lead o manager responsable |
| Criterios de detención | detener si el historial de pages no distingue horario laboral de nocturno/fin de semana — no asumir que todos los pages tienen el mismo costo de fatiga; detener si el esquema de rotación configurado no está disponible, no inferir turnos a partir del historial de pages únicamente |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada persona en la tabla de distribución cita el conteo real de pages por franja horaria; toda afirmación de inequidad se compara contra la distribución esperada según el esquema de rotación configurado, no contra un promedio arbitrario |
| Siguiente prompt recomendado | `17-04-reporte-capacidad-equipo` si la sobrecarga de guardia coincide con sobrecarga general de backlog; `11-12-auditoria-ruido-alertas` si gran parte del volumen de pages resulta ser ruido más que incidentes reales |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Audita la salud del esquema de guardia (on-call) en el periodo indicado: distribución real de pages por persona y franja horaria, equidad frente al esquema de rotación configurado, y correlación con señales de fatiga o rotación de personal, con recomendaciones de rebalanceo.

Entradas:
- historial de pages del periodo: [PEGAR O ENLACE — quién recibió, timestamp, alerta asociada]
- esquema de rotación configurado: [PEGAR O ENLACE — quién está de guardia cuándo]
- periodo a evaluar: [ej. ÚLTIMO TRIMESTRE]
- señales cualitativas de burnout/quejas: [PEGAR SI EXISTEN O "ninguna reportada"]
- horario laboral estándar del equipo: [ej. L-V 9-18, ZONA HORARIA]

Pasos:
1. DISTRIBUCIÓN REAL DE PAGES POR PERSONA
   Para cada persona en el esquema de rotación, cuenta el total de pages recibidos en el periodo, desglosado por franja horaria: horario laboral, nocturno (fuera del horario laboral estándar) y fin de semana. Un page fuera de horario laboral no tiene el mismo costo de fatiga que uno en horario laboral — nunca los agregues sin distinguirlos.

2. COMPARACIÓN CONTRA LA ROTACIÓN ESPERADA
   Compara la distribución real de pages contra lo que el esquema de rotación configurado predeciría (si cada quien está de guardia una fracción similar del tiempo, ¿reciben una fracción similar de pages, o algunas personas concentran desproporcionadamente más por la naturaleza de su especialidad o por errores en la configuración del esquema?).

3. IDENTIFICACIÓN DE INEQUIDAD
   Señala explícitamente si alguna persona recibe una proporción de pages nocturnos/fin de semana notablemente mayor a su proporción de tiempo de guardia — y si es así, si se debe a la configuración del esquema (turnos mal distribuidos) o a que su especialidad concentra más incidentes reales (lo cual apunta a un problema distinto: bus factor o necesidad de entrenar respaldo, no solo de rotación).

4. CORRELACIÓN CON SEÑALES DE FATIGA
   Si hay señales cualitativas disponibles (encuestas, quejas, comentarios en retrospectivas), relaciona el volumen o franja horaria de pages recibidos por persona con esas señales. Si no hay señales cualitativas disponibles, decláralo explícitamente y limita el análisis a los datos cuantitativos — no infieras burnout sin evidencia.

5. TENDENCIA EN EL TIEMPO
   Si hay datos de más de un periodo, señala si la carga de guardia está aumentando, estable o disminuyendo, y si coincide con algún evento conocido (crecimiento de usuarios, incidente prolongado, cambio de arquitectura).

6. RECOMENDACIONES DE REBALANCEO
   Propone al menos una opción concreta para cada inequidad identificada: redistribuir turnos nocturnos/fin de semana de forma más pareja, agregar una persona más a la rotación si la carga total es alta para el tamaño del equipo, o entrenar respaldo si la concentración se debe a especialización y no a mala configuración del esquema. Indica el tradeoff aproximado de cada opción.

Restricciones:
- nunca combines pages de horario laboral con pages nocturnos/fin de semana en una sola cifra sin desglosarlos — tienen costo de fatiga distinto y ocultar la distinción esconde la inequidad real,
- no infieras burnout o insatisfacción sin señal cualitativa que lo respalde — si solo hay datos cuantitativos de pages, limita las conclusiones a la distribución de carga, no al estado emocional del equipo,
- este prompt analiza y recomienda; nunca reasigna turnos, nunca modifica el esquema de rotación ni ejecuta ningún cambio — eso requiere decisión y ejecución humana del lead o manager responsable,
- si el esquema de rotación configurado no está disponible, detente y solicítalo — no infieras los turnos esperados únicamente a partir del historial de pages, que puede no reflejar la rotación planeada si hubo cambios manuales no registrados.

Salida:
- tabla de distribución: persona, pages en horario laboral, pages nocturnos, pages fin de semana, % del total
- comparación contra la rotación esperada, con inequidades señaladas explícitamente
- correlación con señales de fatiga, si hay datos (o su ausencia declarada)
- tendencia en el tiempo, si hay datos de más de un periodo
- recomendaciones de rebalanceo priorizadas, con tradeoff de cada una
```

---

## Uso con fórmula estándar

```text
Usa el prompt de auditoría de salud de rotación on-call y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- historial de pages: [ENLACE AL HISTORIAL DEL PERIODO]
- esquema de rotación: [ENLACE A LA CONFIGURACIÓN DE GUARDIAS]
- periodo a evaluar: [ÚLTIMO TRIMESTRE]
- señales cualitativas: [PEGAR SI EXISTEN O "ninguna reportada"]
- horario laboral estándar: [L-V 9-18, ZONA HORARIA]
- documentos a revisar: historial de pages, esquema de rotación
- objetivo puntual de salida: distribución de carga de guardia con recomendaciones de rebalanceo
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Distribución de pages | Persona, pages por franja horaria, % del total |
| Comparación vs. rotación esperada | Inequidades señaladas explícitamente |
| Correlación con fatiga | Relación con señales cualitativas, o su ausencia declarada |
| Tendencia | Evolución de la carga si hay más de un periodo de datos |
| Recomendaciones | Rebalanceo priorizado, con tradeoff de cada opción |

### Ejemplo (fragmento)

| Persona | Pages laborales | Pages nocturnos | Pages fin de semana | % del total |
|---|---|---|---|---|
| Ana Torres | 8 | 14 | 6 | 38% (guardia = 25% del tiempo del equipo) |
| Luis Ramírez | 6 | 3 | 2 | 17% (guardia = 25% del tiempo del equipo) |

**Inequidad identificada:** Ana Torres recibe 38% del total de pages pese a estar de guardia el 25% del tiempo — concentra el doble de pages nocturnos que el resto del equipo. La causa no es un error de configuración del esquema (los turnos están distribuidos parejo); Ana es la única con conocimiento profundo del módulo de pagos, que genera la mayoría de los incidentes nocturnos. **Recomendación:** esto es un problema de bus factor, no solo de rotación — entrenar a un segundo respaldo en el módulo de pagos antes de rebalancear turnos, ya que redistribuir el turno sin resolver el conocimiento concentrado solo trasladaría el problema a otra persona sin contexto para resolverlo.
