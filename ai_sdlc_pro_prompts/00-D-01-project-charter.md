# 0-D.1 — Project Charter: Definición formal de proyecto nuevo

## Descripción

Prompt para generar el **Project Charter** de un proyecto nuevo: el documento fundacional que establece el porqué, el qué, el quién y el cómo de alto nivel, autorizado por el patrocinador y aceptado por el equipo antes de iniciar cualquier esfuerzo técnico.

**Cuándo usarlo:** al inicio de un proyecto nuevo, al formalizar un proyecto que comenzó sin documentación, o al actualizar el alcance después de un cambio estratégico significativo.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Genera el Project Charter completo para formalizar el inicio de este proyecto.

Inputs requeridos:
- nombre del proyecto: [NOMBRE]
- tipo de proyecto: [producto nuevo / mejora de sistema existente / migración / integración / plataforma interna / otro]
- patrocinador / sponsor: [ROL O NOMBRE]
- cliente o usuario final: [INTERNO / EXTERNO — descripción breve]
- contexto o necesidad de negocio: [PROBLEMA O OPORTUNIDAD QUE ORIGINA EL PROYECTO]
- stack tecnológico preliminar: [framework, lenguaje, base de datos, infra — puede ser tentativo]
- restricciones conocidas: [presupuesto, plazos regulatorios, tecnología obligatoria, equipo fijo, etc.]
- supuestos clave: [qué debe ser verdad para que el proyecto tenga éxito]

Entrega los siguientes apartados del Project Charter:

1. DESCRIPCIÓN DEL PROYECTO
   - nombre formal y código interno (si aplica)
   - resumen ejecutivo de una página: qué es, por qué existe, qué problema resuelve
   - tipo de proyecto y categoría estratégica

2. OBJETIVOS Y BENEFICIOS ESPERADOS
   - objetivo principal (SMART: Específico, Medible, Alcanzable, Relevante, Temporal)
   - objetivos secundarios (máx. 4)
   - beneficios cuantificables esperados: reducción de tiempo, ahorro, incremento de ingresos, etc.
   - KPIs de éxito del proyecto (no del producto — medir avance y entrega)

3. ALCANCE
   - IN SCOPE: lista de funcionalidades, integraciones o entregables incluidos
   - OUT OF SCOPE: lista explícita de lo que NO está incluido (evita scope creep)
   - supuestos de alcance: qué condiciones deben cumplirse para mantener el alcance definido

4. STAKEHOLDERS Y EQUIPO
   Tabla con columnas: Nombre/Rol | Tipo (Sponsor / Propietario / Equipo / Usuario / IA agent) | Responsabilidad principal | Nivel de autorización

5. ENTREGABLES Y CRITERIOS DE ACEPTACIÓN
   Tabla con columnas: Entregable | Descripción breve | Criterio de aceptación | Responsable | Fecha estimada

6. HITOS PRINCIPALES (MILESTONE PLAN)
   Tabla con columnas: Hito | Descripción | Criterio de cierre | Fecha objetivo
   (incluye al menos: Kickoff, Diseño aprobado, MVP/primera entrega, UAT, Go-live, Cierre)

7. PRESUPUESTO Y RECURSOS
   - estimación de esfuerzo por rol (persona/día o semanas)
   - recursos de infraestructura requeridos (cloud, licencias, herramientas)
   - fondos aprobados o por aprobar (indicar si es estimación preliminar)
   - modelo de contratación si aplica: fijo / time & material / mixto

8. RIESGOS INICIALES
   Tabla con columnas: Riesgo | Probabilidad (A/M/B) | Impacto (A/M/B) | Strategy (evitar / mitigar / aceptar / transferir) | Responsable

9. RESTRICCIONES Y DEPENDENCIAS
   - restricciones técnicas (versión de plataforma, API de terceros, compliance, etc.)
   - restricciones organizativas (equipo, presupuesto, ventanas de cambio)
   - dependencias externas: proyectos paralelos, proveedores, decisiones pendientes

10. STACK TECNOLÓGICO INICIAL
    Tabla con columnas: Capa | Tecnología seleccionada o candidata | Estado (confirmado / tentativo) | Justificación breve
    (si se requiere un análisis detallado de arquitectura, usar el prompt 00-D-02)

11. MODELO DE GOBIERNO Y CONTROL DE CAMBIOS
    - frecuencia de reportes de avance
    - proceso para solicitar cambios de alcance (quién aprueba, cómo se documenta)
    - herramienta de seguimiento de issues y tareas: [GitHub Issues / Jira / Linear / otro]
    - repositorio(s) oficial(es) del proyecto

12. FIRMAS Y APROBACIÓN
    Tabla con columnas: Rol | Nombre | Firma / Confirmación | Fecha
    (sponsor, project manager / líder técnico, cliente si es externo)

Formato de salida:
- Documento estructurado con todos los apartados anteriores
- Tablas en Markdown donde se indican
- Lenguaje formal pero técnicamente preciso
- Señala con [PENDIENTE: razón] cualquier dato que deba ser confirmado antes de firmar el charter
```

---

## Notas de uso

- Este prompt genera el **documento fundacional** del proyecto; no sustituye al diseño técnico detallado (usar `04-01-diseno-solucion.md`) ni al plan de implementación (`05-01-plan-implementacion.md`).
- Para el análisis y selección detallada del stack tecnológico, continúa con el prompt **`00-D-02-stack-arquitectura-inicial.md`**.
- Para generar la estructura del repositorio a partir de este charter, usa **`00-B-01-scaffolding-repositorio.md`**.
- Mantén el Project Charter en el repositorio bajo `docs/project-charter.md` o `docs/00-project-charter/` para trazabilidad.
