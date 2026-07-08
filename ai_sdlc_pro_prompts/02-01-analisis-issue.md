# 2.1 — Análisis funcional de un requerimiento, issue o cambio

## Descripción

Prompt para analizar un requerimiento, issue o cambio y determinar su alcance funcional: flujo de negocio afectado, actores, comportamiento actual vs esperado, criterios de aceptación y riesgos.

**Cuándo usarlo:** como primer paso al recibir una tarea, antes de cualquier análisis técnico o diseño.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | medio — un alcance funcional mal definido (actores, comportamiento esperado, criterios de aceptación) puede dirigir mal el análisis técnico y el diseño posteriores, aunque este prompt no ejecuta cambios |
| Entradas requeridas | issue o requerimiento a analizar, repositorio, módulo o funcionalidad, workspace/subproyecto y estándar/compliance aplicable |
| Herramientas permitidas | lectura de código, documentación y del issue/requerimiento — sin ejecución ni cambios |
| Autonomía permitida | A0 — Analizar |
| Criterios de detención | si el issue no aporta información suficiente para fijar comportamiento esperado o criterios de aceptación, declarar el vacío y bajar el `confidence_score` en vez de inventar el alcance |
| Salida esperada | ver `## Salida esperada` |
| Evidencia mínima | cada caso de uso, regla de negocio y riesgo declarado debe estar vinculado al texto del issue o a código/documentación citada, con el bloque JSON de metadatos completo |
| Siguiente prompt recomendado | `02-02-analisis-tecnico` |

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
- repositorio: [NOMBRE O URL]
- módulo o funcionalidad: [MODULO]
- workspace/subproyecto: [WORKSPACE/SUBPROYECTO]
- estándar/compliance: [ESTÁNDAR/COMPLIANCE]

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

Restricciones:
- no propongas ni insinúes una solución técnica o de diseño en este análisis — el objetivo es fijar el alcance funcional, no resolverlo; eso corresponde a `02-02-analisis-tecnico` y a `04-01-diseno-solucion`,
- si el issue no define criterios de aceptación explícitos, no los inventes: decláralos como faltantes y baja el `confidence_score` en proporción a lo que falta,
- distingue en cada sección qué es un hecho confirmado por el texto del issue o por el código/documentación citada, y qué es una suposición tuya — nunca los mezcles sin marcarlos,
- no cierres el análisis como completo si el comportamiento esperado sigue siendo ambiguo; repórtalo como bloqueante en el resumen funcional.

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

### Ejemplo (fragmento)

```json
{
  "status": "analizado_con_vacios",
  "impacted_components": ["build.py", "ai_sdlc_pro_prompts/*.en.md"],
  "risks_detected": ["ruptura de paridad ES/EN si el chequeo se aplica solo a archivos .md"],
  "confidence_score": 0.7
}
```

| Sección | Ejemplo de contenido |
|---|---|
| Resumen funcional (1) | El equipo reporta que `build.py` publica el índice aunque falte el archivo `.en.md` de un prompt nuevo, dejando el sitio con un enlace roto en inglés |
| Riesgos (5) | Alto: si no se detiene el build, el issue puede pasar CI y llegar a producción con contenido bilingüe incompleto; el issue no especifica si debe fallar el build o solo advertir — queda como criterio de aceptación pendiente de confirmar |
