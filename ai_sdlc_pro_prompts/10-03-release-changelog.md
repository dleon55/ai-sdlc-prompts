# 10.3 — Documentación de release o changelog

## Descripción

Prompt para redactar las notas de release o changelog de un cambio con enfoque técnico y funcional: resumen, módulos impactados, correcciones, mejoras, riesgos y consideraciones de despliegue.

**Cuándo usarlo:** al preparar un release o al cerrar un sprint para documentar cambios entregados.

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
