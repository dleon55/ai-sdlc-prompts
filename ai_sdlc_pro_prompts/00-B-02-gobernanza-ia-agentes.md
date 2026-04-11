# 0-B.2 — Configuración de archivos de gobernanza para agentes IA

## Descripción

Prompt para generar los archivos de configuración y gobierno que controlan el comportamiento de los agentes IA sobre el repositorio: instrucciones de rol, reglas de codificación, restricciones de seguridad, contexto del proyecto y protocolo de trabajo. Compatible con GitHub Copilot, Claude, Windsurf, Cursor, Codex y otros agentes.

**Cuándo usarlo:** al iniciar un repositorio nuevo, al incorporar agentes IA a un proyecto existente, o cuando los agentes no siguen las convenciones ni el marco de trabajo del proyecto.

---

## Contexto obligatorio previo

> Incluye el bloque del archivo `00-framework.md` antes de este prompt.

---

## Prompt completo

```text
Objetivo:
Genera los archivos de configuración y gobernanza que controlen el comportamiento de los agentes IA asignados a este repositorio.

Inputs requeridos:
- nombre del proyecto: [NOMBRE]
- stack tecnológico: [ej. Python 3.11 + FastAPI + PostgreSQL + Docker]
- metodología de trabajo: [SCRUM / Kanban / GitFlow / GitHub Flow / Trunk-Based]
- plataforma de agentes IA a usar: [GitHub Copilot / Claude / Windsurf / Cursor / Codex / Antigravity / combinación]
- nivel de autonomía permitido: [solo análisis / análisis + propuesta / ejecución controlada / ejecución autónoma]
- reglas críticas del proyecto: [ej: nunca editar main directamente, no regenerar migraciones ya aplicadas, etc.]
- patrones prohibidos: [ej: no usar eval(), no hardcodear secretos, no instalar dependencias sin aprobación]

Entrega los siguientes archivos con su contenido completo:

1. .github/copilot-instructions.md
   - rol del agente en este repositorio
   - stack y versiones que debe usar
   - convenciones de código (nombrado, estructura, patrones preferidos)
   - qué archivos/carpetas NO debe modificar sin aprobación
   - formato de commits que debe generar
   - reglas de QA (no merge sin tests, cobertura mínima, etc.)
   - cómo debe escalar si detecta ambigüedad o riesgo

2. .windsurfrules (o .cursorrules si aplica Cursor)
   - contexto del proyecto en lenguaje natural
   - tecnologías y frameworks activos
   - patrones de código preferidos y prohibidos
   - reglas de seguridad (OWASP aplicables al stack)
   - instrucción de "siempre revisar antes de modificar"
   - instrucción de commits atómicos

3. AGENTS.md (raíz del repositorio)
   - propósito del archivo
   - lista de agentes autorizados y su rol
   - nivel de acceso por agente (lectura / propuesta / ejecución)
   - protocolo de escalación y aprobación humana
   - qué decisiones NUNCA puede tomar un agente solo

4. docs/ai-governance.md
   - política de uso de IA en el proyecto
   - ambientes donde está permitida la ejecución autónoma
   - checklist de seguridad antes de aprobar un cambio generado por IA
   - registro de decisiones de IA que requieren auditoría

Reglas que deben aparecer en TODOS los archivos:
- no ejecutar migraciones de base de datos sin aprobación humana explícita
- no modificar workflows de CI/CD sin revisión
- no exponer ni generar secretos, tokens ni credenciales
- no hacer push a ramas protegidas directamente
- ante ambigüedad, pausar y escalar — nunca asumir
```

---

## Uso con fórmula estándar

```text
Usa el prompt de gobernanza de agentes IA y adáptalo a:
- nombre del proyecto: [NOMBRE]
- stack: [STACK]
- metodología: [METODOLOGÍA]
- agentes a configurar: [LISTA DE AGENTES]
- nivel de autonomía: [NIVEL]
- reglas críticas del proyecto: [REGLAS ESPECÍFICAS]
- documentos a revisar: README, CONTRIBUTING, estructura del repo, workflows existentes
- objetivo puntual de salida: archivos .github/copilot-instructions.md, .windsurfrules, AGENTS.md, docs/ai-governance.md con contenido completo
- nivel de profundidad: alto
```

---

## Salida esperada

| Archivo | Propósito | Agente destino | Prioridad |
|---|---|---|---|
| `.github/copilot-instructions.md` | Instrucciones de rol y contexto para Copilot | GitHub Copilot (Chat, Edits, Agent) | Obligatorio |
| `.windsurfrules` | Reglas de comportamiento para Windsurf | Windsurf | Obligatorio si se usa Windsurf |
| `.cursorrules` | Reglas de comportamiento para Cursor | Cursor | Obligatorio si se usa Cursor |
| `AGENTS.md` | Política de uso y protocolo de agentes en el repo | Todos los agentes | Obligatorio |
| `docs/ai-governance.md` | Política formal de gobierno de IA | Equipo humano + auditores | Recomendado |
| `.github/prompts/` | Prompts reutilizables para tareas repetitivas | GitHub Copilot workspace | Recomendado |
| `.github/instructions/` | Instrucciones por tipo de archivo (*.py, *.yml, etc.) | GitHub Copilot | Recomendado |
