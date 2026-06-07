# 2.3 — Análisis de impacto cruzado

## Descripción

Prompt para evaluar el impacto del cambio en todos los módulos, procesos, datos, integraciones, ambientes y pipelines del sistema. Detecta impactos directos e indirectos y genera una matriz de severidad.

**Cuándo usarlo:** después del análisis técnico profundo (`02-02`) y antes del diseño de la solución (`04-01`).

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza el impacto del cambio solicitado en otros módulos, procesos, datos, integraciones, ambientes, pipelines, subproyectos del monorepo y políticas de versionado (semver).

Actividades:
1. Evalúa impacto en:
   - subproyectos / workspaces del monorepo (por ejemplo, dependencias compartidas, utilerías comunes),
   - contratos de API y versionado semántico (semver) de paquetes locales,
   - frontend,
   - backend,
   - base de datos,
   - integraciones,
   - infraestructura,
   - CI/CD (pipelines de build independientes o compartidos),
   - seguridad y conformidad normativa (ISO, MAAGTICSI, etc.),
   - monitoreo,
   - documentación.
2. Detecta impactos directos e indirectos.
3. Evalúa afectación a otros casos de uso.

Salida:
- matriz de impacto (incluyendo workspaces y paquetes del monorepo),
- severidad,
- componente/workspace afectado,
- tipo de impacto (directo/indirecto, ruptura de retrocompatibilidad),
- riesgo,
- recomendación de mitigación.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de análisis de impacto cruzado y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA ACTUAL]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: arquitectura, contratos API, esquema de BD
- objetivo puntual de salida: matriz de impacto cruzado con severidad por componente
- nivel de profundidad: alto
```

---

## Salida esperada

| Componente | Tipo de impacto | Severidad | Riesgo | Recomendación |
|---|---|---|---|---|
| frontend | | | | |
| backend | | | | |
| base de datos | | | | |
| integraciones | | | | |
| infraestructura | | | | |
| CI/CD | | | | |
| seguridad | | | | |
| monitoreo | | | | |
| documentación | | | | |
