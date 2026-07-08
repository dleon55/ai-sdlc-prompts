# 14.2 — Registro de métricas de calidad y estimaciones PSP/TSP

## Descripción

Prompt estructurado para guiar al desarrollador en el registro de métricas de tamaño, esfuerzo, tiempos por fase y bitácora de defectos, siguiendo las metodologías formales PSP (Personal Software Process) y TSP (Team Software Process).

**Cuándo usarlo:** al inicio del desarrollo para registrar la estimación base (plan) y al finalizar cada fase de ingeniería de software para registrar el esfuerzo y defectos reales.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | documentación |
| Riesgo esperado | bajo — registra métricas y bitácora de defectos, no modifica código, configuración ni proceso de build |
| Entradas requeridas | issue o requerimiento actual, fase del ciclo (Planeación, Diseño, Codificación, Revisión de Código, Pruebas, Post-mortem), métricas o bitácora previa si existen |
| Herramientas permitidas | lectura de historial de tiempos/defectos previos y del issue actual — no requiere ejecución ni acceso a sistemas externos de tracking |
| Autonomía permitida | A0 — Analizar el estado actual; A1 — Proponer el registro actualizado de estimaciones y métricas reales |
| Criterios de detención | no inventar tiempos reales o defectos no reportados por la persona desarrolladora; si falta la estimación base (plan) de una fase, solicitarla antes de calcular rendimiento o densidad de defectos |
| Salida esperada | ver `Salida:` dentro de `## Prompt completo` |
| Evidencia mínima | cada entrada de tiempo o defecto queda asociada a una fase específica y, en el caso de defectos, a su fase de inyección y remoción |
| Siguiente prompt recomendado | repetir este mismo prompt al cierre de la siguiente fase del ciclo; `14-03-iso-moprosoft-compliance` si las métricas alimentan una auditoría formal de cumplimiento |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Genera o actualiza el registro de planeación y métricas reales (tiempos, defectos y tamaño) del ciclo de desarrollo para el requerimiento actual.

Entradas:
- issue o requerimiento: [PEGAR]
- fase actual (Planeación, Diseño, Codificación, Revisión de Código, Pruebas, Post-mortem): [FASE ACTUAL]
- métricas anteriores (si existen): [PEGAR HISTORIAL]

Actividades:
1. Calcula y registra las estimaciones (Plan) de:
   - tamaño en líneas de código (LOC) o puntos de función,
   - tiempo estimado por fase (en minutos).
2. Durante/al final de la fase actual, registra las métricas reales:
   - tiempo real consumido en la fase,
   - bitácora de defectos encontrados (fase de inyección, fase de remoción, tipo de defecto, descripción y tiempo de reparación).
3. Calcula el rendimiento del proceso (Yield) y la densidad de defectos (defectos/KLOC).

Restricciones:
- no inventes tiempos reales ni defectos no reportados por la persona desarrolladora — si un dato no fue provisto, márcalo como pendiente en vez de estimarlo,
- no calcules rendimiento (Yield) ni densidad de defectos si falta la estimación base (Plan) de la fase — solicítala antes de continuar,
- registra fase de inyección y fase de remoción de cada defecto por separado; no las combines en un solo campo,
- no sobrescribas el historial de métricas de ciclos o fases anteriores — el registro es acumulativo, no reemplaza datos previos.

Salida:
1. Resumen de Planeación vs. Real (Tiempos por Fase)
2. Bitácora de Defectos Inyectados/Removidos
3. Indicadores de Calidad del Proceso (Rendimiento, Densidad)
4. Acciones correctivas para el siguiente ciclo
```

---

## Uso con fórmula estándar

```text
Usa el prompt de métricas PSP/TSP y adáptalo a:
- repositorio: [NOMBRE O URL]
- workspace/subproyecto: [SI APLICA]
- estandar/compliance: PSP
- issue o requerimiento: [REFERENCIA]
- rama: [RAMA]
- ambiente: DEV
- componentes: modulo de pagos
- documentos a revisar: bitacora de tiempos previa, plan de diseño
- objetivo puntual de salida: reporte de estimación vs real y bitácora de defectos
- nivel de profundidad: alto
```

---

## Salida esperada

| Fase | Tiempo estimado (min) | Tiempo real (min) | Desviación | Defectos inyectados | Defectos removidos | Densidad (def/KLOC) |
|---|---|---|---|---|---|---|
| Planeación | 60 | 75 | +25% | 0 | 0 | — |
| Diseño | 90 | 80 | -11% | 1 | 0 | — |
| Codificación | 240 | 310 | +29% | 5 | 2 | 3.2 |
| Revisión de código | 45 | 60 | +33% | 0 | 3 | — |
| Pruebas | 120 | 150 | +25% | 0 | 1 | — |
