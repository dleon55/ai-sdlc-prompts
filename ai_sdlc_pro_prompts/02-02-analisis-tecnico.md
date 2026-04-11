# 2.2 — Análisis técnico profundo de código existente

## Descripción

Prompt para analizar cómo funciona realmente el código existente hoy: flujo end-to-end, acoplamientos, deuda técnica, validaciones faltantes y riesgos de regresión.

**Cuándo usarlo:** después del análisis funcional (`02-01`) y antes del análisis de impacto cruzado (`02-03`) y el diseño de la solución (`02-04`).

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza el código existente relacionado con el requerimiento o incidente y explica cómo funciona realmente hoy.

Actividades:
1. Ubica archivos, clases, funciones, endpoints, servicios, consultas, tablas y componentes UI involucrados.
2. Describe el flujo end-to-end actual.
3. Identifica:
   - acoplamientos,
   - dependencias,
   - deuda técnica,
   - validaciones faltantes,
   - riesgos de regresión,
   - problemas de diseño.
4. Señala exactamente qué archivos y módulos están involucrados.

Formato de salida:
1. Flujo actual
2. Componentes afectados
3. Archivos relevantes
4. Hallazgos técnicos
5. Riesgos de modificación
```

---

## Uso con fórmula estándar

```text
Usa el prompt de análisis técnico profundo y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA ACTUAL]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: código fuente, esquema de BD, contratos API
- objetivo puntual de salida: flujo actual documentado con hallazgos técnicos
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Flujo actual | Descripción paso a paso del comportamiento real |
| Componentes afectados | Lista de servicios, módulos y tablas |
| Archivos relevantes | Rutas exactas en el repositorio |
| Hallazgos técnicos | Deuda, acoplamientos, riesgos detectados |
| Riesgos de modificación | Qué puede romperse al cambiar |

---

## Prompt 2.2 — Análisis técnico profundo de código existente

```text
Objetivo:
Analiza el código existente relacionado con el requerimiento o incidente y explica cómo funciona realmente hoy.

Actividades:
1. Ubica archivos, clases, funciones, endpoints, servicios, consultas, tablas y componentes UI involucrados.
2. Describe el flujo end-to-end actual.
3. Identifica:
   - acoplamientos,
   - dependencias,
   - deuda técnica,
   - validaciones faltantes,
   - riesgos de regresión,
   - problemas de diseño.
4. Señala exactamente qué archivos y módulos están involucrados.

Formato de salida:
1. Flujo actual
2. Componentes afectados
3. Archivos relevantes
4. Hallazgos técnicos
5. Riesgos de modificación
```

---

## Prompt 2.3 — Análisis de impacto cruzado

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
Usa el prompt de análisis técnico profundo y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA ACTUAL]
- ambiente: [DEV / QA / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: código fuente, esquema de BD, contratos API
- objetivo puntual de salida: flujo actual documentado + matriz de impacto cruzado
- nivel de profundidad: alto
```

---

## Salida esperada

### Análisis técnico profundo

| Sección | Contenido esperado |
|---|---|
| Flujo actual | Descripción paso a paso del comportamiento real |
| Componentes afectados | Lista de servicios, módulos y tablas |
| Archivos relevantes | Rutas exactas en el repositorio |
| Hallazgos técnicos | Deuda, acoplamientos, riesgos detectados |
| Riesgos de modificación | Qué puede romperse al cambiar |

### Impacto cruzado

| Componente | Tipo de impacto | Severidad | Riesgo | Recomendación |
|---|---|---|---|---|
