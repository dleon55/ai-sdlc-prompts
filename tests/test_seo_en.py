"""Issue #201: la mitad inglesa del catálogo necesita una URL indexable."""
from pathlib import Path
import html as html_lib
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://prompts.lionsystems.com.mx"


def _read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def _alternates(html):
    return dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', html))


def test_en_page_exists_with_english_head():
    import i18n_strings

    html = _read("en/index.html")
    assert '<html lang="en" data-lang="en" data-page-lang="en">' in html
    assert f'<link rel="canonical" href="{SITE}/en/">' in html
    assert '<meta property="og:locale" content="en_US">' in html
    assert _head(html) == _expected_head("en", html)


def _expected_head(lang, html):
    """Título y descripción que el generador debe poner en la página de `lang`,
    con `{n}` resuelto al número de prompts que la propia página declara."""
    import i18n_strings

    n = re.search(r'<meta name="description" content="(\d+) ', html).group(1)
    s = i18n_strings.LANDING_STRINGS[lang]
    return {"title": s["page_title"].format(n=n), "description": s["meta_description"].format(n=n)}


def _head(html):
    def meta(attr, name):
        return re.search(rf'<meta {attr}="{name}" content="([^"]*)">', html).group(1)

    title = re.search(r"<title>([^<]*)</title>", html).group(1)
    desc = meta("name", "description")
    # og:* y twitter:* deben repetir exactamente el título y la descripción.
    for attr, name, value in [("property", "og:title", title), ("property", "og:description", desc),
                              ("name", "twitter:title", title), ("name", "twitter:description", desc)]:
        assert html_lib.unescape(meta(attr, name)) == html_lib.unescape(value), name
    return {"title": html_lib.unescape(title), "description": html_lib.unescape(desc)}


def test_es_and_en_heads_are_not_mixed_and_fit_in_google():
    es_html, en_html = _read("index.html"), _read("en/index.html")
    es, en = _head(es_html), _head(en_html)
    assert es == _expected_head("es", es_html)
    assert en == _expected_head("en", en_html)
    assert es["title"] != en["title"] and es["description"] != en["description"]
    # Google corta el título hacia los 60 caracteres y la descripción hacia los 155.
    for head in (es, en):
        assert len(head["title"]) <= 60, head["title"]
        assert len(head["description"]) <= 155, head["description"]


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
