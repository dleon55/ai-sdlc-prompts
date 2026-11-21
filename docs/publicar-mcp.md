# Servidor MCP: dónde vive y cómo actualizar sus datos

El servidor MCP expone los 112 prompts, su contrato editorial y el grafo de
siguientes pasos a cualquier agente que hable Model Context Protocol — Claude
Code, Claude Desktop, Cursor. Está publicado en npm como
[`ai-sdlc-prompts-mcp`](https://www.npmjs.com/package/ai-sdlc-prompts-mcp) y en
el registro oficial de MCP como `io.github.dleon55/ai-sdlc-prompts`.

**Desde noviembre de 2026 el servidor vive en su propio repositorio público:
[dleon55/ai-sdlc-mcp](https://github.com/dleon55/ai-sdlc-mcp).** Se movió con
su historial; la 1.0.3 (21-nov-2026) ya se publicó desde el workflow
`publish.yml` de ese repo (tag `v*`), y el *trusted publisher* de npm solo
confía en él. La carpeta `mcp-server/` y el workflow `publish-mcp.yml` de este
repositorio se retiraron: versionar, probar, publicar en npm y registrar en
registry.modelcontextprotocol.io se documenta y se hace allá.

---

## Lo que sigue saliendo de aquí: `data/prompts-full.json`

El paquete embebe `data/prompts-full.json` (texto crudo de cada prompt con sus
placeholders, preámbulo del framework, contrato editorial y `TOKEN_REGISTRY`).
Lo genera `build.py`, que sigue siendo la **única** fuente de verdad del
parseo de los Markdown; el repo del MCP no reimplementa el parser.

`python build.py` ya no escribe ese archivo en ninguna carpeta del repo. Para
generarlo:

```bash
scripts/exportar-datos-mcp.sh ../ai-sdlc-mcp/data/prompts-full.json
```

(equivale a `AI_SDLC_MCP_DATA_OUT=<ruta> python build.py`).

### Al agregar o editar prompts

1. Fusionar el cambio de prompts aquí, en `main`.
2. En un clon de `dleon55/ai-sdlc-mcp`, en una rama nueva, correr el script
   de arriba apuntando a su `data/prompts-full.json`.
3. Abrir PR en `ai-sdlc-mcp` con el JSON regenerado (y la subida de versión
   que pida su propio proceso), fusionarlo y taggear `v<versión>` allá.

### Qué lo vigila aquí

- `tests/test_build_skills.py::test_paridad_con_el_mcp` genera el export en un
  temporal y comprueba que trae los mismos prompts que las skills.
- `tests/test_mcp_contract_parity.py` compara el contrato de operación del
  sitio contra `src/operatingContract.js` **del paquete publicado en npm**.
- `tests/test_licencia_coherente.py` verifica la licencia del paquete publicado
  (MIT AND CC-BY-4.0, con `LICENSE` incluido).

Las tres últimas usan la fixture `paquete_mcp` (`tests/conftest.py`), que hace
`npm pack ai-sdlc-prompts-mcp@latest`. Sin npm o sin red se omiten en local y
fallan en CI. Para probar contra un checkout local del MCP antes de publicar:
`AI_SDLC_MCP_PKG_DIR=../ai-sdlc-mcp python -m pytest tests/`.

---

## La licencia

El repositorio usa **licencia por alcance** (`docs/STRATEGY.md`, decisión del
2026-07-30: *el gate va sobre la plataforma, no sobre el texto*).

| Alcance | Licencia | Por qué |
|---|---|---|
| Los prompts (`ai_sdlc_pro_prompts/**`, `prompts-index.json`, el export `data/prompts-full.json`) | **CC BY 4.0** | El plan Free promete "copia ilimitada y para siempre". Permite uso comercial: sin eso, un freelancer no podría usarlos con un cliente. |
| El servidor MCP ([dleon55/ai-sdlc-mcp](https://github.com/dleon55/ai-sdlc-mcp)) | **MIT** | Instalar es reproducir y ejecutar es usar. Su `package.json` declara `"license": "MIT AND CC-BY-4.0"` porque embebe los prompts. |
| La plataforma (`build.py`, sitio generado, `backend/`, utilerías) | **Propietario** | Es lo que se vende. Que el código sea legible no otorga licencia de uso. |

> Redactado por criterio de ingeniería, no legal.
