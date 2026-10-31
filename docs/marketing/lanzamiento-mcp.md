# Kit de lanzamiento del servidor MCP (`ai-sdlc-prompts-mcp`)

> Preparado el 31-oct-2026. **El paquete ya está publicado** (`ai-sdlc-prompts-mcp` 1.0.0 en npm, con
> procedencia firmada, 31-oct-2026) y `npx -y ai-sdlc-prompts-mcp` arranca y responde.
>
> Complementa, no sustituye, el material general de `docs/marketing/` (`dev-to-article.md`,
> `linkedin-posts.md`, `producthunt-launch.md`). Este kit trata solo el lanzamiento del MCP.

## Datos verificados (31-oct-2026) — la única fuente para los textos

| Dato | Valor | Dónde se comprobó |
|---|---|---|
| Paquete | `ai-sdlc-prompts-mcp` 1.0.0, se instala con `npx -y ai-sdlc-prompts-mcp` | `mcp-server/package.json` |
| Contenido | 112 prompts, español e inglés, 18 secciones (`00`–`17`) | `mcp-server/README.md` |
| Herramientas | `list_prompts`, `get_prompt`, `resolve_prompt`, `get_framework`, `recommend_next` | paquete publicado 1.0.0 (`tools/list`, 31-oct-2026) |
| Seguridad | Solo lectura, transporte stdio, no abre red, no escribe en ningún sistema | `mcp-server/README.md` |
| Diferenciador | Cada prompt viaja con su **contrato de operación**: autonomía máxima (A0–A3), herramientas permitidas, cuándo detenerse y preguntar, evidencia mínima | `mcp-server/README.md` |
| Licencia | Código MIT; prompts CC BY 4.0 (uso comercial con atribución) | #194 |
| Precio | Los 112 prompts y el MCP: **gratis**. Pro: **$9 USD/mes** o **$90 USD/año** (proyectos ilimitados, personalización por prompt, guardado de resultados) | `prompts.lionsystems.com.mx`, JSON-LD de la portada |

Reglas para cualquier variante que se escriba después:
- Nada de «el mejor», «oficial», «certificado» ni cifras de usuarios o descargas que no existan.
- El precio se revisa en `/precios.html` el día de publicar (`docs/cambiar-precio.md`).
- El MCP es gratis: el texto vende el contrato de operación, no el plan Pro. El Pro se menciona una vez, al final.

## Enlaces con origen medible

Son **enlaces rastreables de Odoo**: cuentan los clics en el CRM (campaña «AI-SDLC Pro · Lanzamiento servidor MCP · nov-2026», nombre técnico `mcp-launch`, medio `organic_social`) y redirigen al sitio con `utm_campaign=mcp-launch`, `utm_source=<canal>` y `utm_medium=organic_social`, que Google Analytics registra. Usa siempre el enlace de su canal.

| Canal | Enlace |
|---|---|
| Dev.to | `https://www.lionsystems.com.mx/r/DMZ` |
| LinkedIn | `https://www.lionsystems.com.mx/r/ZWc` |
| X | `https://www.lionsystems.com.mx/r/OnV` |
| Bluesky | `https://www.lionsystems.com.mx/r/8yk` |
| Reddit | `https://www.lionsystems.com.mx/r/4LZ` |
| Show HN | `https://github.com/dleon55/ai-sdlc-prompts` (HN prefiere el repositorio) |

---

## 1. Artículo para Dev.to (inglés)

**Título:** Your coding agent fetches a prompt over MCP — does it also get the rules for running it?

**Tags:** `mcp`, `ai`, `claude`, `productivity`

```markdown
When I copy a prompt from a website, I read it before I paste it. I notice when it asks the agent
to touch something it shouldn't, and I trim it.

When a coding agent fetches a prompt over MCP, nobody reads it first. The agent just runs it.

That difference is why I built the MCP server for AI-SDLC Pro, an open library of 112 structured
prompts for every phase of the software lifecycle: discovery, architecture, implementation,
testing, security, release and operations. It's free, read-only and installs with one line:

    npx -y ai-sdlc-prompts-mcp

## What the agent gets

Five tools:

- `list_prompts`: filter by lifecycle section, risk level, autonomy level or free text.
- `get_prompt`: the full prompt, its usage notes and the recommended next prompt.
- `resolve_prompt`: fills in your project's variables, the same way the website does.
- `get_framework`: the shared context block that goes in front of every prompt.
- `recommend_next`: the prompt(s) to run after a given one.

## The part that matters: an operating contract

Every prompt ships with a short contract, and `resolve_prompt` appends it by default:

- **Maximum autonomy**, from A0 (analyze only) to A3.
- **Allowed tools** for that task.
- **When to stop and ask**: the ambiguities the agent must not guess through.
- **Minimum evidence**: what the output has to include so you can check it.

If the task contradicts the contract, the prompt tells the agent to say so instead of going past it.
A prompt delivered over MCP without its autonomy ceiling is the riskiest way to lose it.

## Setup

Claude Desktop, Claude Code or Cursor:

    {
      "mcpServers": {
        "ai-sdlc-prompts": {
          "command": "npx",
          "args": ["-y", "ai-sdlc-prompts-mcp"]
        }
      }
    }

It talks over stdio, opens no network connections and writes nothing anywhere. The code is MIT and
the prompts are CC BY 4.0, so you can use them commercially with attribution.

## Try it

Ask your agent: *"List the AI-SDLC prompts for threat modeling and resolve the first one for my
project."*

The library is in Spanish and English. You can also browse and copy every prompt on the website,
no account needed: https://www.lionsystems.com.mx/r/DMZ

There is an optional Pro plan ($9/month) for saved projects and per-prompt customization; the
prompts and the MCP server stay free.

Source and issues: https://github.com/dleon55/ai-sdlc-prompts
```

## 2. LinkedIn (español)

```text
Cuando copias un prompt de una página, lo lees antes de pegarlo.
Cuando un agente de IA lo pide por MCP, nadie lo lee: el agente lo ejecuta.

Por eso el servidor MCP de AI-SDLC Pro entrega cada uno de sus 112 prompts con su contrato de operación:
• hasta dónde puede actuar el agente (autonomía A0 a A3),
• qué herramientas puede usar,
• cuándo debe detenerse y preguntar,
• qué evidencia tiene que entregar.

Funciona en Claude Code, Claude Desktop y Cursor con una línea:
npx -y ai-sdlc-prompts-mcp

Gratis, de solo lectura, sin red. Código MIT y prompts CC BY 4.0.
Biblioteca completa, en español e inglés: https://www.lionsystems.com.mx/r/ZWc

#IA #IngenieriaDeSoftware #ClaudeCode #MCP
```

## 3. LinkedIn (inglés)

```text
When you copy a prompt from a website, you read it before you paste it.
When a coding agent fetches it over MCP, nobody reads it. The agent runs it.

So the AI-SDLC Pro MCP server ships each of its 112 prompts with an operating contract:
• how far the agent may go (autonomy A0–A3),
• which tools it may use,
• when it must stop and ask,
• what evidence it has to return.

Works in Claude Code, Claude Desktop and Cursor with one line:
npx -y ai-sdlc-prompts-mcp

Free, read-only, no network. MIT code, CC BY 4.0 prompts.
https://www.lionsystems.com.mx/r/9RW

#AI #SoftwareEngineering #MCP
```

## 4. X / Bluesky (inglés, una publicación)

En Bluesky, cambia el enlace por `https://www.lionsystems.com.mx/r/8yk`.

```text
New: an MCP server with 112 software-lifecycle prompts for Claude Code, Claude Desktop and Cursor.

Each prompt comes with its operating contract: autonomy ceiling, allowed tools, when to stop and ask, minimum evidence.

Free, read-only, no network:
npx -y ai-sdlc-prompts-mcp

https://www.lionsystems.com.mx/r/OnV
```

## 5. Reddit (r/ClaudeAI, r/mcp, r/cursor)

Antes de publicar, leer las reglas de cada subreddit sobre autopromoción. Publicar en uno por día,
desde una cuenta con historial, y responder los comentarios.

**Título:** I made a free MCP server that gives your agent 112 SDLC prompts *with* guardrails attached

```markdown
Prompts copied from a website get read before they're pasted. Prompts fetched over MCP get
executed. So every prompt in this server carries a short operating contract that
`resolve_prompt` appends by default: max autonomy (A0–A3), allowed tools, when to stop and ask,
and the minimum evidence the output must include.

- `npx -y ai-sdlc-prompts-mcp`
- 5 tools: `list_prompts`, `get_prompt`, `resolve_prompt`, `get_framework`, `recommend_next`
- stdio only, no network, read-only
- MIT code, CC BY 4.0 prompts, Spanish and English

Repo: https://github.com/dleon55/ai-sdlc-prompts

I'd like feedback on the contract format: is it useful or just noise for your agent?
```

## 6. Show HN

**Título:** Show HN: An MCP server whose prompts carry their own autonomy limits

**Enlace:** `https://github.com/dleon55/ai-sdlc-prompts`

**Primer comentario:**

```text
I maintain an open library of 112 structured prompts for the software lifecycle (Spanish and English).
When I exposed it over MCP I realized the risk changes: a human reads a prompt before pasting it, an
agent just runs it. So each prompt now travels with a contract (max autonomy A0–A3, allowed tools,
stop-and-ask conditions, minimum evidence) that the server appends by default.

It is read-only, stdio-only and opens no network. MIT code, CC BY 4.0 prompts. Install:
npx -y ai-sdlc-prompts-mcp

Happy to hear whether agents actually respect contracts like this in your experience.
```

## 7. Directorios de servidores MCP

Dar de alta el paquete una vez publicado. Cada directorio tiene su propio proceso; **leer sus
requisitos vigentes antes de enviar**, porque cambian seguido.

| Directorio | Cómo se agrega (verificar el día del alta) |
|---|---|
| MCP Registry oficial (`registry.modelcontextprotocol.io`) | Con su herramienta de publicación y un `server.json` que apunta al paquete de npm; requiere verificar la propiedad del paquete |
| Smithery (`smithery.ai`) | Alta desde su sitio con la cuenta de GitHub |
| Glama (`glama.ai/mcp/servers`) | Indexa repositorios públicos; se puede reclamar el servidor |
| PulseMCP (`pulsemcp.com`) | Formulario de envío |
| mcp.so | Formulario de envío o *issue* en su repositorio |

## Orden de publicación

1. Publicar el paquete (#199) y comprobar `npx -y ai-sdlc-prompts-mcp`.
2. Fusionar #258 (sección MCP en la portada). El despliegue es automático.
3. Día 1: Dev.to y LinkedIn (español e inglés).
4. Día 2: X/Bluesky y el primer subreddit.
5. Días 3 a 5: los otros subreddits, uno por día; Show HN un martes o miércoles por la mañana (hora de EE. UU.).
6. Semana 1: altas en los directorios.
7. Al cerrar la semana: anotar en este archivo las visitas por origen (`utm_source`) y las altas Pro.
