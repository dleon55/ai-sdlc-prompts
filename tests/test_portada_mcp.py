"""Issue #200: la portada anuncia el servidor MCP en los dos idiomas."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_portada_es_y_en_anuncian_el_servidor_mcp():
    import i18n_strings

    for rel, lang in (("index.html", "es"), ("en/index.html", "en")):
        html = _read(rel)
        assert '<section class="landing-mcp" id="mcp">' in html, rel
        assert i18n_strings.LANDING_STRINGS[lang]["mcp_title"] in html, rel
        assert "&quot;ai-sdlc-prompts-mcp&quot;" in html, rel
        assert "https://www.npmjs.com/package/ai-sdlc-prompts-mcp" in html, rel


def test_el_nombre_del_paquete_coincide_con_mcp_server():
    import json

    pkg = json.loads(_read("mcp-server/package.json"))
    assert pkg["name"] == "ai-sdlc-prompts-mcp"
