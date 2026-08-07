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

## Bloqueo: la licencia

**Esto no se puede publicar tal como está, y no es un detalle de forma.**

`LICENSE` dice:

> No part of this Software may be reproduced, distributed, transmitted,
> displayed, modified, or adapted in any form or by any means […] without the
> prior written permission of LionSystems.
>
> UNAUTHORIZED USE PROHIBITED

Instalar un paquete de npm **es** reproducirlo; ejecutarlo **es** usarlo. Con
esta licencia, cada persona que corra `npx ai-sdlc-prompts-mcp` estaría en
violación, y `package.json` declara `"license": "UNLICENSED"`, que es
coherente con `LICENSE` pero incoherente con distribuir el paquete.

Además contradice la estrategia ya decidida. `docs/STRATEGY.md` define el plan
Free como *"los 112 prompts, copia ilimitada y para siempre, sin cuenta"*, y el
registro de decisiones del 2026-07-30 dice que el gate va sobre la plataforma y
no sobre el texto. La licencia dice lo contrario que el modelo de negocio.

### Qué hace falta decidir (es una decisión de negocio, no técnica)

| Opción | Qué implica |
|---|---|
| **Licencia permisiva para el contenido del paquete** (MIT/Apache-2.0, o una propia que permita uso y redistribución) | Coherente con el plan Free ya publicado. Es lo que la estrategia describe. |
| **Licencia propia de "uso permitido, redistribución no"** | Permite instalar y usar, prohíbe revender. Más cercana a la intención actual sin romper npm. |
| **No publicar** | Coherente con `LICENSE`, pero entonces conviene corregir `STRATEGY.md`, que afirma que el MCP ya sirve el texto sin autenticación. |

Sea cual sea, hay un defecto aparte que sí conviene corregir: el contacto de
licencias en `LICENSE` es `contacto@lionsystems.com.mx`, la dirección que ya se
confirmó que **rebota** (sin registros MX). Quien quiera licenciar el producto
hoy no tiene a dónde escribir.

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

## Subir de versión

`data/prompts-full.json` se regenera con `python build.py`, así que **cualquier
cambio en los prompts cambia el paquete**. Al agregar o editar prompts:

1. `python build.py` y commitear `mcp-server/data/prompts-full.json`
2. Subir la versión en `mcp-server/package.json`
3. Taggear `mcp-v<version>`

Si se olvida el paso 1, la CI lo detiene.
