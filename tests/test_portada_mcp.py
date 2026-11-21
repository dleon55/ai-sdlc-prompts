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


def test_portada_enlaza_al_repo_del_servidor_mcp():
    """El código del MCP vive en dleon55/ai-sdlc-mcp desde nov-2026."""
    for rel in ("index.html", "en/index.html"):
        assert "https://github.com/dleon55/ai-sdlc-mcp" in _read(rel), rel


def test_el_fragmento_de_config_usa_el_paquete_publicado():
    import build

    assert "ai-sdlc-prompts-mcp" in build.MCP_CONFIG_SNIPPET_HTML
    assert build.MCP_NPM_URL == "https://www.npmjs.com/package/ai-sdlc-prompts-mcp"
