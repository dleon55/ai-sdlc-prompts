# Publicar el servidor MCP en npm

El servidor MCP (`mcp-server/`) expone los 112 prompts, su contrato editorial y
el grafo de siguientes pasos a cualquier agente que hable Model Context
Protocol — Claude Code, Claude Desktop, Cursor. Está construido, probado en CI
y **nadie puede instalarlo**: hasta ahora `package.json` tenía `private: true`.

Esto importa más que una función nueva. `docs/STRATEGY.md` justifica toda la
decisión de monetización con esta frase:

> el texto ya es legible por cualquiera en GitHub o **vía el servidor MCP sin
> autenticación**

Mientras el paquete no exista, esa frase es falsa.

---

## La licencia (resuelta)

El repositorio usa **licencia por alcance**, porque el producto ya estaba
dividido así — `docs/STRATEGY.md`, decisión del 2026-07-30: *el gate va sobre
la plataforma, no sobre el texto*.

| Alcance | Licencia | Por qué |
|---|---|---|
| Los prompts (`ai_sdlc_pro_prompts/**`, `prompts-index.json`, `data/prompts-full.json`) | **CC BY 4.0** | El plan Free promete "copia ilimitada y para siempre". Permite uso comercial: sin eso, un freelancer no podría usarlos con un cliente, que es la persona con mayor disposición a pagar. |
| El servidor MCP (`mcp-server/`, sin `data/`) | **MIT** | Instalar es reproducir y ejecutar es usar. Sin permiso explícito, el paquete es ininstalable en términos legales. |
| La plataforma (`build.py`, sitio generado, `supabase/`, utilerías) | **Propietario** | Es lo que se vende. Que el código sea legible no otorga licencia de uso. |

`mcp-server/package.json` declara `"license": "MIT AND CC-BY-4.0"`, que es la
expresión SPDX correcta para un paquete cuyo código y contenido embebido tienen
licencias distintas.

**Lo que esto concede y lo que no.** Cualquiera puede usar, adaptar y
redistribuir los prompts, incluso comercialmente, dando crédito con enlace al
sitio. Nadie puede tomar `build.py` y el sitio generado para operar un servicio
equivalente. La atribución convierte cada reuso en un enlace de vuelta.

> Redactado por criterio de ingeniería, no legal. Antes de depender de la
> sección propietaria en una disputa real, conviene que la revise alguien con
> criterio legal.

---

## Procedimiento, una vez resuelta la licencia

### 1. Secreto de npm (una vez)

1. En npmjs.com → *Access Tokens* → **Generate New Token** → tipo **Automation**.
2. En GitHub → *Settings* → *Secrets and variables* → *Actions* → **New repository secret**:
   - Nombre: `NPM_TOKEN`
   - Valor: el token generado

### 2. Publicar

La publicación la dispara un tag, no un push a `main`: publicar es
irreversible — una versión de npm no se reemplaza, solo se deprecia.

```bash
git tag mcp-v1.0.0
git push origin mcp-v1.0.0
```

`.github/workflows/publish-mcp.yml` se encarga del resto y **aborta** si:

- `mcp-server/data/prompts-full.json` está desactualizado respecto a
  `python build.py` (evita publicar un catálogo viejo sin que nada avise);
- el tag no coincide con la versión de `package.json` (evita que quede en npm
  una versión distinta de la taggeada, imposible de rastrear después);
- fallan las pruebas.

### 3. Verificar

```bash
npx ai-sdlc-prompts-mcp
```

Debe quedarse esperando en stdin (es el transporte stdio de MCP), sin abrir red.

### 4. Anunciarlo en el sitio

Deliberadamente **no** se agregó todavía el bloque de instalación a
`index.html`: enlazar a un paquete de npm que no existe es peor que no
enlazarlo. Una vez publicado y verificado con el paso 3, agregarlo.

---

## Dependencias y alcance real

`mcp-server` no declara más que `@modelcontextprotocol/sdk` y `zod`. Todo lo
que aparece en las alertas de seguridad es **transitivo del SDK**, y conviene
saber qué es alcanzable antes de reaccionar a un aviso.

Este servidor usa **únicamente el transporte stdio**. Siguiendo los imports
desde sus dos puntos de entrada reales (`server/stdio.js`, `server/mcp.js`) se
alcanzan 16 archivos del SDK y estos paquetes externos:

    ajv, ajv-formats, zod, zod-to-json-schema

Es decir, la pila HTTP del SDK (`hono`, `@hono/node-server`,
`express-rate-limit` y su `ip-address`) **no se carga nunca**. Un aviso sobre
CORS, rate limiting o path traversal en `serve-static` no aplica aquí, porque
no hay servidor HTTP: el proceso habla por stdin/stdout y no abre red.

Lo que sí es alcanzable es `ajv` (valida los esquemas de entrada de cada tool)
y, por debajo, `fast-uri`.

**Importante sobre lo que recibe quien instala.** El paquete publicado no lleva
`package-lock.json` (ver `files` en `package.json`), así que cada instalación
resuelve su propio árbol desde los rangos declarados. `ajv` pide
`fast-uri: ^3.0.1` y `express-rate-limit` pide `ip-address: ^10.2.0`: una
instalación nueva toma la versión parchada por sí sola. Las alertas de
Dependabot se referían al lockfile **de este repositorio** — que afecta a la CI
y a quien clona, no a quien hace `npx`.

Para reproducir el análisis de alcance, seguir los imports desde
`node_modules/@modelcontextprotocol/sdk/dist/esm/server/{stdio,mcp}.js`.

El workflow de publicación corre `npm audit --audit-level=high` y **no publica**
con vulnerabilidades altas conocidas.

---

## Subir de versión

`data/prompts-full.json` se regenera con `python build.py`, así que **cualquier
cambio en los prompts cambia el paquete**. Al agregar o editar prompts:

1. `python build.py` y commitear `mcp-server/data/prompts-full.json`
2. Subir la versión en `mcp-server/package.json`
3. Taggear `mcp-v<version>`

Si se olvida el paso 1, la CI lo detiene.
