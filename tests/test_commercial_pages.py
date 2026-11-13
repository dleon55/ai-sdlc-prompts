"""Regression coverage for public commercial and legal generated pages."""

from pathlib import Path
import re

import build


ROOT = Path(__file__).resolve().parent.parent


def _read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def test_legal_pages_use_the_official_support_address():
    assert build.LEGAL_CONTACT_EMAIL == "soporte@lionsystems.com.mx"
    for page in ("terminos.html", "privacidad.html", "reembolsos.html"):
        content = _read(page)
        assert "soporte@lionsystems.com.mx" in content
        assert "dleon555@live.com.mx" not in content


def test_pricing_page_discloses_subscription_terms_before_checkout():
    content = _read("precios.html")
    for fragment in (
        "La suscripción se renueva mensualmente hasta que la canceles.",
        'href="/terminos.html"',
        'href="/privacidad.html"',
        'href="/reembolsos.html"',
        "soporte@lionsystems.com.mx",
        "https://www.googletagmanager.com/gtag/js",
    ):
        assert fragment in content


def test_commercial_ctas_and_events_do_not_include_personal_data():
    landing = _read("index.html")
    pricing = _read("precios.html")

    assert "ai-sdlc-pro-product-auditoria" in landing
    assert "ai-sdlc-pro-product-auditoria" in pricing
    for event in (
        "pricing_cta_click",
        "b2b_audit_cta_click",
        "pricing_view",
        "checkout_open_requested",
        "checkout_login_required",
    ):
        assert event in landing or event in pricing
    assert "email:" not in pricing
    tracked_calls = re.findall(r"pxTrack\([^;]+\);", pricing)
    assert tracked_calls
    assert all("user_id" not in call and "email" not in call for call in tracked_calls)


def test_refund_policy_has_a_single_non_discretionary_post_window_rule():
    content = _read("reembolsos.html")
    assert "No hay reembolsos una vez activada la suscripción" in content
    assert "lo revisamos caso por caso" not in content


def test_refund_policy_is_one_and_the_same_in_terms_and_refunds():
    """Decisión del titular (2026-11-02): sin reembolsos salvo cargo
    duplicado o error técnico comprobable. Términos y reembolsos citan el
    mismo texto; no queda rastro de la ventana de 14 días ni del plazo de
    respuesta de 2 días hábiles."""
    terminos, reembolsos = build.build_terminos_page(), build.build_reembolsos_page()
    for html in (terminos, reembolsos):
        assert build.POLITICA_REEMBOLSO_ES in html
        assert build.POLITICA_REEMBOLSO_EN in html
        assert "sin perjuicio de los derechos que la ley aplicable o los términos de compra de Paddle" in html
        for viejo in ("14 días", "14-day", "14 days", "2 días hábiles", "2 business days", "sin preguntas"):
            assert viejo not in html, viejo
    assert "soporte@lionsystems.com.mx" in reembolsos


def test_pricing_page_has_no_struck_through_list_price():
    """El "antes $19" era un ancla de marketing que nunca se cobró."""
    precios = build.build_precios_page()
    for viejo in ("antes $19", "was $19", "Precio de lista", "List price", "px-anchor"):
        assert viejo not in precios, viejo


def test_ninguna_pagina_promete_renovar_la_prueba_cada_semana():
    """Spec E1 (13-nov-2026): la prueba Pro es 1 semana + 1 renovación. Ninguna
    página publicada puede seguir prometiendo la renovación semanal sin fin
    del piloto."""
    import pathlib
    raiz = pathlib.Path(__file__).resolve().parent.parent
    prohibidas = (
        "renovar cada semana", "renewing weekly for as long",
        "mientras dure el piloto", "mientras dure el periodo de piloto",
        "for as long as the pilot", "1 semana, renovable", "1 week, renewable",
    )
    for nombre in ("index.html", "en/index.html", "precios.html", "terminos.html", "privacidad.html"):
        html = (raiz / nombre).read_text(encoding="utf-8")
        for frase in prohibidas:
            assert frase not in html, f"{nombre} aún promete: {frase!r}"
    precios = (raiz / "precios.html").read_text(encoding="utf-8")
    assert "1 semana + 1 renovación" in precios and "1 week + 1 renewal" in precios
    terminos = (raiz / "terminos.html").read_text(encoding="utf-8")
    assert "renovable una sola vez" in terminos and "renewable once" in terminos
