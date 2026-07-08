# 10.3 — Documentación de release o changelog

## Descripción

Prompt para redactar las notas de release o changelog de un cambio con enfoque técnico y funcional: resumen, módulos impactados, correcciones, mejoras, riesgos y consideraciones de despliegue.

**Cuándo usarlo:** al preparar un release o al cerrar un sprint para documentar cambios entregados.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo — documento de comunicación de un release; el riesgo es reputacional/operativo si omite breaking changes o notas de despliegue, no ejecuta acciones sobre el sistema |
| Entradas requeridas | versión o tag, rama de release, issues o PRs incluidos, commits del período |
| Herramientas permitidas | solo lectura (historial de commits, PRs mergeados, issues cerrados); no publica el release ni crea el tag |
| Autonomía permitida | A1 — Proponer: entrega el changelog listo para publicar; la publicación efectiva en GitHub Releases o CHANGELOG.md es una acción A3 separada y explícita |
| Criterios de detención | si detecta cambios que rompen compatibilidad sin nota de migración clara, debe detenerse y solicitar esa información antes de dar el changelog por completo |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada entrada del changelog es trazable a un commit o PR real dentro del período declarado |
| Siguiente prompt recomendado | `10-02-memoria-tecnica` si aún no existe el registro de auditoría del cambio; `09-04-promotion-checklist` para validar que el release está listo para promoción |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Redacta las notas de release o changelog del cambio con enfoque técnico y funcional.

Incluye:
- resumen del cambio,
- módulos impactados,
- correcciones,
- mejoras,
- riesgos,
- consideraciones de despliegue,
- notas de compatibilidad.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de release/changelog y adáptalo a:
- repositorio: [NOMBRE O URL]
- versión: [TAG O VERSIÓN]
- rama: [RAMA DE RELEASE]
- issues incluidos: [LISTA DE ISSUES O PRs]
- documentos a revisar: commits del período, PRs mergeados, issues cerrados
- objetivo puntual de salida: changelog listo para publicar en GitHub Releases o CHANGELOG.md
- nivel de profundidad: medio
```

---

## Salida esperada

### Encabezado

```
## [vX.X.X] - YYYY-MM-DD
```

### Secciones del changelog

| Sección | Contenido |
|---|---|
| Resumen | Descripción ejecutiva del release |
| Correcciones (fixes) | Bugs y defectos corregidos |
| Mejoras (features) | Funcionalidades nuevas o mejoradas |
| Módulos impactados | Lista de módulos con cambios |
| Riesgos | Riesgos conocidos en esta versión |
| Notas de despliegue | Pasos especiales, migraciones, variables nuevas |
| Compatibilidad | Cambios que rompen compatibilidad (breaking changes) |
