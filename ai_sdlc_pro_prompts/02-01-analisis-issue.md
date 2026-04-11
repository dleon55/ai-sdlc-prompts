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
Analiza el requerimiento, issue o cambio solicitado y determina su alcance funcional y técnico dentro del proyecto.

Entradas:
- issue o requerimiento: [PEGAR]
- repositorio o módulo: [INDICAR]

Actividades:
1. Comprende el problema o necesidad.
2. Identifica:
   - flujo de negocio afectado,
   - actor(es),
   - caso(s) de uso,
   - comportamiento actual,
   - comportamiento esperado,
   - criterios de aceptación si existen.
3. Revisa si ya está documentado en el proyecto.
4. Relaciona el requerimiento con módulos, componentes y datos impactados.
5. Detecta dependencias y riesgos.

Salida:
1. Resumen funcional
2. Casos de uso impactados
3. Reglas de negocio detectadas
4. Componentes técnicos involucrados
5. Riesgos funcionales y técnicos
6. Recomendación de atención
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
| Resumen funcional | Problema o necesidad en lenguaje de negocio |
| Casos de uso impactados | Lista de CU afectados o derivados |
| Reglas de negocio | Restricciones, validaciones, lógica detectada |
| Componentes técnicos | Módulos, servicios, tablas involucradas |
| Riesgos | Funcionales y técnicos identificados |
| Recomendación | Prioridad y orden de atención sugerido |
