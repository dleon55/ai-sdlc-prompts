"""Brechas transversales de cobro (issue #232).

T1 identidad legal e impuestos, T3 reembolsos (Edge Function), T4 guardas
de precio y de centinela, T5 alertas, T7 conversión. Casi todo son
comprobaciones estáticas sobre la salida de build.py y sobre las fuentes
que no se pueden ejecutar aquí (Edge Function en Deno, workflow de CI); lo
ejecutable (script de smoke, salida del build) se ejecuta de verdad.
"""

import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest

import build


ROOT = Path(__file__).resolve().parent.parent
BUILD_SRC = (ROOT / "build.py").read_text(encoding="utf-8")
EDGE_SRC = (ROOT / "supabase" / "functions" / "paddle-webhook" / "index.ts").read_text(encoding="utf-8")
ALERTAS_SRC = (ROOT / "supabase" / "functions" / "paddle-webhook" / "alertas.ts").read_text(encoding="utf-8")
WORKFLOW = (ROOT / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")
SCRIPT = ROOT / "scripts" / "verificar-precio-publicado.sh"
DOCS_PADDLE = (ROOT / "docs" / "paddle-integration.md").read_text(encoding="utf-8")

PAGINAS_CON_PRECIO = ("precios", "terminos", "reembolsos")


def _read(name):
    return (ROOT / name).read_text(encoding="utf-8")


def _paginas_en_memoria():
    """Las tres legales + precios generadas con la config vigente del
    proceso. En memoria y no desde disco: otras pruebas regeneran los
    estáticos a mitad de la corrida (ver ofertas_structured_data)."""
    return {
        "precios": build.build_precios_page(),
        "terminos": build.build_terminos_page(),
        "privacidad": build.build_privacidad_page(),
        "reembolsos": build.build_reembolsos_page(),
    }


# ── T1: identidad legal desde un solo dict ───────────────────────────────

def test_legal_entity_is_the_single_source_of_identity():
    e = build.LEGAL_ENTITY
    assert e["nombre"] == "DAVID LEON GOMEZ"
    assert e["rfc"] == "LEGD870627K11"
    assert e["rfc"] in e["responsable"] and e["rfc"] in e["responsable_en"]
    assert e["nombre_comercial"] in e["responsable"]
    # Sin domicilio hasta que el titular elija uno de notificaciones. No se
    # inventa: las páginas lo omiten.
    assert e["domicilio"] is None
    assert e["correo_privacidad"] == "privacidad@lionsystems.com.mx"
    assert e["correo_soporte"] == "soporte@lionsystems.com.mx"
    assert e["actualizado"] == "18 de octubre de 2026"
    nombres = [x["nombre"] for x in e["encargados"]]
    for encargado in ("Paddle", "Supabase", "GitHub", "Google Analytics"):
        assert encargado in nombres
    # Los alias que usan páginas y pruebas derivan del dict, no son copia.
    assert build.LEGAL_CONTACT_EMAIL == e["correo_soporte"]
    assert build.LEGAL_PRIVACY_EMAIL == e["correo_privacidad"]
    assert build.LEGAL_ENTITY_NAME_ES == e["responsable"]
    assert build.LEGAL_LAST_UPDATED_ES == e["actualizado"]


def test_identity_literals_only_live_inside_legal_entity():
    """Si el RFC o el nombre fiscal aparecen fuera del dict, hay una segunda
    copia que puede divergir: exactamente lo que #225/#228 corrigieron."""
    bloque = re.search(r"^LEGAL_ENTITY = \{\n.*?^\}\n", BUILD_SRC, re.S | re.M)
    assert bloque, "no se encontró el bloque LEGAL_ENTITY en build.py"
    for literal in ("LEGD870627K11", "DAVID LEON GOMEZ", "privacidad@lionsystems.com.mx"):
        assert BUILD_SRC.count(literal) == bloque.group(0).count(literal), (
            f"{literal!r} aparece fuera de LEGAL_ENTITY"
        )


def test_legal_pages_render_responsable_processors_and_date():
    paginas = _paginas_en_memoria()
    e = build.LEGAL_ENTITY
    for slug in ("terminos", "privacidad"):
        html = paginas[slug]
        assert e["responsable"] in html
        assert e["responsable_en"] in html
    for slug in ("terminos", "privacidad", "reembolsos"):
        html = paginas[slug]
        assert "Última actualización: " + e["actualizado"] in html
        assert "Last updated: " + e["actualizado_en"] in html
        for prohibido in ("S.A. de C.V.", "Mina 210", "PENDIENTE", "[PENDIENTE"):
            assert prohibido not in html, f"{slug}: publica {prohibido!r}"

    privacidad = paginas["privacidad"]
    for encargado in e["encargados"]:
        assert "<strong>" + encargado["nombre"] + "</strong> — " + encargado["es"] in privacidad
        assert "<strong>" + encargado["nombre"] + "</strong> — " + encargado["en"] in privacidad
    assert e["correo_privacidad"] in privacidad
    assert e["correo_soporte"] in privacidad
    assert "Ley Federal de Protección de Datos Personales" in privacidad


def test_privacy_notice_cites_the_2025_law_not_the_extinct_inai():
    """La LFPDPPP de 2010 fue abrogada por la ley publicada en el DOF el 20 de
    marzo de 2025, y el INAI se extinguió: sus funciones en datos en posesión
    de particulares pasaron a la Secretaría Anticorrupción y Buen Gobierno.
    Remitir al INAI o al Reglamento de la ley abrogada es afirmar algo falso."""
    paginas = _paginas_en_memoria()
    for slug, html in paginas.items():
        for prohibido in ("INAI", "su Reglamento", "its Regulations", "Lineamientos del Aviso"):
            assert prohibido not in html, f"{slug}: cita {prohibido!r}"
    for slug in ("privacidad", "terminos", "reembolsos"):
        disco = _read(slug + ".html")
        assert "INAI" not in disco and "su Reglamento" not in disco, f"{slug}.html en disco"
    privacidad = paginas["privacidad"]
    assert "publicada en el DOF el 20 de marzo de 2025" in privacidad
    assert "published in the Official Gazette (DOF) on March 20, 2025" in privacidad
    assert "Secretaría Anticorrupción y Buen Gobierno" in privacidad
    assert "Secretariat of Anti-Corruption and Good Governance" in privacidad


def test_privacy_notice_no_longer_claims_a_local_copy_counter():
    """Ya no existe contador local de copias (copiar es libre e ilimitado);
    afirmarlo era describir un dato que no se recaba."""
    privacidad = build.build_privacidad_page()
    for frase in ("contador local", "contador de copias", "local counter", "copy counter"):
        assert frase not in privacidad


def test_tax_note_is_shared_by_pricing_terms_and_refunds():
    paginas = _paginas_en_memoria()
    for slug in PAGINAS_CON_PRECIO:
        html = paginas[slug]
        assert build.NOTA_IMPUESTOS_ES in html, slug
        assert build.NOTA_IMPUESTOS_EN in html, slug
    for frase in ("antes de impuestos", "IVA", "No emitimos CFDI", "comprobante de pago"):
        assert frase in build.NOTA_IMPUESTOS_ES
    for frase in ("before taxes", "VAT", "We do not issue a CFDI", "proof of payment"):
        assert frase in build.NOTA_IMPUESTOS_EN


def test_refund_tax_sentence_does_not_promise_a_full_refund_for_every_case():
    """La política también reembolsa periodos sin servicio por falla nuestra,
    que pueden ser parciales: la frase de impuestos no puede prometer «el
    importe completo que pagaste» para cualquier reembolso aprobado. Lo
    verdadero en todos los casos es que el impuesto se devuelve en
    proporción a lo reembolsado."""
    html = build.build_reembolsos_page()
    assert "importe completo que pagaste, impuestos incluidos" not in html
    assert "full amount you paid, taxes included" not in html
    assert "el impuesto correspondiente al importe reembolsado" in html
    assert "the tax charged on the refunded amount" in html


# ── T4: el precio publicado es uno solo ──────────────────────────────────

def test_price_meta_and_prose_agree_on_the_three_priced_pages(monkeypatch):
    monkeypatch.setenv("PADDLE_PRICE_AMOUNT_USD", "9")
    paginas = _paginas_en_memoria()
    for slug in PAGINAS_CON_PRECIO:
        html = paginas[slug]
        assert '<meta name="precio-mensual-usd" content="9">' in html, slug
        assert re.search(r"(^|[^0-9.])9 USD", html), slug
        assert '<meta name="precio-mensual-usd" content="1">' not in html
    # privacidad no cita precio: sin meta, el smoke test no la revisa.
    assert "precio-mensual-usd" not in paginas["privacidad"]


def test_published_pages_on_disk_agree_with_each_other():
    metas = set()
    for slug in PAGINAS_CON_PRECIO:
        m = re.search(r'<meta name="precio-mensual-usd" content="([^"]+)">', _read(slug + ".html"))
        assert m, f"{slug}.html sin meta de precio"
        metas.add(m.group(1))
    assert len(metas) == 1, f"las páginas publican precios distintos: {metas}"


@pytest.mark.skipif(shutil.which("curl") is None, reason="el script usa curl")
def test_price_smoke_script_passes_and_fails_for_real(tmp_path, monkeypatch):
    """Se ejecuta el script de verdad contra archivos locales (curl file://)
    con el build de 9 USD: pasa con 9, falla con 7 y falla sin meta."""
    monkeypatch.setenv("PADDLE_PRICE_AMOUNT_USD", "9")
    paginas = _paginas_en_memoria()
    for slug in PAGINAS_CON_PRECIO:
        (tmp_path / f"{slug}.html").write_text(paginas[slug], encoding="utf-8")

    def correr(esperado):
        env = dict(os.environ, PADDLE_PRICE_AMOUNT_USD=esperado, SITIO_URL=tmp_path.as_uri())
        return subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)

    ok = correr("9")
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "PRECIO_OK" in ok.stdout

    mal = correr("7")
    assert mal.returncode == 1
    assert "PRECIO_ERROR" in mal.stdout and "7 USD" in mal.stdout

    sin_meta = paginas["terminos"].replace('<meta name="precio-mensual-usd" content="9">\n', "")
    (tmp_path / "terminos.html").write_text(sin_meta, encoding="utf-8")
    viejo = correr("9")
    assert viejo.returncode == 1
    assert "no declara" in viejo.stdout


@pytest.mark.skipif(shutil.which("curl") is None, reason="el script usa curl")
def test_price_smoke_script_also_checks_the_annual_price(tmp_path, monkeypatch):
    """Producción vende también el plan anual: su precio publicado debe ser
    el que cobra Paddle (PADDLE_PRICE_AMOUNT_ANNUAL_USD), con la misma
    tolerancia a espacios que tiene build.py al leer la variable."""
    monkeypatch.setenv("PADDLE_PRICE_AMOUNT_USD", "9")
    monkeypatch.setenv("PADDLE_PRICE_ID_ANNUAL", "pri_02anual")
    monkeypatch.setenv("PADDLE_PRICE_AMOUNT_ANNUAL_USD", "90")
    paginas = _paginas_en_memoria()
    assert '<meta name="precio-anual-usd" content="90">' in paginas["precios"]
    for slug in ("terminos", "reembolsos", "privacidad"):
        assert "precio-anual-usd" not in paginas[slug], slug
    for slug in PAGINAS_CON_PRECIO:
        (tmp_path / f"{slug}.html").write_text(paginas[slug], encoding="utf-8")

    def correr(mensual, anual):
        env = dict(os.environ, PADDLE_PRICE_AMOUNT_USD=mensual, SITIO_URL=tmp_path.as_uri())
        env.pop("PADDLE_PRICE_AMOUNT_ANNUAL_USD", None)
        if anual is not None:
            env["PADDLE_PRICE_AMOUNT_ANNUAL_USD"] = anual
        return subprocess.run(["bash", str(SCRIPT)], env=env, capture_output=True, text=True)

    ok = correr("9", "90")
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "anual" in ok.stdout
    # Espacios en la variable de GitHub: build.py los recorta; el smoke
    # también, o fallaría un deploy correcto.
    assert correr(" 9 ", " 90\n").returncode == 0

    mal = correr("9", "80")
    assert mal.returncode == 1
    assert "80 USD" in mal.stdout

    # La página ofrece un anual que la configuración ya no cobra.
    sin_anual = correr("9", "")
    assert sin_anual.returncode == 1
    assert "precio-anual-usd" in sin_anual.stdout

    # La configuración cobra un anual que la página no publica.
    viejo = paginas["precios"].replace('<meta name="precio-anual-usd" content="90">\n', "")
    (tmp_path / "precios.html").write_text(viejo, encoding="utf-8")
    assert correr("9", "90").returncode == 1


def test_price_smoke_script_is_executable_and_wired_into_deploy():
    assert SCRIPT.stat().st_mode & stat.S_IXUSR, "scripts/verificar-precio-publicado.sh sin bit de ejecución"
    paso = WORKFLOW.index("scripts/verificar-precio-publicado.sh")
    # Corre en el job de GCP, después del reemplazo atómico y del smoke
    # test existente: lo que se compara es lo que ya sirve nginx.
    assert paso > WORKFLOW.index("deploy-gcp:")
    assert paso > WORKFLOW.index("Atomic replace in production dir")
    assert paso > WORKFLOW.index("Smoke test GCP production")
    assert paso < WORKFLOW.index("Cleanup SSH key")
    bloque = WORKFLOW[WORKFLOW.index("Smoke test precio publicado"):paso]
    assert "vars.PADDLE_PRICE_AMOUNT_USD" in bloque
    assert "PADDLE_PRICE_AMOUNT_ANNUAL_USD: ${{ vars.PADDLE_PRICE_AMOUNT_ANNUAL_USD }}" in bloque
    assert "SITIO_URL: https://prompts.lionsystems.com.mx" in bloque


def test_build_exits_non_zero_with_sentinel_token_in_production():
    """Guarda T4: con PADDLE_ENVIRONMENT=production y el centinela, build.py
    debe salir con código distinto de cero ANTES de escribir nada."""
    index = ROOT / "index.html"
    antes = index.stat().st_mtime_ns
    env = dict(
        os.environ,
        PADDLE_ENVIRONMENT="production",
        PADDLE_CLIENT_TOKEN=build.PADDLE_DISABLED_VALUE,
        PADDLE_PRICE_ID="pri_01abc",
    )
    r = subprocess.run([sys.executable, "build.py"], cwd=ROOT, env=env, capture_output=True, text=True)
    assert r.returncode == 1, r.stdout + r.stderr
    assert build.PADDLE_DISABLED_VALUE in r.stderr
    assert "production" in r.stderr
    assert index.stat().st_mtime_ns == antes, "el build escribió artefactos antes de fallar"


# ── T7: conversión ───────────────────────────────────────────────────────

def test_ctas_to_corporate_site_carry_utm_product():
    for name in ("index.html", "precios.html"):
        html = _read(name)
        hrefs = re.findall(r'<a [^>]*href="([^"]*lionsystems\.com\.mx[^"]*)"', html)
        hrefs = [h for h in hrefs if "prompts.lionsystems.com.mx" not in h and not h.startswith("mailto:")]
        assert hrefs, f"{name}: no se encontraron CTAs al sitio corporativo"
        for href in hrefs:
            assert "utm_product=ai-sdlc-pro" in href, f"{name}: {href}"
    assert "ai-sdlc-pro-product-auditoria" in build.LIONSYSTEMS_AUDIT_CTA_URL
    assert "utm_product=ai-sdlc-pro" in build.LIONSYSTEMS_HOME_CTA_URL


def test_pricing_page_reports_purchase_only_after_the_webhook_confirms():
    precios = build.build_precios_page()
    script = re.search(r"function pxTrackPurchase\(\)\{.*?\n\}\n", precios, re.S)
    assert script, "falta pxTrackPurchase en precios.html"
    cuerpo = script.group(0)
    assert 'pxTrack("purchase"' in cuerpo
    assert 'currency:"USD"' in cuerpo
    assert "PADDLE_PRICE_AMOUNT_USD" in cuerpo
    # Se dispara en la rama de éxito del sondeo del webhook...
    assert "subscribed){pxTrackPurchase();pxShowPro();" in precios
    # ...y nunca al abrir el checkout: abrir no es vender.
    inicio = re.search(r"function pxStartCheckout\(anual\)\{.*?\n\}\n", precios, re.S).group(0)
    assert "purchase" not in inicio
    assert 'var PADDLE_PRICE_AMOUNT_USD="' + build.precio_mensual_usd() + '"' in precios


# ── T3 / T5: Edge Function ───────────────────────────────────────────────

def test_edge_function_records_adjustment_created_without_touching_access():
    assert 'eventType === "adjustment.created"' in EDGE_SRC
    assert 'clave: "reembolso"' in EDGE_SRC
    # La rama que registra eventos no-suscripción manda null en los campos
    # que la función SQL usaría para escribir subscriptions.
    rama = EDGE_SRC[EDGE_SRC.index("} else {"):EDGE_SRC.index('if (eventType === "adjustment.created")')]
    assert "p_subscription_id: null" in rama
    assert "p_user_id: null" in rama
    # Y la función SQL solo cambia estado para subscription.%
    sql = (ROOT / "supabase" / "migrations" / "20260731_paddle_webhook_fail_loud_on_unlinked_event.sql").read_text(encoding="utf-8")
    assert "if p_event_type like 'subscription.%' then" in sql


def test_edge_function_alerts_before_every_500_and_on_throw():
    assert 'from "./alertas.ts"' in EDGE_SRC
    assert "ALERTAS_WEBHOOK_URL" in EDGE_SRC
    respuestas_500 = EDGE_SRC.count('new Response("DB error", { status: 500 })')
    assert respuestas_500 == 2, "hay más 500 que alertas"
    assert EDGE_SRC.count('clave: "webhook_error"') == 2
    assert "} catch (error) {" in EDGE_SRC and "transaction threw" in EDGE_SRC
    assert ": any" not in EDGE_SRC


def test_edge_function_never_leaks_secrets_into_logs_or_alerts():
    for linea in EDGE_SRC.splitlines():
        if "alertar(" in linea or "console." in linea:
            assert "PADDLE_WEBHOOK_SECRET" not in linea
            assert "SERVICE_ROLE" not in linea
            assert "rawBody" not in linea
            assert "signatureHeader" not in linea
    assert "CLAVES_PROHIBIDAS" in ALERTAS_SRC
    assert "secret|token|password|authorization|signature" in ALERTAS_SRC
    assert "VENTANA_DEDUP_MS = 60 * 60 * 1000" in ALERTAS_SRC
    # Portabilidad: alertas.ts se ejecuta en Node para probarse, así que
    # ningún código (los comentarios no cuentan) puede tocar Deno.*
    codigo = [l for l in ALERTAS_SRC.splitlines() if not l.lstrip().startswith("//")]
    assert not any("Deno." in l for l in codigo)


def test_new_secret_is_documented():
    assert "ALERTAS_WEBHOOK_URL" in DOCS_PADDLE
    assert "adjustment.created" in DOCS_PADDLE
    env_example = (ROOT / "supabase" / "functions" / ".env.example").read_text(encoding="utf-8")
    assert "ALERTAS_WEBHOOK_URL=" in env_example
    assert "PADDLE_WEBHOOK_SECRET=" in env_example
    assert re.search(r"^ALERTAS_WEBHOOK_URL=\s*$", env_example, re.M), ".env.example lleva un valor real"
    assert "supabase/functions/.env" in _read(".gitignore")
