# 16.4 — Matriz de escalamiento y SLA por severidad

## Descripción

Prompt para definir la matriz de política de soporte de un producto/equipo: niveles de severidad (P0-P3 o el esquema equivalente que use el equipo), el SLA de primera respuesta y de resolución por nivel, y la cadena de escalamiento explícita — a quién escalar y después de cuánto tiempo sin cumplir el SLA. No clasifica tickets individuales ni redacta respuestas a un incidente real: produce el documento de política que otros prompts de la operación día a día usan como referencia.

**Cuándo usarlo:** al establecer por primera vez la política de soporte de un producto/equipo, o al revisarla periódicamente (cambio de capacidad del equipo, nuevos SLAs contractuales, incidentes recientes que revelaron huecos en la cadena de escalamiento). Diferencia con prompts relacionados: `16-01-triage-tickets-soporte` clasifica tickets entrantes reales contra los niveles de severidad ya definidos aquí — este prompt diseña esos niveles, no los aplica. `16-02-diagnostico-respuesta-incidente-soporte` diagnostica y responde a un incidente concreto ya en curso, usando el SLA de esta matriz como el reloj contra el que debe operar — este prompt no diagnostica ni responde incidentes, solo fija las reglas del juego antes de que ocurran.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | diseño de política/proceso |
| Riesgo esperado | medio — una matriz de SLA mal calibrada genera expectativas incumplibles frente a clientes/usuarios y compromete al equipo de soporte con plazos que no puede sostener con su capacidad real, pero el prompt en sí solo redacta una propuesta de política, nunca la publica ni la aplica a un ticket real |
| Entradas requeridas | catálogo de tipos de incidentes/tickets conocidos (si existe), capacidad real del equipo de soporte (headcount, horario de cobertura, existencia de on-call), SLAs contractuales ya vigentes con clientes (si aplica), definiciones de severidad usadas actualmente (aunque sean informales), canales de escalamiento disponibles |
| Herramientas permitidas | lectura de documentación de soporte existente, contratos/SLAs con clientes, organigrama del equipo y esquemas de guardia (on-call); la salida es un documento de política en texto — no configura herramientas de alertas/paging ni modifica el sistema de ticketing |
| Autonomía permitida | A0 — Analizar (relevar SLAs y capacidad existentes); A1 — Proponer (la matriz de severidad, SLA y cadena de escalamiento); nunca A2/A3 — la matriz requiere aprobación humana explícita antes de adoptarse como política oficial de soporte |
| Criterios de detención | detener y escalar a un humano si no hay información real de capacidad del equipo (headcount, horario de cobertura) — no fabricar una matriz de SLA sin verificar que el equipo puede sostenerla; señalar como propuesta de baja confianza si existen SLAs contractuales con clientes que no pudieron confirmarse |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada nivel de severidad incluye un ejemplo concreto del tipo de incidente que lo dispara, el SLA de primera respuesta y de resolución correspondiente, y el punto exacto de la cadena de escalamiento (a quién y después de cuánto tiempo sin cumplirse el SLA) queda explícito por nivel |
| Siguiente prompt recomendado | `16-01-triage-tickets-soporte` para aplicar esta matriz clasificando tickets entrantes en la operación día a día |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Actúa como Responsable de Soporte/Confiabilidad especializado en diseño de políticas de servicio. Define una matriz de escalamiento y SLA por severidad para el producto/equipo indicado: niveles de severidad claros, el SLA de primera respuesta y de resolución por nivel, y la cadena de escalamiento con tiempos y responsables cuando el SLA no se cumple.

Entradas:
- producto/equipo de soporte: [NOMBRE DEL PRODUCTO O EQUIPO]
- catálogo de tipos de incidentes/tickets conocidos: [LISTA, o "no existe — inferir de histórico de tickets/incidentes"]
- capacidad real del equipo de soporte: [HEADCOUNT, HORARIO DE COBERTURA, ¿EXISTE ON-CALL FUERA DE HORARIO LABORAL?]
- SLAs contractuales ya vigentes con clientes: [DESCRIPCIÓN, o "ninguno"]
- definiciones de severidad usadas actualmente: [DESCRIPCIÓN, o "no existen — es la primera definición formal"]
- canales de escalamiento disponibles: [SLACK / PAGERDUTY / TELÉFONO / EMAIL / OTRO]
- número de niveles de severidad deseado: [ej: 4 NIVELES (P0-P3) / OTRO ESQUEMA]

Pasos:

1. RELEVAMIENTO DE CONTEXTO ACTUAL
   Reúne la capacidad real del equipo (headcount, horario de cobertura, existencia de guardia on-call), los SLAs contractuales ya vigentes con clientes si los hay, y cualquier definición de severidad usada hoy, aunque sea informal.
   - si la capacidad real del equipo no está disponible, indícalo explícitamente y detente en este punto: no se puede calibrar un SLA sostenible sin ese dato.

2. DEFINICIÓN DE NIVELES DE SEVERIDAD
   Define el número de niveles indicado (por defecto P0-P3 si no se especifica otro esquema), con un criterio objetivo y verificable para cada uno (ej: alcance de usuarios afectados, existencia de workaround, pérdida de datos, impacto en ingresos/reputación). Evita criterios subjetivos tipo "muy grave" sin un ancla observable.

3. SLA DE PRIMERA RESPUESTA Y RESOLUCIÓN POR NIVEL
   Para cada nivel de severidad, define el SLA de primera respuesta (tiempo hasta que un humano confirma que el ticket/incidente fue recibido y está siendo atendido) y el SLA de resolución (tiempo hasta que el incidente se considera cerrado o mitigado). Ambos deben ser tiempos concretos (ej: "15 minutos", "4 horas hábiles"), nunca rangos vagos tipo "lo antes posible".

4. CADENA DE ESCALAMIENTO POR NIVEL
   Para cada nivel, define a quién se escala si el SLA de primera respuesta o de resolución está por vencerse o ya venció, en qué canal, y quién es el siguiente responsable en la cadena (ej: ingeniero de guardia → tech lead → gerente de ingeniería → VP). Especifica el gatillo temporal exacto de cada salto de escalamiento (ej: "si no hay primera respuesta a los 10 minutos de P0, escalar automáticamente al tech lead de guardia").

5. HORARIO DE COBERTURA Y EXCEPCIONES
   Aclara si los SLA definidos aplican 24/7 o solo en horario laboral, y qué pasa con incidentes de severidad alta fuera de ese horario (activación de on-call, SLA distinto fuera de horario, etc.). No asumas cobertura 24/7 si la capacidad relevada en el paso 1 no la sostiene.

6. CRITERIOS DE RECLASIFICACIÓN
   Define cuándo y cómo se puede reclasificar la severidad de un ticket/incidente ya abierto (hacia arriba o hacia abajo), y quién tiene autoridad para hacerlo, para evitar que la severidad quede congelada en una clasificación inicial equivocada.

7. VALIDACIÓN DE VIABILIDAD CONTRA CAPACIDAD REAL
   Contrasta cada SLA propuesto contra la capacidad real relevada en el paso 1 (headcount, cobertura horaria). Si un SLA no es sostenible con la capacidad actual, señálalo explícitamente como riesgo en vez de proponerlo como si fuera viable.

8. RESUMEN EJECUTIVO Y PRÓXIMOS PASOS
   Resume la matriz completa, los riesgos de viabilidad detectados en el paso 7, y qué debe aprobar un humano antes de adoptar esta matriz como política oficial de soporte.

Restricciones:
- nunca definas un SLA de resolución o de primera respuesta sin contrastarlo contra la capacidad real del equipo (headcount, horario de cobertura); si esa capacidad no fue provista, detente y pide el dato en vez de asumir cobertura 24/7 o un equipo de tamaño no confirmado.
- cada nivel de severidad debe tener un criterio objetivo y un ejemplo concreto de incidente que lo dispara; evita definiciones subjetivas sin ancla observable.
- cada salto de la cadena de escalamiento debe tener un gatillo temporal exacto (cuánto tiempo sin cumplir el SLA) y un responsable nombrado por rol, nunca "escalar quien corresponda".
- este prompt diseña y propone una política; nunca la publica como oficial, nunca notifica a clientes del nuevo SLA, y nunca configura herramientas de alertas/paging/on-call — todo eso requiere aprobación humana explícita y ejecución fuera de este prompt.
- si existen SLAs contractuales ya vigentes con clientes, la matriz propuesta no puede proponer plazos menos favorables que esos contratos sin señalarlo explícitamente como un conflicto que debe resolver un humano.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de matriz de escalamiento y SLA por severidad y adáptalo a:
- producto/equipo de soporte: [NOMBRE DEL PRODUCTO O EQUIPO]
- catálogo de tipos de incidentes/tickets conocidos: [LISTA O "inferir de histórico"]
- capacidad real del equipo de soporte: [HEADCOUNT, HORARIO, ON-CALL SÍ/NO]
- SLAs contractuales existentes con clientes: [DESCRIPCIÓN O "ninguno"]
- definiciones de severidad usadas actualmente: [DESCRIPCIÓN O "no existen"]
- canales de escalamiento disponibles: [SLACK / PAGERDUTY / TELÉFONO / EMAIL]
- número de niveles de severidad deseado: [ej: 4 NIVELES (P0-P3)]
- documentos a revisar: contratos con clientes, organigrama de soporte, histórico de tickets/incidentes
- objetivo puntual de salida: matriz de severidad, SLA de respuesta/resolución y cadena de escalamiento lista para revisión humana
- nivel de profundidad: alto
```

---

## Salida esperada

| Nivel | Definición / ejemplo | SLA primera respuesta | SLA resolución | Cadena de escalamiento |
|---|---|---|---|---|
| P0 — Crítico | Servicio caído para todos los usuarios o pérdida de datos en curso; sin workaround (ej: caída total de producción) | 10 minutos, 24/7 | 4 horas | Ingeniero de guardia notificado automáticamente al abrirse → si no hay primera respuesta en 10 min, escala a tech lead de guardia → si no hay resolución en 2 horas, escala a gerente de ingeniería → a las 4 horas, escala a VP de Producto |
| P1 — Alto | Funcionalidad clave degradada para un subconjunto grande de usuarios; existe workaround parcial | 30 minutos, horario extendido (7am-11pm) | 8 horas hábiles | Ingeniero de soporte de turno → si no hay primera respuesta en 30 min, escala a tech lead → si no hay resolución en 6 horas, escala a gerente de ingeniería |
| P2 — Medio | Funcionalidad secundaria afectada o bug con workaround claro para un número acotado de usuarios | 4 horas hábiles | 3 días hábiles | Ingeniero de soporte de turno → si no hay primera respuesta en 4 horas, escala a tech lead |
| P3 — Bajo | Defecto cosmético, solicitud de mejora o pregunta sin impacto funcional | 1 día hábil | 10 días hábiles | Ingeniero de soporte de turno; sin escalamiento automático — se revisa en la reunión semanal de backlog de soporte |

> Nota: la tabla completa debe incluir una fila por nivel de severidad definido, señalando explícitamente cualquier SLA que el paso 7 del prompt haya marcado como no sostenible con la capacidad actual del equipo, y distinguiendo horario de cobertura 24/7 de horario laboral/extendido en cada nivel.

### Resumen ejecutivo

- **Esquema de severidad adoptado:** [ej: P0-P3, 4 niveles] — criterio principal de clasificación: [ALCANCE DE USUARIOS AFECTADOS / EXISTENCIA DE WORKAROUND / PÉRDIDA DE DATOS / OTRO].
- **Nivel con mayor riesgo de incumplimiento:** [NIVEL] — motivo: [ej: SLA de 10 minutos 24/7 requiere on-call que el equipo aún no tiene cubierto].
- **Conflictos con SLAs contractuales existentes:** [NINGUNO / DESCRIPCIÓN DEL CONFLICTO A RESOLVER].
- **Aprobación requerida antes de adoptar como política oficial:** [ROL/PERSONA] debe validar la viabilidad de capacidad y autorizar la publicación de esta matriz.
