#!/usr/bin/env python3
"""
tests/test_subscriptions_schema.py — Contrato de regresión para
supabase/subscriptions.sql

Mismo riesgo central que user_trial en trial_gate.sql: subscriptions no
debe tener ninguna política RLS que permita a un usuario escribir su
propia fila. Si la tuviera, cualquiera podría auto-otorgarse
status='active' desde la consola del navegador con el anon key público,
sin haber pagado nada -- la única vía de escritura debe ser la Edge
Function del webhook de Paddle (que usa la service role key).
"""
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SCHEMA = (PROJECT_ROOT / "supabase" / "subscriptions.sql").read_text(encoding="utf-8")
WEBHOOK_FN = (
    PROJECT_ROOT / "supabase" / "functions" / "paddle-webhook" / "index.ts"
).read_text(encoding="utf-8")


def _policies_on_table(table):
    pattern = re.compile(
        r"create policy\s+\"[^\"]*\"\s+on\s+" + re.escape(table) + r"\s+for\s+(\w+)",
        re.IGNORECASE,
    )
    return [m.group(1).lower() for m in pattern.finditer(SCHEMA)]


def test_subscriptions_has_rls_enabled():
    assert "alter table subscriptions enable row level security" in SCHEMA


def test_subscriptions_has_no_client_write_policy():
    """Negativo a propósito: solo 'select' es aceptable."""
    policies = _policies_on_table("subscriptions")
    assert policies, "subscriptions no tiene ninguna política RLS -- revisar RLS habilitado"
    forbidden = {"update", "insert", "delete", "all"}
    found_forbidden = forbidden.intersection(policies)
    assert not found_forbidden, (
        f"subscriptions tiene política(s) de {found_forbidden} para el cliente -- "
        "esto permitiría a un usuario auto-otorgarse una suscripción activa sin pagar"
    )
    assert policies == ["select"], f"Se esperaba solo ['select'], se encontró {policies}"


def test_check_trial_status_checks_subscription_before_trial():
    """El check_trial_status() de subscriptions.sql (que reemplaza al de
    trial_gate.sql) debe revisar la suscripción ANTES de aplicar el límite
    de prueba gratuita -- si no, un usuario que ya pagó podría quedar
    bloqueado por el muro de prueba vencida."""
    match = re.search(
        r"create (or replace )?function check_trial_status\(\)"
        r"[\s\S]*?\$\$;",
        SCHEMA,
        re.IGNORECASE,
    )
    assert match, "No se encontró el check_trial_status() actualizado en subscriptions.sql"
    body = match.group(0)
    sub_check_pos = body.lower().find("from subscriptions")
    trial_check_pos = body.lower().find("from user_trial")
    assert sub_check_pos != -1, "no revisa la tabla subscriptions"
    assert trial_check_pos != -1, "no revisa la tabla user_trial"
    assert sub_check_pos < trial_check_pos, (
        "debe revisar subscriptions ANTES que user_trial -- si no, un usuario "
        "con suscripción activa pero prueba vencida quedaría bloqueado"
    )


def test_paddle_webhook_verifies_signature_before_parsing_payload():
    """Vulnerabilidad a evitar: si la función procesara el payload antes de
    verificar la firma HMAC, cualquiera podría mandar un POST falso
    diciendo 'ya pagué' y auto-otorgarse acceso ilimitado sin pagar."""
    sig_check_pos = WEBHOOK_FN.find("timingSafeEqual")
    json_parse_pos = WEBHOOK_FN.find("JSON.parse(rawBody)")
    assert sig_check_pos != -1, "no se encontró la verificación de firma"
    assert json_parse_pos != -1, "no se encontró el parseo del payload"
    assert sig_check_pos < json_parse_pos, (
        "la verificación de firma debe ocurrir ANTES de parsear/usar el payload"
    )


def test_paddle_webhook_uses_service_role_not_anon_key():
    """La Edge Function debe escribir con la service role key (bypassa
    RLS por diseño, ya que subscriptions no tiene política de escritura de
    cliente) -- si usara la anon key, ningún insert/update funcionaría."""
    assert "SUPABASE_SERVICE_ROLE_KEY" in WEBHOOK_FN
    assert "SUPABASE_ANON_KEY" not in WEBHOOK_FN


def test_paddle_webhook_rejects_stale_signatures_and_deduplicates_events():
    assert "MAX_SIGNATURE_AGE_SECONDS" in WEBHOOK_FN
    assert "Math.abs(now - timestamp)" in WEBHOOK_FN
    assert "paddle_webhook_events" in SCHEMA
    assert 'rpc("apply_paddle_subscription_event"' in WEBHOOK_FN
    assert "Already processed" in WEBHOOK_FN


def test_paddle_webhook_events_are_not_client_writable():
    assert "create table if not exists paddle_webhook_events" in SCHEMA
    assert "alter table paddle_webhook_events enable row level security" in SCHEMA
    assert _policies_on_table("paddle_webhook_events") == []


def test_paddle_webhook_transaction_is_atomic_and_orders_events():
    assert "for update" in SCHEMA.lower()
    assert "last_event_occurred_at" in SCHEMA
    assert "on conflict (event_id) do nothing" in SCHEMA.lower()
    assert "revoke execute on function apply_paddle_subscription_event" in SCHEMA.lower()


def test_unlinked_subscription_event_fails_instead_of_being_marked_done():
    """Un evento subscription.* sin user_id cuya suscripcion no existe
    localmente NO puede marcarse como procesado.

    Si se marcara, la Edge Function devolveria 200, Paddle dejaria de
    reintentar, el cliente quedaria sin el acceso que pago, y ni un replay
    manual lo arreglaria -- todo con el tablero en verde. Como Paddle no
    garantiza el orden de entrega, un subscription.updated puede llegar
    antes que el created que si trae el user_id, asi que hay que fallar
    ruidosamente para forzar el reintento."""
    lowered = SCHEMA.lower()

    # Se mide cuantas filas toco el UPDATE del camino sin user_id.
    assert "get diagnostics" in lowered
    assert "row_count" in lowered

    # 0 filas se desambigua: solo es error si ademas no existe la fila.
    assert "affected = 0" in lowered
    assert "not exists" in lowered

    # Y ese caso lanza excepcion, que revierte el insert en
    # paddle_webhook_events y hace que el webhook responda 500.
    unlinked = re.search(
        r"if\s+affected\s*=\s*0.*?raise\s+exception", lowered, re.DOTALL
    )
    assert unlinked, "el camino sin fila local debe terminar en raise exception"


# ── Contrato del frontend de suscripción (issue del pago sin indicador) ──
# Un cliente pagó, Paddle confirmó por correo, y la app nunca mostró nada.
# Estos tests fijan las cuatro piezas que faltaban para que eso no vuelva.

INDEX_HTML = (PROJECT_ROOT / "index.html").read_text(encoding="utf-8")
PRECIOS_HTML = (PROJECT_ROOT / "precios.html").read_text(encoding="utf-8")


def test_supabase_session_is_persisted_explicitly():
    """Sin persistSession la sesión vive solo en memoria: cada recarga
    vuelve anónimo, auth.uid() es null y check_trial_status() nunca
    encuentra la suscripción de alguien que YA PAGÓ."""
    for name, html in (("index.html", INDEX_HTML), ("precios.html", PRECIOS_HTML)):
        compact = html.replace(" ", "")
        assert "persistSession:true" in compact, f"{name} sin persistSession"
        assert "autoRefreshToken:true" in compact, f"{name} sin autoRefreshToken"


def test_app_reads_subscribed_and_shows_pro_badge():
    """check_trial_status() ya devolvía 'subscribed', pero la app solo leía
    'active' y lo descartaba -- por eso no existía indicador de Pro."""
    assert "subscribed" in INDEX_HTML
    assert "setProState" in INDEX_HTML
    assert "auth-pro-badge" in INDEX_HTML


def test_pricing_page_handles_checkout_return_and_waits_for_webhook():
    """El webhook de Paddle es asíncrono: una sola consulta al volver del
    checkout llega antes que la escritura y deja al comprador viendo
    'Suscribirme'. Debe sondear, y al rendirse confirmar que el pago sí
    se recibió en vez de dar a entender que se perdió."""
    assert "checkout=success" in PRECIOS_HTML
    assert "pxPollPro" in PRECIOS_HTML
    assert "setTimeout" in PRECIOS_HTML
    assert "Pago recibido" in PRECIOS_HTML


def test_oauth_returns_to_the_page_the_user_started_from():
    """Sin redirectTo, Supabase devuelve siempre al Site URL: quien iniciaba
    sesión desde /precios.html aterrizaba en la landing y abandonaba."""
    assert "redirectTo" in INDEX_HTML
    assert "redirectTo" in PRECIOS_HTML
    assert "pxSignIn" in PRECIOS_HTML


def test_oauth_tokens_never_accumulate_in_the_url():
    """redirectTo con window.location.href arrastra el #access_token= que
    Supabase acaba de dejar, asi que cada login apila otro token: se
    observaron URLs en produccion con TRES access_token, refresh_token y
    provider_token de GitHub encadenados, visibles en la barra de
    direcciones, el historial y cualquier captura de pantalla."""
    assert "redirectTo: window.location.href" not in INDEX_HTML, (
        "redirectTo no debe incluir el hash -- apila tokens en cada login"
    )
    for name, html in (("index.html", INDEX_HTML), ("precios.html", PRECIOS_HTML)):
        assert "replaceState" in html, f"{name} no limpia el hash tras consumir los tokens"
        assert "access_token=" in html, f"{name} no detecta el fragmento a limpiar"


def test_sign_out_is_discoverable():
    """El nombre de usuario a secas no se lee como boton de salida: se
    reporto no encontrar donde cerrar sesion."""
    assert "aria-label" in INDEX_HTML
    assert "Cerrar sesión" in INDEX_HTML


# ── Muro medido del modo guiado (propuesta de monetización) ──

def test_guided_mode_is_metered_not_free_forever():
    """El único muro de pago era 'crear un segundo proyecto': un disparador
    administrativo que un dev individual puede no tocar nunca, mientras el
    modo guiado -- asesoría, el valor recurrente -- era gratis e ilimitado.
    El muro debe estar donde se concentra el valor."""
    assert "GUIDED_FREE_USES" in INDEX_HTML
    assert "AI_SDLC_guided_uses" in INDEX_HTML
    assert "guidedFreeUsesLeft" in INDEX_HTML


def test_guided_wall_appears_only_after_the_value_was_felt():
    """Cobrar en el primer uso mataría el 'aha'. Las primeras aperturas son
    libres incluso sin cuenta, y con Pro no hay contador."""
    assert "if (isProUser()) { showGuidedModal(); return; }" in INDEX_HTML
    assert "if (guidedFreeUsesLeft() > 0)" in INDEX_HTML


def test_guided_quota_is_announced_before_running_out():
    """Toparse con un muro sin verlo venir se lee como cambio de reglas."""
    assert "renderGuidedQuotaNotice" in INDEX_HTML
    assert "guided-quota" in INDEX_HTML


def test_guided_gate_fails_open_on_error():
    """Mismo principio que el resto del muro: nunca bloquear a un usuario
    real por una falla transitoria de red o del SDK."""
    assert ".catch(function() { showGuidedModal(); })" in INDEX_HTML
