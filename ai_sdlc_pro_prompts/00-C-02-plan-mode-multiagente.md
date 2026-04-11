# 0-C.2 — Modo plan seguro y coordinación multi-agente

## Descripción

Prompt para ejecutar cualquier tarea en **modo plan** antes de implementar: el agente analiza, diseña y propone sin tocar el código. Incluye el protocolo de coordinación para entornos donde múltiples agentes (Copilot, Claude, Codex, Windsurf, Antigravity) operan en paralelo sobre el mismo repositorio, previniendo conflictos, sobreescrituras y pérdida de trabajo.

**Cuándo usarlo:** siempre antes de ejecutar tareas de alto impacto, cuando hay más de un agente activo en el repo, o cuando se trabaja en `mode:plan` en Agent Manager o GitHub Copilot Agent.

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

¿Apruebas este plan? Confirma para proceder a ejecución controlada.
```

---

## Prompt completo — PROTOCOLO MULTI-AGENTE

```text
Objetivo:
Antes de iniciar cualquier trabajo, ejecuta el protocolo de coordinación multi-agente para este repositorio.

Paso 1. VERIFICACIÓN DE ESTADO
- git fetch origin && git log --oneline -10 origin/[BRANCH]
- git branch -r | grep -v HEAD
- gh pr list --repo [ORG/REPO] --state open

Paso 2. DETECCIÓN DE CONFLICTOS POTENCIALES
- lista los archivos que modificarías en esta tarea
- verifica si alguno fue modificado en los últimos commits
- verifica si hay PRs abiertos que toquen los mismos archivos
- si hay conflicto: DETENER y reportar antes de continuar

Paso 3. RESERVA DE ÁREA DE TRABAJO
- crea tu rama con prefijo de agente: [tipo-agente]/[issue-id]/[descripcion-corta]
  Ejemplos:
  - copilot/42/fix-login-validation
  - claude/43/refactor-auth-service
  - codex/44/add-unit-tests
  - windsurf/45/update-nginx-config
  - antigravity/46/e2e-checkout-flow
- realiza un commit vacío inicial para marcar el área:
  git commit --allow-empty -m "wip([agente]): reserva rama para issue #[N]"

Paso 4. REGLAS DE CONVIVENCIA ENTRE AGENTES
- un agente = una rama = un issue a la vez
- si dos agentes necesitan el mismo archivo, el segundo espera o trabaja en una copia separada
- ningún agente hace merge a main/develop sin aprobación humana
- commits atómicos — un cambio lógico por commit
- si detectas trabajo de otro agente en la misma área: pausar, reportar, esperar instrucción

Paso 5. REPORTE DE ESTADO
Al finalizar el plan o la ejecución, reporta:
- rama creada: [NOMBRE]
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
