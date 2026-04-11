# 0-C.1 — Documentar un issue listo para ejecución por agente IA

## Descripción

Prompt para redactar un issue GitHub de alta calidad que pueda ser ejecutado por un agente IA de forma autónoma y controlada: con contexto suficiente, criterios de aceptación verificables, restricciones explícitas, archivos involucrados y checklist de validación humana post-ejecución.

**Cuándo usarlo:** antes de asignar cualquier tarea a un agente IA (Copilot Agent, Claude, Codex, Windsurf), para garantizar que el agente opere con contexto completo y dentro de límites seguros.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Redacta un issue GitHub completo y listo para ser ejecutado por un agente IA, siguiendo las mejores prácticas de documentación y gobierno de agentes.

Inputs requeridos:
- título del issue: [TÍTULO CORTO Y PRECISO]
- tipo: [feat / fix / refactor / chore / docs / test / security / infra]
- descripción del problema o requerimiento: [DESCRIPCIÓN EN LENGUAJE NATURAL]
- repositorio y rama destino: [REPO / BRANCH]
- ambiente: [dev / qa / staging]
- archivos o módulos involucrados (si se conocen): [LISTA]
- criterios de aceptación: [LISTA DE CONDICIONES VERIFICABLES]
- restricciones: [LO QUE EL AGENTE NO PUEDE HACER EN ESTE ISSUE]
- agente asignado: [Copilot / Claude / Codex / Windsurf / Cursor / Antigravity]

Genera el issue con las siguientes secciones:

## Descripción
Explicación clara y precisa del problema o requerimiento. Sin ambigüedades.
- comportamiento actual (si es un fix)
- comportamiento esperado
- contexto de negocio relevante

## Contexto técnico
- rama: [BRANCH]
- ambiente: [AMBIENTE]
- archivos clave involucrados (con ruta relativa)
- dependencias o servicios relacionados
- commits o PRs relacionados (si aplica)

## Criterios de aceptación
Lista numerada, cada uno verificable de forma objetiva por el agente y por el revisor humano:
- [ ] 1. [CRITERIO CONCRETO Y MEDIBLE]
- [ ] 2. ...

## Restricciones para el agente
Lo que el agente NO debe hacer en el contexto de este issue:
- no modificar [ARCHIVOS/MÓDULOS fuera del alcance]
- no ejecutar [ACCIONES DE ALTO RIESGO]
- no alterar configuraciones de [ÁREA CRÍTICA]
- parar y escalar si encuentra: [CONDICIÓN DE ESCALACIÓN]

## Pruebas requeridas
Qué pruebas debe escribir o actualizar el agente:
- tipo de prueba (unitaria / integración / e2e / humo)
- cobertura mínima esperada
- archivo(s) de prueba a crear o modificar

## Checklist de validación humana (post-ejecución)
Revisión que debe hacer el humano antes de hacer merge:
- [ ] El PR solo toca los archivos del alcance definido
- [ ] Los criterios de aceptación fueron satisfechos con evidencia
- [ ] No hay secretos, credenciales ni tokens en el diff
- [ ] Los tests pasan en verde (CI verde)
- [ ] El código sigue las convenciones del proyecto
- [ ] No se instalaron dependencias nuevas sin justificación
- [ ] No hay cambios en workflows, migraciones ni archivos de infraestructura no autorizados

## Nivel de autonomía autorizado
[ ] Solo análisis y propuesta (el agente no hace commits)
[ ] Propuesta con draft PR (el agente crea PR en borrador)
[ ] Ejecución controlada (el agente puede hacer commits en rama de feature)
[ ] Ejecución autónoma (el agente puede completar y pedir merge)

## Labels sugeridos
[tipo], [agente-ia], [ambiente], [prioridad]
```

---

## Uso con fórmula estándar

```text
Usa el prompt de issue para agente IA y adáptalo a:
- repositorio: [NOMBRE O URL]
- título del issue: [TÍTULO]
- tipo: [TIPO]
- descripción del requerimiento: [DESCRIPCIÓN]
- archivos involucrados: [LISTA]
- criterios de aceptación: [CRITERIOS]
- restricciones: [RESTRICCIONES]
- agente asignado: [AGENTE]
- nivel de autonomía: [NIVEL]
- objetivo puntual de salida: issue completo listo para crear en GitHub con gh issue create
- nivel de profundidad: alto
```

---

## Salida esperada

Issue redactado con todas las secciones completas, más el comando para crearlo directamente:

```bash
gh issue create \
  --repo [ORG/REPO] \
  --title "[TIPO]: [TÍTULO]" \
  --body-file issue-draft.md \
  --label "[tipo],[agente-ia],[prioridad]" \
  --assignee "@me"
```

---

## Antipatrones a evitar

| Antipatrón | Consecuencia | Solución |
|---|---|---|
| "Arregla el login" sin más contexto | El agente asume ruta incorrecta | Incluir archivos involucrados y comportamiento esperado |
| Sin criterios de aceptación | El agente no sabe cuándo terminó | Criterios numerados y verificables |
| Sin restricciones | El agente toca archivos fuera del alcance | Lista explícita de lo que NO debe tocar |
| Sin checklist humano | PR se mergea sin revisar output del agente | Sección de validación humana obligatoria |
| Nivel de autonomía no definido | El agente asume autonomía total | Siempre declarar el nivel autorizado |
