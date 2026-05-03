# 11.7 — Post-Mortem Blameless y Generación de Runbook (SRE)

## Descripción

Prompt diseñado para adoptar la cultura SRE (Site Reliability Engineering). Toma los datos crudos de un incidente resuelto (logs, chat de slack, métricas) y genera un documento Post-Mortem "sin culpa" (Blameless), identificando la verdadera causa raíz y extrayendo un Runbook automatizable para mitigar futuros incidentes similares.

**Cuándo usarlo:** Inmediatamente después de haber resuelto un incidente crítico o caída en producción (Fase 03 finalizada), para documentar el aprendizaje institucional.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.
> Adjunta el resultado del análisis de causa raíz (`03-02`) si está disponible.

---

## Prompt completo

```text
Objetivo:
Actúa como un Site Reliability Engineer (SRE). Redacta un documento Post-Mortem Blameless (sin culpa) basado en los datos del incidente proporcionado, y genera un Runbook accionable para el equipo de guardia (On-Call).

Entradas:
- datos_incidente: [PEGA AQUÍ TIMELINES, LOGS, O RESUMEN DEL INCIDENTE]
- resolucion_aplicada: [CÓMO SE SOLUCIONÓ EL PROBLEMA]

Actividades de Análisis:
1. TIMELINE DE INCIDENTE: Reconstruye cronológicamente el evento (Detección, Triaje, Mitigación, Resolución).
2. ANÁLISIS BLAMELESS: Identifica fallas en el sistema, la observabilidad o los procesos, NUNCA en las personas ("El sistema permitió que un push directo rompiera producción" en lugar de "Juan rompió producción").
3. CAUSA RAÍZ (5 Whys): Ejecuta los 5 porqués para llegar al defecto estructural subyacente.
4. DISEÑO DE RUNBOOK: Crea pasos deterministas para que un ingeniero on-call mitigador (o un bot) resuelva esto en el futuro.

Salida Obligatoria:
1. POST-MORTEM DOCUMENT: Estructurado con: Impacto al usuario, Línea de tiempo, Causa Raíz y Action Items (tickets preventivos).
2. ON-CALL RUNBOOK: Instrucciones paso a paso (comandos de terminal, queries, dashboards a mirar) para mitigar si vuelve a ocurrir.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de post-mortem SRE y adáptalo a:
- datos_incidente: [TEXTO DEL INCIDENTE]
- resolucion_aplicada: [TEXTO]
- objetivo puntual de salida: generar documento institucional post-mortem y playbook on-call.
- nivel de profundidad: exhaustivo
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Post-Mortem | Documento SRE estándar (Impacto, Timeline, 5 Whys, Action Items) |
| Enfoque Blameless | Lenguaje que audita procesos y sistemas, no individuos |
| Runbook | Comandos ejecutables y comprobaciones para On-Call |
