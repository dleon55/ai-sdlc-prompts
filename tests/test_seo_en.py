"""Issue #201: la mitad inglesa del catálogo necesita una URL indexable."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://prompts.lionsystems.com.mx"


def _read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def _alternates(html):
    return dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', html))


def test_en_page_exists_with_english_head():
    html = _read("en/index.html")
    assert '<html lang="en" data-lang="en" data-page-lang="en">' in html
    assert f'<link rel="canonical" href="{SITE}/en/">' in html
    assert '<meta property="og:locale" content="en_US">' in html
    assert "<title>AI-SDLC Pro — Software Engineering Prompt Library</title>" in html


def test_hreflang_reciprocal_between_es_and_en():
    expected = {"es": f"{SITE}/", "en": f"{SITE}/en/", "x-default": f"{SITE}/"}
    assert _alternates(_read("index.html")) == expected
    assert _alternates(_read("en/index.html")) == expected
    assert f'<link rel="canonical" href="{SITE}/">' in _read("index.html")


def test_en_landing_is_rendered_in_english():
    import i18n_strings

    en = i18n_strings.LANDING_STRINGS["en"]
    es = i18n_strings.LANDING_STRINGS["es"]
    html = _read("en/index.html")
    assert en["hero_title"] in html
    assert es["hero_title"] not in html


def test_en_page_relative_assets_climb_one_level():
    html = _read("en/index.html")
    assert 'href="favicon-32.png"' not in html
    assert 'src="apple-touch-icon.png"' not in html
    assert "var PROMPTS_TEXT_BASE = '../';" in html
    assert "var PROMPTS_TEXT_BASE = '';" in _read("index.html")


def test_en_page_keeps_full_catalog():
    es, en = _read("index.html"), _read("en/index.html")
    assert es.count('class="card"') == en.count('class="card"') > 0


def test_sitemap_lists_en_url_with_alternates():
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
    tree = ET.parse(ROOT / "sitemap.xml")
    urls = {u.find("s:loc", ns).text: u for u in tree.getroot().findall("s:url", ns)}
    assert f"{SITE}/en/" in urls
    for loc in (f"{SITE}/", f"{SITE}/en/"):
        alts = {l.get("hreflang"): l.get("href") for l in urls[loc].findall("x:link", ns)}
        assert alts == {"es": f"{SITE}/", "en": f"{SITE}/en/", "x-default": f"{SITE}/"}


def test_deploy_ships_en_page():
    wf = _read(".github/workflows/deploy.yml")
    assert "cp en/index.html dist/en/index.html" in wf
    assert "${D}/en/index.html" in wf
