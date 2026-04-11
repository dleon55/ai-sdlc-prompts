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
Analiza el impacto del cambio solicitado en otros módulos, procesos, datos, integraciones, ambientes y pipelines.

Actividades:
1. Evalúa impacto en:
   - frontend,
   - backend,
   - base de datos,
   - integraciones,
   - infraestructura,
   - CI/CD,
   - seguridad,
   - monitoreo,
   - documentación.
2. Detecta impactos directos e indirectos.
3. Evalúa afectación a otros casos de uso.

Salida:
- matriz de impacto,
- severidad,
- componente afectado,
- tipo de impacto,
- riesgo,
- recomendación.
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
