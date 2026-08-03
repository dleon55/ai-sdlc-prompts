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
    assert "no hacemos reembolsos ni prorrateos después de los 14 días" in content
    assert "lo revisamos caso por caso" not in content
