"""Regression tests for safe Paddle Checkout build configuration."""

import pytest

import build


def test_paddle_defaults_disable_checkout(monkeypatch):
    monkeypatch.delenv("PADDLE_ENVIRONMENT", raising=False)
    monkeypatch.delenv("PADDLE_CLIENT_TOKEN", raising=False)
    monkeypatch.delenv("PADDLE_PRICE_ID", raising=False)

    monkeypatch.delenv("PADDLE_PRICE_AMOUNT_USD", raising=False)
    monkeypatch.delenv("PADDLE_PRICE_ID_ANNUAL", raising=False)
    monkeypatch.delenv("PADDLE_PRICE_AMOUNT_ANNUAL_USD", raising=False)

    assert build.paddle_public_config() == {
        "environment": "sandbox",
        "client_token": build.PADDLE_DISABLED_VALUE,
        "price_id": build.PADDLE_DISABLED_VALUE,
        # El monto viaja con el price id para que el precio cobrado y el
        # comunicado (sitio + terminos + reembolsos) no puedan divergir.
        "amount": "1",
        # Plan anual opcional: vacio = no se ofrece.
        "annual_price_id": "",
        "annual_amount": "",
    }


def test_paddle_accepts_live_values_only_in_production(monkeypatch):
    monkeypatch.setenv("PADDLE_ENVIRONMENT", "production")
    monkeypatch.setenv("PADDLE_CLIENT_TOKEN", "live_abc123")
    monkeypatch.setenv("PADDLE_PRICE_ID", "pri_abc123")

    assert build.paddle_public_config()["environment"] == "production"


def test_paddle_rejects_test_token_in_production(monkeypatch):
    monkeypatch.setenv("PADDLE_ENVIRONMENT", "production")
    monkeypatch.setenv("PADDLE_CLIENT_TOKEN", "test_abc123")
    monkeypatch.setenv("PADDLE_PRICE_ID", "pri_abc123")

    with pytest.raises(ValueError, match="live_"):
        build.paddle_public_config()


def test_amount_is_validated(monkeypatch):
    """Un monto malformado debe reventar el build, no llegar al sitio."""
    monkeypatch.setenv("PADDLE_PRICE_AMOUNT_USD", "nueve")
    with pytest.raises(ValueError):
        build.paddle_public_config()

    monkeypatch.setenv("PADDLE_PRICE_AMOUNT_USD", "9.999")
    with pytest.raises(ValueError):
        build.paddle_public_config()


def test_annual_plan_requires_id_and_amount_together(monkeypatch):
    """Un id sin monto pintaria un boton sin precio; un monto sin id
    abriria un checkout vacio. Se exigen juntos o ninguno."""
    monkeypatch.setenv("PADDLE_PRICE_ID_ANNUAL", "pri_01abc")
    monkeypatch.delenv("PADDLE_PRICE_AMOUNT_ANNUAL_USD", raising=False)
    with pytest.raises(ValueError):
        build.paddle_public_config()

    monkeypatch.delenv("PADDLE_PRICE_ID_ANNUAL", raising=False)
    monkeypatch.setenv("PADDLE_PRICE_AMOUNT_ANNUAL_USD", "90")
    with pytest.raises(ValueError):
        build.paddle_public_config()


def test_legal_pages_derive_price_from_the_same_config(monkeypatch):
    """El defecto que esto previene: cambiar el cobro y dejar terminos.html
    y reembolsos.html diciendo el precio viejo. Es el mismo error que ya
    ocurrio con el $499 de Gumroad en la documentacion."""
    monkeypatch.setenv("PADDLE_PRICE_AMOUNT_USD", "9")

    terminos = build.build_terminos_page()
    reembolsos = build.build_reembolsos_page()

    assert "9 USD al mes" in terminos
    assert "9 USD" in reembolsos
    assert "1 USD al mes" not in terminos
