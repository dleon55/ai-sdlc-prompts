# Auditoría de variables en prompts e interfaz

Fecha: 2026-06-07
Alcance: prompts ES/EN, `build.py`, persistencia de proyectos, preview y copiado.

## Resumen ejecutivo

El sistema tenía 12 campos persistentes, pero la biblioteca utiliza cientos de
placeholders textuales con semánticas distintas. La sustitución dependía de una
lista manual de alias y no existía un control que informara al usuario qué
valores seguían pendientes.

La principal causa de defectos era el uso de alias demasiado genéricos:
`[NOMBRE]`, `[TIPO]`, `[NIVEL]`, `[SEVERIDAD]` e `[INDICAR]`. Un mismo valor
podía reemplazar conceptos no equivalentes en diferentes prompts.

## Hechos confirmados

- Los proyectos se almacenan en `AI_SDLC_v1_projects`.
- La migración defensiva completa campos nuevos mediante `EMPTY_VARS`.
- El motor sustituía únicamente placeholders con sintaxis `[TOKEN]`.
- El preview y el copiado mantenían implementaciones de reemplazo separadas.
- El copiado sobrescribía `modulo` con el título de la tarjeta.
- `02-04` requería fuente de issues, filtro, componente y assignee sin campos
  equivalentes de calidad en el frontend.
- `02-05` requería el texto completo del requerimiento, pero lo asociaba al
  campo genérico de referencia.

## Hallazgos

| ID | Severidad | Hallazgo |
|---|---|---|
| VAR-01 | Alta | Alias genéricos podían sustituir contenido con significado incorrecto. |
| VAR-02 | Alta | Existían placeholders específicos sin forma de captura en la UI. |
| VAR-03 | Alta | El módulo capturado podía perderse durante el copiado. |
| VAR-04 | Media | No se advertían placeholders pendientes después de sustituir. |
| VAR-05 | Media | No había soporte uniforme para `{{TOKEN}}`, aunque la documentación lo prescribe. |
| VAR-06 | Media | Triage y requerimientos no usaban un vocabulario canónico común. |
| VAR-07 | Media | No existían pruebas de contrato entre esquema, UI, alias y prompts. |

## Correcciones implementadas

- Se agregaron variables canónicas:
  - `entrada`: requerimiento, listado de issues, reporte o contexto principal.
  - `objetivo`: resultado concreto esperado.
  - `responsable`: usuario, equipo, assignee o rol.
  - `adicionales`: asignaciones `TOKEN=valor`, una por línea.
- Se retiraron alias ambiguos del reemplazo automático.
- Se unificó el reemplazo de `[TOKEN]` y `{{TOKEN}}`.
- Se conserva el módulo configurado; el título solo funciona como fallback.
- Se detectan placeholders pendientes y se informa al usuario al copiar.
- Se normalizaron `02-04` y `02-05` en español e inglés.
- Se agregaron pruebas de contrato del sistema de variables.

## Supuestos

- Los valores adicionales no deben almacenar secretos ni credenciales.
- La advertencia no bloquea el copiado porque algunos placeholders representan
  ejemplos, plantillas de salida o valores que el agente debe generar.
- La compatibilidad de proyectos existentes se mantiene mediante la migración
  actual basada en `Object.assign`.

## Riesgos residuales

- La biblioteca conserva placeholders históricos no canónicos; ahora son
  configurables mediante `TOKEN=valor`, pero requieren captura manual.
- La detección heurística puede marcar algunos tokens usados como ejemplos.
- El panel crece de 12 a 16 variables y requiere validación visual en móvil.
- Los requisitos y conteos históricos del repositorio contienen datos obsoletos.

## Recomendaciones

1. Migrar gradualmente los prompts a un catálogo reducido de tokens canónicos.
2. Añadir metadatos declarativos por prompt para mostrar solo variables relevantes.
3. Incorporar una vista de “variables requeridas por este prompt”.
4. Convertir `extract_vars.py` en un gate que clasifique tokens canónicos,
   adicionales y ejemplos ignorables.
5. Añadir pruebas E2E de persistencia, preview, copiado y cambio de idioma.
