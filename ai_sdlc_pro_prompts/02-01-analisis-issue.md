# 2.1 — Análisis funcional de un requerimiento, issue o cambio

## Descripción

Prompt para analizar un requerimiento, issue o cambio y determinar su alcance funcional: flujo de negocio afectado, actores, comportamiento actual vs esperado, criterios de aceptación y riesgos.

**Cuándo usarlo:** como primer paso al recibir una tarea, antes de cualquier análisis técnico o diseño.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Analiza el requerimiento, issue o cambio solicitado y determina su alcance funcional y técnico dentro del proyecto, considerando la estructura del monorepo y los estándares aplicables.

Entradas:
- issue o requerimiento: [PEGAR]
- repositorio o módulo: [INDICAR]
- workspace/subproyecto: [INDICAR SI APLICA]
- estándar/compliance: [PSP / TSP / ISO / MOPROSOFT / MAAGTICSI / NINGUNO]

Actividades:
1. Comprende el problema o necesidad.
2. Identifica:
   - flujo de negocio afectado,
   - actor(es),
   - caso(s) de uso,
   - comportamiento actual,
   - comportamiento esperado,
   - criterios de aceptación funcionales y de calidad.
3. Determina el subproyecto/workspace del monorepo afectado y si hay dependencias con otros paquetes locales.
4. Revisa si ya está documentado en el proyecto.
5. Relaciona el requerimiento con módulos, componentes y datos impactados.
6. Detecta dependencias, riesgos y controles de seguridad (DevSecOps/ISO 27001).

Salida:
0. Bloque JSON de Metadatos de Tarea al inicio (claves: status, impacted_components, risks_detected, confidence_score [0.0 a 1.0]).
1. Resumen funcional
2. Casos de uso impactados
3. Reglas de negocio detectadas
4. Componentes técnicos involucrados
5. Riesgos funcionales y técnicos
6. Recomendación de atención
7. Registro de Métricas PSP/TSP (Tiempo estimado de atención en minutos, tiempo real y densidad de defectos sugerida).
```

---

## Uso con fórmula estándar

```text
Usa el prompt de análisis funcional y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [PEGAR TEXTO O REFERENCIA]
- rama: [RAMA ACTUAL]
- ambiente: [DEV / QA / PROD]
- componentes: [SI YA CONOCES ALGUNO]
- documentos a revisar: README, docs/, casos de uso existentes
- objetivo puntual de salida: alcance funcional completo con criterios de aceptación
- nivel de profundidad: alto
```

---

## Salida esperada

| Sección | Contenido esperado |
|---|---|
| Metadatos JSON (0) | Bloque JSON estructurado y parseable con metadatos de diagnóstico inicial |
| Resumen funcional (1) | Problema o necesidad en lenguaje de negocio |
| Casos de uso impactados (2) | Lista de CU afectados o derivados |
| Reglas de negocio (3) | Restricciones, validaciones, lógica detectada |
| Componentes técnicos (4) | Módulos, servicios, tablas involucradas |
| Riesgos (5) | Funcionales y técnicos identificados |
| Recomendación (6) | Prioridad y orden de atención sugerido |
| Métricas PSP/TSP (7) | Bloque de control con tiempos estimados en minutos y tasa esperada de defectos |
