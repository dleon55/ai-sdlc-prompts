# 0-C.3 — Configuración específica por tipo de agente IA

## Descripción

Prompt y referencia para configurar el comportamiento, las instrucciones y las restricciones de cada tipo de agente IA según sus capacidades y mecanismos propios: GitHub Copilot (Agent / Chat / Edits), Claude (Anthropic), OpenAI Codex, Windsurf, Cursor y Chrome Antigravity. Garantiza que cada agente opere con el contexto del proyecto y dentro de las reglas de equipo.

**Cuándo usarlo:** al incorporar un nuevo tipo de agente al proyecto, al detectar que un agente no sigue las convenciones, o al configurar un entorno multi-agente por primera vez.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Genera las instrucciones de configuración para cada agente IA activo en este proyecto, según sus mecanismos propios de control y los estándares del repositorio.

Inputs requeridos:
- agentes activos: [lista: Copilot / Claude / Codex / Windsurf / Cursor / Antigravity]
- stack del proyecto: [STACK]
- metodología: [METODOLOGÍA]
- reglas críticas del proyecto: [REGLAS QUE TODOS DEBEN CUMPLIR]
- nivel de autonomía general: [NIVEL]

Para cada agente activo, entrega:

─────────────────────────────────────
GITHUB COPILOT (Agent / Chat / Edits)
─────────────────────────────────────
Archivo: .github/copilot-instructions.md
Contenido:
- rol del agente: Ingeniero de Software Senior trabajando en [PROYECTO]
- stack: [versiones exactas de lenguaje, framework, DB, infra]
- convenciones de código: nombrado, estructura, patrones obligatorios y prohibidos
- reglas de commit: formato Conventional Commits, commits atómicos
- qué archivos NO modificar sin aprobación: workflows/, migrations/, .env, CODEOWNERS
- cómo actuar ante ambigüedad: pausar y preguntar al usuario humano
- reglas QA: no proponer código sin pruebas para lógica de negocio nueva
- modo plan: cuando el usuario diga "modo plan" o "solo analiza", no hacer cambios

Archivos adicionales de Copilot:
- .github/prompts/ → prompts reutilizables para tareas frecuentes del proyecto
- .github/instructions/ → instrucciones por tipo de archivo (applyTo patterns):
  - *.py → convenciones Python del proyecto
  - *.yml → reglas para modificar workflows
  - *.sql / migrations/ → "nunca modificar sin aprobación explícita"

─────────────────────────────────────
CLAUDE (Anthropic — API / claude.ai)
─────────────────────────────────────
Mecanismo: system prompt (primer mensaje del contexto)
Contenido del system prompt base:
- rol, proyecto y stack
- reglas de comportamiento (mismas del 00-framework.md)
- instrucción de modo plan por defecto si no se indica lo contrario
- instrucción de reportar siempre en formato estructurado: hechos / hallazgos / supuestos / riesgos / recomendaciones
- instrucción de prefijo de rama: claude/[issue]/[descripcion]
- instrucción de "no ejecutar hasta confirmación humana explícita"

Archivo a crear: docs/ai-agents/claude-system-prompt.md
(plantilla del system prompt para usar en cada sesión Claude del proyecto)

─────────────────────────────────────
OPENAI CODEX (API / GitHub Copilot X)
─────────────────────────────────────
Mecanismo: instrucciones en el prompt + AGENTS.md en el repo
Configuración:
- AGENTS.md en raíz: define rol de Codex, accesos permitidos y prohibidos
- Instrucciones de rama: codex/[issue]/[descripcion]
- Restricciones de herramientas: qué comandos puede ejecutar (tests, lint, build) y cuáles no (deploy, migrate, push a main)
- Instrucción de sandbox: ejecutar tests en entorno aislado, no modificar datos de staging/prod
- Modo de aprobación: proponer cambios como diff para revisión humana antes de aplicar

Archivo a crear: docs/ai-agents/codex-config.md

─────────────────────────────────────
WINDSURF (Codeium)
─────────────────────────────────────
Mecanismo: .windsurfrules en raíz del repositorio
Secciones del archivo:
- [context]: descripción del proyecto, stack, arquitectura
- [rules]: convenciones de código, patrones prohibidos
- [security]: OWASP aplicables, secretos, validación de input
- [workflow]: siempre revisar antes de modificar, commits atómicos, rama con prefijo windsurf/
- [restricted_files]: lista de archivos que requieren confirmación explícita
- [escalation]: condiciones donde Windsurf debe pausar y mostrar advertencia al usuario

─────────────────────────────────────
CURSOR
─────────────────────────────────────
Mecanismo: .cursorrules en raíz del repositorio (o .cursor/rules/)
Estructura del archivo:
- descripción del proyecto y stack en lenguaje natural
- reglas de código: qué patrones usar, cuáles evitar
- instrucciones de seguridad: sin secretos hardcodeados, sin eval(), sin SQL concatenado
- reglas de testing: todo cambio de lógica de negocio requiere test
- rama con prefijo cursor/[issue]/[descripcion]
- instrucción de modo plan disponible: cuando se indique "plan only"

─────────────────────────────────────
CHROME ANTIGRAVITY (pruebas E2E en navegador)
─────────────────────────────────────
Mecanismo: instrucciones en el prompt de tarea + archivo de configuración
Alcance específico: solo pruebas en navegador, no modificación de código fuente
Configuración:
- URL base por ambiente: [DEV_URL / QA_URL / STAGING_URL]
- credenciales de prueba: usar variables de entorno, nunca hardcodear
- flujos autorizados: lista de flows que puede automatizar
- datos de prueba: usar solo datasets marcados como "test data", nunca datos reales
- captura de evidencias: screenshots y video obligatorios para cada escenario ejecutado
- reporte: formato estándar del proyecto (tabla: escenario | resultado | evidencia)
- restricción: no ejecutar en producción

Archivo a crear: docs/ai-agents/antigravity-config.md

─────────────────────────────────────
TABLA COMPARATIVA DE MECANISMOS
─────────────────────────────────────

| Agente | Mecanismo de instrucción | Archivo del repo | Scope |
|---|---|---|---|
| GitHub Copilot | .github/copilot-instructions.md | Sí, en repo | Código + análisis |
| Claude | System prompt | docs/ai-agents/claude-system-prompt.md | Análisis + código |
| OpenAI Codex | AGENTS.md + prompt | AGENTS.md | Código + shell |
| Windsurf | .windsurfrules | Sí, en repo | Código |
| Cursor | .cursorrules | Sí, en repo | Código |
| Antigravity | Prompt de tarea | docs/ai-agents/antigravity-config.md | Solo browser/E2E |

Reglas que deben estar presentes en TODOS los agentes:
- nunca hacer push a ramas protegidas directamente
- nunca exponer secretos, tokens ni credenciales
- nunca ejecutar migraciones sin aprobación humana
- nunca modificar workflows de CI/CD sin revisión
- ante ambigüedad o riesgo, pausar y escalar
- todos los cambios son trazables: rama nombrada con prefijo de agente + issue ID
```

---

## Uso con fórmula estándar

```text
Usa el prompt de configuración por tipo de agente y adáptalo a:
- repositorio: [NOMBRE O URL]
- agentes activos: [LISTA]
- stack: [STACK]
- metodología: [METODOLOGÍA]
- reglas críticas: [REGLAS ESPECÍFICAS DEL PROYECTO]
- nivel de autonomía: [NIVEL]
- documentos a revisar: README, CONTRIBUTING, AGENTS.md existente (si hay), estructura del repo
- objetivo puntual de salida: archivos de instrucciones completos para cada agente activo + tabla comparativa
- nivel de profundidad: alto
```

---

## Estructura de carpeta docs/ai-agents/ recomendada

```
docs/ai-agents/
├── README.md                    ← índice de agentes configurados y nivel de acceso
├── claude-system-prompt.md      ← system prompt base para sesiones Claude
├── codex-config.md              ← configuración y restricciones para Codex
└── antigravity-config.md        ← config de ambientes y flows autorizados para Antigravity
```
