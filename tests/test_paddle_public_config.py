"""Regression tests for safe Paddle Checkout build configuration."""

import pytest

import build


def test_paddle_defaults_disable_checkout(monkeypatch):
    monkeypatch.delenv("PADDLE_ENVIRONMENT", raising=False)
    monkeypatch.delenv("PADDLE_CLIENT_TOKEN", raising=False)
    monkeypatch.delenv("PADDLE_PRICE_ID", raising=False)

    assert build.paddle_public_config() == {
        "environment": "sandbox",
        "client_token": build.PADDLE_DISABLED_VALUE,
        "price_id": build.PADDLE_DISABLED_VALUE,
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
