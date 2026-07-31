# AI-SDLC Prompts — servidor MCP

Expone la biblioteca de prompts [AI-SDLC Pro](../README.md) (112 prompts, ES/EN) a agentes de IA (Claude Code, Claude Desktop, Cursor, etc.) vía [Model Context Protocol](https://modelcontextprotocol.io), transporte stdio.

Solo lectura: ningún tool escribe en el repositorio, en GitHub ni en ningún sistema externo. Todo el contenido se sirve desde `data/prompts-full.json`, generado por `python build.py` en la raíz del repo — este servidor nunca parsea Markdown por su cuenta.

## Instalación

```bash
cd mcp-server
npm install
```

## Ejecutar

```bash
npm start
# equivalente a: node index.js
```

El proceso escucha en stdin/stdout (protocolo MCP) — no expone HTTP ni requiere red. Se cierra con `Ctrl+C` o cuando el cliente cierra la conexión.

## Configurar en Claude Code / Claude Desktop

Agrega esto a la configuración de servidores MCP del cliente (`claude_desktop_config.json` o el equivalente de Claude Code), ajustando la ruta absoluta al checkout local:

```json
{
  "mcpServers": {
    "ai-sdlc-prompts": {
      "command": "node",
      "args": ["/ruta/absoluta/a/ai-sdlc-prompts/mcp-server/index.js"]
    }
  }
}
```

## Herramientas expuestas

| Herramienta | Descripción |
|---|---|
| `list_prompts` | Lista prompts, con filtro opcional por sección (`00`-`17`), riesgo (`low`/`medium`/`high`/`variable`), autonomía (`A0`-`A3`) y texto libre. |
| `get_prompt` | Detalle completo de un prompt por `id`: título, descripción, texto crudo (placeholders sin resolver), fórmulas de uso, contrato editorial y siguiente(s) prompt(s) recomendado(s). |
| `resolve_prompt` | Sustituye los placeholders del prompt (y opcionalmente el preámbulo del framework) con variables provistas — misma sustitución que hace el sitio. Devuelve el texto resuelto y los placeholders obligatorios/opcionales que quedaron sin resolver. |
| `get_framework` | Preámbulo obligatorio del framework (el bloque que el sitio antepone a cada prompt copiado). |
| `recommend_next` | Prompt(s) recomendado(s) por el contrato editorial para continuar después de uno dado. |

### Variables de `resolve_prompt`

Las claves de `variables` son los **campos canónicos** del sistema de variables del sitio, no los alias `[EN MAYÚSCULAS]` que aparecen en el texto del prompt:

`repositorio`, `referencia`, `rama_actual`, `rama_destino`, `ambiente`, `componentes`, `modulo`, `stack`, `tipo_proyecto`, `metodologia`, `agentes`, `autonomia`, `entrada`, `objetivo`, `responsable`, `workspace`, `compliance`, `documentos`, `profundidad`, `adicionales` (líneas `TOKEN=valor` para placeholders no cubiertos por los campos anteriores).

Ejemplo:

```json
{
  "id": "07-06-pruebas-performance-carga",
  "lang": "es",
  "variables": {
    "repositorio": "org/mi-repo",
    "ambiente": "staging",
    "adicionales": "PATRON DE CARGA=1000 req/s durante 10 min"
  }
}
```

## Desarrollo

```bash
npm test    # node --test test/ -- 24 tests: dataStore, resolvePrompt, integración MCP real (InMemoryTransport)
```

Los datos (`data/prompts-full.json`) se regeneran desde la raíz del repo con `python build.py` — no editar ese archivo a mano. Cualquier cambio de contenido de prompts se hace en `ai_sdlc_pro_prompts/*.md`.

## Alcance de esta primera versión

- Solo ejecución local desde este checkout (`node index.js` / `npm start`). No se publica a npm.
- Transporte stdio únicamente — sin servidor HTTP.
