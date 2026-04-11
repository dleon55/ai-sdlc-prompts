# 5.2 — Análisis de riesgos e impacto de implementación

## Descripción

Prompt para identificar y clasificar los riesgos de implementación: funcionales, técnicos, de datos, seguridad, operación, concurrencia de agentes, integración y despliegue. Genera una matriz de riesgos con probabilidad, impacto y plan de mitigación.

**Cuándo usarlo:** en paralelo al plan de implementación (`05-01`), antes de ejecutar cualquier cambio.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Identifica y analiza los riesgos de implementación y el impacto potencial del cambio en otros módulos, procesos, servicios, pipelines, integraciones y usuarios.

Clasifica riesgos por:
- funcional,
- técnico,
- datos,
- seguridad,
- operación,
- concurrencia de agentes,
- integración,
- despliegue.

Entrega:
- matriz de riesgos,
- probabilidad,
- impacto,
- mitigación,
- contingencia.
```

---

## Uso con fórmula estándar

```text
Usa el prompt de análisis de riesgos de implementación y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA OBJETIVO]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES A MODIFICAR]
- documentos a revisar: diseño aprobado, arquitectura, historial de incidentes
- objetivo puntual de salida: matriz de riesgos completa con plan de mitigación
- nivel de profundidad: alto
```

---

## Salida esperada

| Riesgo | Categoría | Probabilidad | Impacto | Mitigación | Contingencia |
|---|---|---|---|---|---|
