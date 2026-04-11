# 12 — Prompt maestro orquestador del ciclo completo

## Descripción

Prompt que coordina la totalidad del ciclo de ingeniería de software para una asignación: desde la comprensión del repositorio hasta la documentación final, pasando por análisis, diseño, implementación, pruebas e integración.

**Cuándo usarlo:** para asignaciones completas que requieren pasar por todas las fases, o cuando se trabaja con un agente que debe operar de forma autónoma sobre un issue de principio a fin.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Coordina el ciclo completo de ingeniería de software para esta asignación dentro del repositorio.

Entrada:
- issue/requerimiento/incidente: [PEGAR]
- rama objetivo: [INDICAR]
- ambiente: [INDICAR]
- componentes: [INDICAR]

Quiero que trabajes por fases:

Fase 1. Comprensión e inventario
- revisar documentación, procesos, políticas y estructura del repo.

Fase 2. Análisis
- funcional,
- técnico,
- impacto,
- riesgos,
- concurrencia con otros agentes.

Fase 3. Diseño
- solución funcional,
- solución técnica,
- casos de uso,
- diagramas mermaid,
- plan de implementación.

Fase 4. Ejecución controlada
- propuesta de cambios por archivo,
- estrategia de commits,
- validaciones.

Fase 5. Calidad
- pruebas unitarias,
- integración,
- E2E,
- humo,
- automatización navegador,
- revisión estática.

Fase 6. Integración
- ramas,
- CI local,
- GitHub Actions,
- riesgos de integración.

Fase 7. Documentación
- memoria técnica,
- actualización documental,
- release notes.

Formato de salida obligatorio:
1. Resumen ejecutivo
2. Hallazgos
3. Riesgos
4. Diseño propuesto
5. Plan de implementación
6. Estrategia de pruebas
7. Estrategia de integración
8. Documentación requerida
9. Recomendación final
```

---

## Uso con fórmula estándar

```text
Usa el prompt maestro orquestador y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [PEGAR TEXTO COMPLETO]
- rama objetivo: [RAMA DESTINO]
- ambiente: [DEV / QA / STAGING / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: README, docs/, arquitectura, workflows, issues relacionados
- objetivo puntual de salida: ciclo completo documentado listo para ejecución
- nivel de profundidad: alto
```

---

## Fases y entregables esperados

| Fase | Nombre | Entregable |
|---|---|---|
| 1 | Comprensión e inventario | Inventario técnico + mapa de gobierno |
| 2 | Análisis | Análisis funcional + técnico + impacto cruzado |
| 3 | Diseño | Diseño completo + diagramas + casos de uso |
| 4 | Ejecución controlada | Propuesta de cambios + commits atómicos |
| 5 | Calidad | Suite de pruebas + revisión estática |
| 6 | Integración | Estrategia de ramas + estado CI |
| 7 | Documentación | Memoria técnica + release notes |
