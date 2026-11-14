"""Rutas Free, Pro y Enterprise medibles y sin contradicciones (issue #220).

Cada CTA de plan debe dejar rastro con el mismo vocabulario que las UTM del
CRM (`utm_product=ai-sdlc-pro`, `utm_plan=free|pro|enterprise`):

- Enterprise sale del dominio hacia el formulario de Odoo, asi que lleva las
  UTM en la URL.
- Free y Pro son enlaces internos; ahi las UTM en el href reiniciarian la
  sesion de GA4, de modo que el plan viaja en el evento de GA.
"""
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build  # noqa: E402


@pytest.fixture(scope="module")
def portada():
    return (ROOT / "index.html").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def portada_en():
    return (ROOT / "en" / "index.html").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def precios():
    return build.build_precios_page()


@pytest.fixture(scope="module")
def terminos():
    return build.build_terminos_page()


def _anclas(html):
    return re.findall(r"<a\b[^>]*>", html)


def test_plan_event_params_usa_el_vocabulario_de_las_utm():
    assert build.plan_event_params("free", "landing_hero") == (
        "{utm_product:'ai-sdlc-pro',utm_plan:'free',source:'landing_hero'}"
    )
    with pytest.raises(ValueError):
        build.plan_event_params("gold", "landing")
    with pytest.raises(ValueError):
        build.plan_event_params("pro", "landing');alert(1")


@pytest.mark.parametrize("pagina", ["portada", "portada_en"])
def test_ctas_free_de_la_portada_miden_el_plan(pagina, request):
    html = request.getfixturevalue(pagina)
    ctas_app = [a for a in _anclas(html) if 'href="/app"' in a]
    assert len(ctas_app) == 3, ctas_app
    fuentes = set()
    for a in ctas_app:
        assert "plan_cta_click" in a and "utm_plan:'free'" in a, a
        assert "utm_product:'ai-sdlc-pro'" in a, a
        fuentes.add(re.search(r"source:'([a-z_]+)'", a).group(1))
    assert fuentes == {"landing_nav", "landing_hero", "landing_final"}


@pytest.mark.parametrize("pagina", ["portada", "portada_en"])
def test_ctas_pro_y_enterprise_de_la_portada_miden_el_plan(pagina, request):
    html = request.getfixturevalue(pagina)
    anclas = _anclas(html)
    pro = [a for a in anclas if "pricing_cta_click" in a]
    assert pro and all("utm_plan:'pro'" in a and "utm_product:'ai-sdlc-pro'" in a for a in pro), pro
    enterprise = [a for a in anclas if "b2b_audit_cta_click" in a]
    assert len(enterprise) == 1
    a = enterprise[0]
    assert "utm_product=ai-sdlc-pro" in a and "utm_plan=enterprise" in a and "utm_content=landing" in a
    assert "utm_plan:'enterprise'" in a


def test_ctas_de_precios_miden_el_plan(precios):
    assert "pxTrack(\"checkout_open_requested\",{utm_product:'ai-sdlc-pro',utm_plan:'pro',source:'pricing'});" in precios
    enterprise = [a for a in _anclas(precios) if "b2b_audit_cta_click" in a]
    assert len(enterprise) == 1
    a = enterprise[0]
    assert "utm_product=ai-sdlc-pro" in a and "utm_plan=enterprise" in a and "utm_content=pricing" in a
    assert "utm_plan:'enterprise'" in a


def test_enlaces_al_sitio_corporativo_llevan_utm_de_producto(portada, precios, terminos):
    for html in (portada, precios, terminos):
        for a in _anclas(html):
            m = re.search(r'href="(https://(?:www\.)?lionsystems\.com\.mx[^"]*)"', a)
            if m:
                assert "utm_product=ai-sdlc-pro" in m.group(1), m.group(1)


def test_terminos_nombran_el_plan_como_en_precios(terminos, precios):
    assert "Individual" not in terminos
    assert "El plan Pro cuesta" in terminos and "The Pro plan costs" in terminos
    assert "Plan Pro" in precios


def test_terminos_respetan_la_promesa_del_programa_fundador(terminos, precios):
    """Precios promete congelar el precio a los fundadores; los terminos no
    pueden decir solo que "el precio puede cambiar"."""
    assert "Programa Fundador" in precios
    assert build.FUNDADOR_TERMINOS_ES in terminos
    assert build.FUNDADOR_TERMINOS_EN in terminos
