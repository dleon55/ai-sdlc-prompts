# 14.2 — Registro de métricas de calidad y estimaciones PSP/TSP

## Descripción

Prompt estructurado para guiar al desarrollador en el registro de métricas de tamaño, esfuerzo, tiempos por fase y bitácora de defectos, siguiendo las metodologías formales PSP (Personal Software Process) y TSP (Team Software Process).

**Cuándo usarlo:** al inicio del desarrollo para registrar la estimación base (plan) y al finalizar cada fase de ingeniería de software para registrar el esfuerzo y defectos reales.

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
