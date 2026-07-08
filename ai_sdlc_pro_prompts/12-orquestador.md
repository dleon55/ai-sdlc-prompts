# 12 — Prompt maestro orquestador del ciclo completo

## Descripción

Prompt que clasifica una asignación y selecciona el flujo mínimo suficiente para completarla con seguridad y evidencia. Puede operar con un solo agente, un workflow determinista o un supervisor con subagentes.

**Cuándo usarlo:** cuando una asignación requiere coordinación entre varias capacidades, fases o agentes. Para tareas simples, utiliza directamente el prompt especializado correspondiente.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | operación (meta-prompt de enrutamiento — no ejecuta trabajo técnico directamente) |
| Riesgo esperado | variable — depende de la asignación que enrute; el propio prompt exige declarar riesgo y reversibilidad como parte de la clasificación |
| Entradas requeridas | issue/requerimiento, rama objetivo, ambiente, componentes, nivel de autonomía permitido, herramientas disponibles, presupuesto |
| Herramientas permitidas | las que declare el contrato de ejecución generado en el Paso 3 — no asume herramientas por defecto |
| Autonomía permitida | definida dinámicamente por el propio prompt (Paso 3, "Crear contrato"); nunca debe exceder el nivel de autonomía de entrada declarado |
| Criterios de detención | "No ejecutes todas las fases por defecto"; escalar a humano cuando el riesgo o permiso exceda el contrato generado |
| Salida esperada | ver `## Fases y entregables esperados` y el formato de salida obligatorio de 8 puntos del prompt |
| Evidencia mínima | contrato de ejecución explícito (alcance, herramientas, checkpoints, condición de detención) antes de delegar cualquier subtarea |
| Siguiente prompt recomendado | el que determine el propio contrato de ejecución — este prompt es el punto de entrada, no de salida |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Enruta y coordina esta asignación mediante el flujo mínimo que permita cumplirla con evidencia verificable.

Entrada:
- issue/requerimiento/incidente: [PEGAR]
- rama objetivo: [RAMA OBJETIVO]
- ambiente: [AMBIENTE]
- componentes: [COMPONENTES INVOLUCRADOS]
- nivel de autonomía permitido: [A0 / A1 / A2 / A3]
- herramientas disponibles: [HERRAMIENTAS DISPONIBLES]
- presupuesto: [TIEMPO / CAMBIOS / INTENTOS / COSTE]

Paso 1. CLASIFICAR
- intención: [analizar / diseñar / implementar / revisar / investigar / operar]
- complejidad: [simple / compuesta / abierta]
- riesgo: [bajo / medio / alto]
- reversibilidad: [alta / media / baja]
- evidencia necesaria para finalizar

Paso 2. SELECCIONAR PATRÓN
- agente único: tarea acotada y claramente verificable
- workflow secuencial: pasos conocidos con dependencias
- workflow paralelo: subtareas independientes
- supervisor + subagentes: especialidades distintas y reconciliación necesaria
- human-in-the-loop: decisiones ambiguas o acciones de alto riesgo

No ejecutes todas las fases por defecto.

Paso 3. CREAR CONTRATO
- alcance y exclusiones
- herramientas y permisos
- acciones que requieren aprobación
- estados y checkpoints
- presupuesto y condición de detención
- criterios de éxito y evidencia

Estados permitidos:
`discovered`, `planned`, `approved`, `executing`, `verifying`, `blocked`, `completed`, `rolled_back`.

Paso 4. EJECUTAR
- carga sólo las capacidades necesarias
- delega subtareas con entrada, alcance y salida explícitos
- preserva aislamiento y ownership
- registra decisiones, tool calls relevantes y evidencia
- reconcilia resultados antes de integrar

Paso 5. VERIFICAR
- criterios de aceptación
- pruebas proporcionales al impacto
- seguridad y regresiones
- diff y alcance real
- riesgos residuales

Paso 6. CERRAR O ESCALAR
- marca `completed` sólo con evidencia suficiente
- marca `blocked` cuando exista un impedimento real y documentado
- usa `rolled_back` si la ejecución fue revertida
- solicita decisión humana cuando el riesgo o permiso exceda el contrato

Formato de salida obligatorio:
1. Clasificación y patrón seleccionado
2. Estado actual
3. Contrato de ejecución
4. Plan o grafo de tareas
5. Acciones ejecutadas
6. Evidencia y validaciones
7. Riesgos residuales
8. Decisiones humanas pendientes
```

---

## Uso con fórmula estándar

```text
Usa el prompt maestro orquestador y adáptalo a:
- repositorio: [NOMBRE O URL]
- issue o requerimiento: [PEGAR TEXTO COMPLETO]
- rama objetivo: [RAMA DESTINO]
- ambiente: [DEV / QA / STAGING / PROD]
- componentes: [COMPONENTES INVOLUCRADOS]
- documentos a revisar: README, docs/, arquitectura, workflows, issues relacionados
- objetivo puntual de salida: ciclo completo documentado listo para ejecución
- nivel de profundidad: alto
```

---

## Fases y entregables esperados

| Patrón | Cuándo usarlo | Entregable |
|---|---|---|
| Agente único | Tarea pequeña y acotada | Cambio o análisis verificado |
| Secuencial | Dependencias estrictas | Checkpoints por etapa |
| Paralelo | Subtareas independientes | Entregables reconciliados |
| Supervisor | Varias especialidades | Resultado integrado y revisado |
| Humano en el ciclo | Riesgo alto o decisión ambigua | Aprobación y evidencia |
