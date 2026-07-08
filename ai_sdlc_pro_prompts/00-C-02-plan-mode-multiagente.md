# 0-C.2 — Modo plan seguro y coordinación multi-agente

## Descripción

Prompt para ejecutar cualquier tarea en **modo plan** antes de implementar: el agente analiza, diseña y propone sin tocar el código. Incluye el protocolo de coordinación para entornos donde múltiples agentes (Copilot, Claude, Codex, Windsurf, Antigravity) operan en paralelo sobre el mismo repositorio, previniendo conflictos, sobreescrituras y pérdida de trabajo.

**Cuándo usarlo:** siempre antes de ejecutar tareas de alto impacto, cuando hay más de un agente activo en el repo, o cuando se trabaja en `mode:plan` en Agent Manager o GitHub Copilot Agent.

---

## Contrato editorial

| Campo | Valor |
|---|---|
| Tipo | análisis |
| Riesgo esperado | bajo — el modo plan prohíbe explícitamente modificar archivos, hacer commits o ejecutar comandos que alteren el repositorio o el ambiente; el riesgo real es indirecto (un conflicto no detectado desperdicia trabajo de otro agente en paralelo) |
| Entradas requeridas | issue/tarea de referencia, rama objetivo, agentes activos en paralelo si se conocen; estado local del repositorio (rama, worktrees, commits recientes, PRs abiertos) |
| Herramientas permitidas | lectura de estado git (status, log, branches, worktrees) y de PRs/issues abiertos — explícitamente prohibido: `pull`, `fetch`, mutaciones remotas, commits o cambios de archivo |
| Autonomía permitida | A1 — Proponer |
| Criterios de detención | si el Paso 2 (detección de conflictos) encuentra un conflicto potencial o activo — mismo archivo tocado por otro agente o PR abierto — DETENER de inmediato y reportar antes de continuar; no pasar a ejecución controlada sin confirmación humana |
| Salida esperada | no existe una sección `## Salida esperada` independiente en este prompt — el formato de entrega está definido inline en "Entrega en MODO PLAN" (9 subsecciones: archivos a modificar, archivos fuera de alcance, conflictos potenciales, dependencias, pasos, commits, pruebas, señales de alto, contrato de ejecución) y en el "Paso 5. Reporte de estado" del protocolo multi-agente |
| Evidencia mínima | la tabla de archivos a modificar incluye riesgo y si requiere aprobación; la sección de detección de conflictos documenta explícitamente presencia o ausencia de solapamiento con ramas/PRs activos |
| Siguiente prompt recomendado | `06-01-implementacion-multiagente` una vez aprobado el plan y sin conflictos, para pasar a ejecución controlada |

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo — MODO PLAN

```text
Objetivo:
Opera en MODO PLAN. No modifiques ningún archivo. No hagas commits. No ejecutes comandos que alteren el estado del repositorio o del ambiente.

Tu trabajo en este modo es:
1. Analizar el estado actual del repositorio relacionado con la tarea.
2. Mapear qué archivos serían modificados y por qué.
3. Identificar riesgos, conflictos potenciales y dependencias.
4. Proponer el plan de implementación detallado.
5. Estimar el alcance del cambio (líneas, archivos, módulos).
6. Señalar qué requiere aprobación humana antes de ejecutar.
7. Definir criterios de éxito, evidencia y presupuesto de ejecución.
8. Identificar subtareas independientes y dependencias entre ellas.

Entrada:
- issue/tarea: [REFERENCIA O DESCRIPCIÓN]
- rama objetivo: [BRANCH]
- agentes activos en paralelo (si se conocen): [LISTA O "ninguno conocido"]

Entrega en MODO PLAN:

## Plan de implementación
### 1. Archivos que serían modificados
| Archivo | Tipo de cambio | Riesgo | Requiere aprobación |
|---|---|---|---|

### 2. Archivos que NO deben tocarse en esta tarea
(Lista explícita para evitar scope creep)

### 3. Conflictos potenciales con trabajo en paralelo
- ramas activas que tocan los mismos archivos
- cambios recientes (últimas 48h) en archivos del alcance
- issues o PRs abiertos relacionados

### 4. Dependencias y precondiciones
- qué debe estar listo antes de ejecutar
- variables de entorno o secretos necesarios
- migraciones o datos requeridos

### 5. Pasos de implementación propuestos
Numerados, atómicos, con qué archivo cambia en cada paso.

Representa las dependencias como un grafo simple:
| ID | Tarea | Depende de | Owner sugerido | Entregable verificable |
|---|---|---|---|---|

### 6. Estrategia de commits
- número de commits estimados
- mensaje de cada commit (convención del proyecto)
- orden recomendado

### 7. Plan de pruebas
- pruebas a escribir o actualizar
- cómo verificar que los criterios de aceptación se cumplen

### 8. Señales de alto que detienen la ejecución
Lista de condiciones donde el agente debe pausar y escalar al humano:
- encontrar [condición A]
- encontrar [condición B]

### 9. Contrato de ejecución
- nivel de riesgo:
- modo de autonomía:
- herramientas permitidas:
- acciones que requieren aprobación:
- presupuesto de archivos/tiempo/intentos:
- evidencia de finalización:

Solicita aprobación únicamente para acciones que la política o el nivel de riesgo no hayan preautorizado.
```

---

## Prompt completo — PROTOCOLO MULTI-AGENTE

```text
Objetivo:
Antes de iniciar cualquier trabajo, ejecuta el protocolo de coordinación multi-agente para este repositorio.

Paso 1. VERIFICACIÓN DE ESTADO
- inspecciona estado local, rama, worktrees, cambios recientes y PRs relacionados usando comandos compatibles con el entorno
- no ejecutes `pull`, `fetch`, mutaciones remotas ni comandos con red sin autorización o necesidad confirmada

Paso 2. DETECCIÓN DE CONFLICTOS POTENCIALES
- lista los archivos que modificarías en esta tarea
- verifica si alguno fue modificado en los últimos commits
- verifica si hay PRs abiertos que toquen los mismos archivos
- si hay conflicto: DETENER y reportar antes de continuar

Paso 3. AISLAMIENTO Y OWNERSHIP
- usa un worktree, workspace o rama aislada cuando exista ejecución concurrente
- registra task ID, owner, alcance de archivos y dependencias en el mecanismo de coordinación disponible
- no uses commits vacíos como bloqueo: una rama no garantiza exclusividad
- si no existe mecanismo de coordinación, reporta el riesgo y reduce el alcance

Paso 4. REGLAS DE CONVIVENCIA ENTRE AGENTES
- cada subtarea tiene un owner y contrato de entrega
- dos agentes pueden trabajar en paralelo sólo si sus entregables son independientes o existe una estrategia explícita de reconciliación
- ningún agente hace merge a main/develop sin aprobación humana
- commits atómicos — un cambio lógico por commit
- ante solapamiento, determina si el conflicto es textual, contractual o semántico; pausa únicamente el área afectada

Paso 5. REPORTE DE ESTADO
Al finalizar el plan o la ejecución, reporta:
- rama creada: [RAMA CREADA]
- archivos modificados: [LISTA]
- tests actualizados: [SÍ/NO]
- PR abierto: [URL o "pendiente de aprobación para crear"]
- conflictos detectados: [NINGUNO / DESCRIPCIÓN]
- pendiente de revisión humana: [LISTA]
```

---

## Uso con fórmula estándar

```text
Usa el prompt de modo plan y coordinación multi-agente y adáptalo a:
- repositorio: [NOMBRE O URL]
- tarea o issue: [REFERENCIA]
- rama objetivo: [BRANCH]
- agentes activos en paralelo: [LISTA O "ninguno conocido"]
- modo: [SOLO PLAN / PLAN + EJECUCIÓN CONTROLADA]
- documentos a revisar: git log reciente, PRs abiertos, AGENTS.md
- objetivo puntual de salida: plan de implementación con tabla de archivos + detección de conflictos + reserva de rama
- nivel de profundidad: alto
```

---

## Convención de nombres de rama por agente

| Agente | Prefijo de rama | Ejemplo |
|---|---|---|
| GitHub Copilot | `copilot/` | `copilot/42/fix-login` |
| Claude (Anthropic) | `claude/` | `claude/43/refactor-auth` |
| OpenAI Codex | `codex/` | `codex/44/add-tests` |
| Windsurf | `windsurf/` | `windsurf/45/update-nginx` |
| Cursor | `cursor/` | `cursor/46/style-cleanup` |
| Antigravity | `antigravity/` | `antigravity/47/e2e-flow` |
| Humano / mixto | `feat/`, `fix/`, etc. | `feat/user-profile` |

---

## Semáforo de ejecución

| Estado | Color | Descripción | Acción del agente |
|---|---|---|---|
| Sin conflictos, plan aprobado | 🟢 Verde | Área libre, plan claro | Proceder con ejecución controlada |
| Conflicto potencial detectado | 🟡 Amarillo | Otro agente modificó archivos cercanos | Reportar, esperar confirmación humana |
| Conflicto activo confirmado | 🔴 Rojo | Mismo archivo modificado en trabajo activo | Detener, no hacer commits, escalar |
| Área crítica (infra/cicd/bd) | 🔴 Rojo | workflows/, migrations/, docker-compose | Siempre requiere aprobación humana explícita |
