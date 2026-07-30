# 10.6 — Materiales de capacitación y plan de rollout para usuarios finales

## Descripción

Prompt para diseñar los materiales de capacitación y el plan de comunicación de rollout dirigidos a **usuarios finales** de un sistema o funcionalidad nueva: guías, formato de capacitación según el perfil de audiencia, calendario de comunicación, estrategia de soporte reforzado durante el lanzamiento, y métrica de adopción. Distinto de `17-01-onboarding-tecnico`, que es exclusivamente para ingenieros nuevos que se incorporan al equipo, no para usuarios finales del producto.

**Cuándo usarlo:** antes de lanzar una funcionalidad o sistema nuevo a sus usuarios finales no técnicos, especialmente si implica un cambio de flujo de trabajo existente o afecta a un grupo grande de usuarios.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | medio — una capacitación insuficiente o un rollout mal comunicado puede generar resistencia a la adopción, tickets de soporte evitables, o uso incorrecto de una funcionalidad crítica de negocio; el prompt no envía comunicaciones reales ni ejecuta el rollout |
| Entradas requeridas | descripción de la funcionalidad o sistema a lanzar, audiencia de usuarios finales (roles, nivel técnico, tamaño del grupo), canal de comunicación disponible, fecha de lanzamiento |
| Herramientas permitidas | lectura de documentación del producto — sin ejecutar nada ni enviar ninguna comunicación real |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si no se conoce el nivel técnico o el tamaño de la audiencia, detente y solicítalo antes de proponer el formato de capacitación — un video corto y una guía escrita no sirven igual para 5 usuarios expertos que para 500 usuarios no técnicos |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada material propuesto declara la audiencia objetivo y el formato elegido con su razón; el plan de rollout declara fecha, canal y responsable de cada comunicación |
| Siguiente prompt recomendado | `17-06-reporte-estado-stakeholders` para comunicar el avance del rollout a stakeholders internos |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Diseña los materiales de capacitación y el plan de comunicación de rollout para los usuarios finales de la funcionalidad o sistema descrito, con estrategia de soporte durante el lanzamiento y métrica de adopción.

Entradas:
- funcionalidad o sistema a lanzar: [DESCRIPCIÓN]
- audiencia de usuarios finales: [ROLES, NIVEL TÉCNICO, TAMAÑO APROXIMADO DEL GRUPO]
- canal de comunicación disponible: [EMAIL, IN-APP, REUNIÓN EN VIVO, INTRANET, U OTRO]
- fecha de lanzamiento: [FECHA O VENTANA APROXIMADA]

Actividades:
1. PERFIL DE AUDIENCIA
   Describe quiénes son los usuarios finales, su nivel técnico, y qué les preocupa o qué resistencia es esperable ante este cambio (ej. temor a perder un flujo conocido, curva de aprendizaje, cambio de responsabilidades).

2. MATERIALES DE CAPACITACIÓN
   Propón el formato de capacitación (guía escrita paso a paso, video corto, FAQ, sesión en vivo) según el perfil de audiencia — nunca elijas un formato por defecto sin justificarlo contra ese perfil.

3. PLAN DE COMUNICACIÓN DE ROLLOUT
   Define qué se comunica, en qué momento (antes/durante/después del lanzamiento), por qué canal, y quién es responsable de cada mensaje — un calendario concreto, no una intención genérica.

4. ESTRATEGIA DE SOPORTE DURANTE EL ROLLOUT
   Define el canal de dudas durante la ventana de lanzamiento, quién responde, y si se requiere una ventana de soporte reforzado (más capacidad de respuesta de lo normal) dado el impacto del cambio.

5. PLAN DE COMUNICACIÓN DE ROLLBACK
   Si el lanzamiento se retrasa o se revierte, define qué se comunica a los usuarios finales y en qué momento — no dejes este escenario sin plan.

6. MÉTRICA DE ADOPCIÓN
   Define cómo se medirá si los usuarios finales realmente adoptaron el cambio (uso real de la nueva funcionalidad), no solo si recibieron la comunicación.

Restricciones:
- no asumas el mismo formato de capacitación para audiencias con perfiles técnicos distintos sin justificar la elección contra el perfil descrito,
- todo plan de comunicación debe declarar responsable y canal para cada mensaje — nunca dejarlo implícito o "se comunicará después",
- si el sistema o funcionalidad tiene impacto en un flujo crítico de negocio, la estrategia de soporte reforzado durante el rollout es obligatoria, no opcional — señala explícitamente si falta esa capacidad,
- este prompt no envía ninguna comunicación real ni ejecuta el rollout — produce los materiales y el plan para que el equipo los ejecute.

Salida:
0. Bloque JSON de metadatos (claves: status, audience_profile, materials_count, confidence_score [0.0 a 1.0]).
1. Perfil de audiencia y resistencia esperada.
2. Materiales de capacitación propuestos, con formato y justificación por audiencia.
3. Plan de comunicación de rollout (calendario con canal y responsable).
4. Estrategia de soporte reforzado durante el rollout.
5. Plan de comunicación de rollback, si aplica.
6. Métrica de adopción propuesta.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de materiales de capacitación y rollout y adáptalo a:
- repositorio/proyecto: [NOMBRE O URL]
- funcionalidad o sistema a lanzar: [DESCRIPCIÓN]
- audiencia de usuarios finales: [ROLES Y NIVEL TÉCNICO]
- documentos a revisar: documentación del producto, comunicaciones previas de lanzamientos similares si existen
- objetivo puntual de salida: materiales de capacitación y plan de rollout completo
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con el resumen del plan |
| Perfil de audiencia (1) | Roles, nivel técnico y resistencia esperada |
| Materiales de capacitación (2) | Formato propuesto por audiencia, con justificación |
| Plan de rollout (3) | Calendario de comunicación con canal y responsable |
| Soporte durante rollout (4) | Canal de dudas y ventana de refuerzo si aplica |
| Plan de rollback (5) | Comunicación en caso de retraso o reversión |
| Métrica de adopción (6) | Cómo se medirá el uso real, no solo el aviso |

### Ejemplo (fragmento)

```json
{
  "status": "plan_definido",
  "audience_profile": "300 usuarios internos de ventas, nivel técnico bajo-medio",
  "materials_count": 3,
  "confidence_score": 0.77
}
```

| Sección | Ejemplo de contenido |
|---|---|
| Materiales de capacitación (2) | Guía escrita de 1 página con capturas de pantalla (formato preferido por perfil de baja disponibilidad de tiempo) + video de 3 minutos para quienes prefieren ver el flujo antes de usarlo — se descarta sesión en vivo obligatoria por el tamaño del grupo (300 personas, inviable coordinar) |
| Métrica de adopción (6) | % de usuarios que completan al menos una acción con la nueva funcionalidad en los primeros 14 días post-lanzamiento, medido vía el evento de analítica ya instrumentado `feature_used:new_dashboard` — objetivo: 60% de adopción a 2 semanas |
