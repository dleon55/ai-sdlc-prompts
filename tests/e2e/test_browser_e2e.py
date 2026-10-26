#!/usr/bin/env python3
"""
tests/e2e/test_browser_e2e.py — E2E en navegador real (Chromium/Playwright)

Cubre comportamiento de usuario real que el DOM simulado (tests/js/*.js,
tests/test_variables*.py) no garantiza: portapapeles real, foco de teclado,
enrutamiento por idioma/proyecto y reflow — issue #50.

Requiere el paquete Python `playwright` (pip install playwright) y un
binario de Chromium accesible. No se ejecuta como parte de `pytest -q`
por defecto (requiere navegador); ejecutar explícitamente:

    python -m pytest tests/e2e/test_browser_e2e.py -v

Variable de entorno opcional CHROMIUM_PATH para apuntar a un binario
distinto del detectado automáticamente por Playwright.
"""
import json
import os
import pathlib
from urllib.parse import urlparse

import pytest

playwright_sync_api = pytest.importorskip(
    "playwright.sync_api", reason="playwright no instalado (pip install playwright)"
)
sync_playwright = playwright_sync_api.sync_playwright

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent
INDEX_HTML = PROJECT_ROOT / "index.html"
CHROMIUM_PATH = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")


# La app se sirve por HTTP, no por file://.
#
# El texto de los prompts dejó de viajar dentro de index.html y se pide con
# fetch a prompts-text.<lang>.json (issue #202). En file:// el navegador
# bloquea ese fetch por CORS, así que las cards quedarían sin prompt y estas
# pruebas fallarían por el esquema de URL, no por el producto.
#
# Servirlo por HTTP además acerca el e2e a producción: es como lo recibe un
# visitante real.
@pytest.fixture(scope="session")
def app_url():
    import functools
    import http.server
    import threading

    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory=str(PROJECT_ROOT))
    # Puerto 0: el sistema asigna uno libre, para no chocar con otra corrida.
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
    hilo.start()
    try:
        yield f"http://127.0.0.1:{servidor.server_port}/index.html#app"
    finally:
        servidor.shutdown()
        servidor.server_close()


def _launch_browser(playwright):
    kwargs = {"headless": True}
    if pathlib.Path(CHROMIUM_PATH).exists():
        kwargs["executable_path"] = CHROMIUM_PATH
    return playwright.chromium.launch(**kwargs)


def _instalar_backend_simulado(page):
    """Hace de backend propio (/api/*) dentro del navegador: ninguna prueba
    llega a red real ni a producción. El estado es un dict de Python que cada
    prueba puede cambiar (page.api): la prueba de la sesión, el estado de la
    prueba gratuita y las llamadas de feedback recibidas."""
    estado = {"usuario": None, "prueba": {"active": True, "subscribed": False}, "feedback": [], "logins": []}

    def responder(route):
        ruta = urlparse(route.request.url).path
        if ruta == "/api/auth/session":
            return route.fulfill(status=200, content_type="application/json", body=json.dumps({"user": estado["usuario"]}))
        if ruta == "/api/trial/status":
            return route.fulfill(status=200, content_type="application/json", body=json.dumps(estado["prueba"]))
        if ruta == "/api/trial/feedback":
            estado["feedback"].append(route.request.post_data_json)
            return route.fulfill(status=200, content_type="application/json",
                                 body=json.dumps({"renewed": True, "new_expires_at": "2099-01-01"}))
        if ruta == "/api/auth/login":
            estado["logins"].append(route.request.url)
            return route.fulfill(status=200, content_type="text/html", body="<p>login simulado</p>")
        if ruta in ("/api/prompt-stats/track", "/api/projects", "/api/project-prompt-state"):
            return route.fulfill(status=204, body="")
        return route.fulfill(status=404, content_type="application/json", body="{}")

    page.route("**/api/**", responder)
    page.api = estado
    return estado


@pytest.fixture
def app_page(app_url):
    """Página de la app ya cargada, en español, sin onboarding/banner de
    bienvenida (se seedea localStorage antes del primer render real)."""
    with sync_playwright() as p:
        browser = _launch_browser(p)
        context = browser.new_context(viewport={"width": 1400, "height": 1000})
        context.grant_permissions(["clipboard-read", "clipboard-write"])
        page = context.new_page()
        _instalar_backend_simulado(page)
        page.goto(app_url)
        page.evaluate(
            """
            localStorage.setItem('AI_SDLC_welcome_seen', '1');
            localStorage.setItem('AI_SDLC_onboarding_done', '1');
            localStorage.setItem('AI_SDLC_language', 'es');
            """
        )
        page.reload()
        page.wait_for_load_state("networkidle")
        # El backend es simulado (ver _instalar_backend_simulado): cada copia
        # en la suite no toca ningún contador real. Por defecto todo queda
        # "permitido"; las pruebas del muro cambian page.api explícitamente.
        page.evaluate(
            """
            window._usuario = null;
            // Por defecto, el estado de auth ya está "resuelto" (sin sesión) --
            // checkProFeatureGate() falla abierto mientras _authStateResolved
            // sea false (ver build.py, regresión del race condition post-login),
            // así que sin esto TODOS los tests de este archivo quedarían en
            // modo fail-open permanente y el muro de registro/feedback nunca
            // se mostraría. Los tests que ejercitan esa ventana de carrera lo
            // sobreescriben explícitamente de vuelta a false.
            window._authStateResolved = true;
            """
        )
        yield page
        browser.close()


def _set_variable(page, field_id, value):
    page.click("#var-toggle-btn")
    page.fill(f"#{field_id}", value)
    page.click("#var-apply-btn")
    page.wait_for_timeout(150)


def _copy_and_read_clipboard(page, pid, lang="es"):
    """Copia un prompt y lee el portapapeles resultante. Si el prompt tiene
    placeholders OBLIGATORIOS sin resolver, el copiado ahora queda
    bloqueado por un toast de confirmación ("Copiar de todas formas") en
    vez de copiar directamente (fix: validación bloqueante de placeholders,
    antes el copiado siempre 'tenía éxito' aunque quedaran [CORCHETES] sin
    llenar) -- si aparece, lo confirmamos para completar el copiado real."""
    btn = page.locator(f'.copy-btn[onclick*="{pid}\', \'{lang}\'"]').first
    btn.click()
    page.wait_for_timeout(250)
    action = page.locator(".toast-action").first
    if action.count() and action.is_visible():
        action.click()
        page.wait_for_timeout(250)
    return page.evaluate("navigator.clipboard.readText()")


def _canonical_newlines(text):
    """El portapapeles de Chromium en Windows convierte LF a CRLF.

    La aplicación conserva el contenido; las pruebas comparan el texto con
    saltos de línea canónicos para no confundir una convención de plataforma
    con pérdida de datos durante la sustitución o el copiado.
    """
    return text.replace("\r\n", "\n").replace("\r", "\n")


# ─────────────────────  Copia individual + sustitución  ─────────────────────

def test_single_copy_matches_variable_panel_value_verbatim(app_page):
    """Un valor con HTML, &, comillas, $, / y salto de línea sobrevive
    intacto desde el textarea hasta el portapapeles (criterio: valores con
    HTML, $, barras, saltos de línea y Unicode)."""
    special = "Línea1 <b>&\"'$/tag\nLínea2 ñ 日本語 emoji:🚀"
    _set_variable(app_page, "vf-entrada", special)
    clip = _copy_and_read_clipboard(app_page, "02-05-analisis-integral-requerimientos", "es")
    assert _canonical_newlines(special) in _canonical_newlines(clip), (
        "El valor especial no sobrevivió en el portapapeles"
    )


def test_single_copy_preview_equals_clipboard_content(app_page):
    """El contenido visible en el <code> del card (preview) coincide con lo
    que efectivamente llega al portapapeles al copiar, para el mismo pid."""
    special = "Repo-Test_valor/con-slash"
    _set_variable(app_page, "vf-repositorio", special)
    pid = "00-B-01-scaffolding-repositorio"
    app_page.click(f'.card-expand[onclick*="{pid}-es"]')
    app_page.wait_for_timeout(150)
    preview = app_page.evaluate(f'document.getElementById("code-{pid}-es").textContent')
    clip = _copy_and_read_clipboard(app_page, pid, "es")
    # El portapapeles antepone el framework; el preview no. El cuerpo del
    # prompt (preview) debe estar íntegro dentro del portapapeles.
    assert _canonical_newlines(preview).strip() in _canonical_newlines(clip)
    assert special in preview
    assert special in clip


# ─────────────────────  Copia múltiple  ─────────────────────

def test_multi_select_copy_does_not_duplicate_prompts(app_page):
    """Regresión del fix de multi-select (PR #42): seleccionar una sección
    completa no debe duplicar cada prompt en el portapapeles."""
    app_page.click("#ms-toggle-btn")
    app_page.wait_for_timeout(150)
    sec_check = app_page.locator("#sec-01 .sec-check").first
    sec_check.check(force=True)
    app_page.wait_for_timeout(150)
    app_page.click(".ms-copy-btn")
    app_page.wait_for_timeout(250)
    clip = app_page.evaluate("navigator.clipboard.readText()")
    # Contar separadores '---' era un proxy de "no se duplicó", y dejó de
    # servir cuando el contrato de operación pasó a viajar con el prompt
    # copiado: cada prompt aporta ahora un bloque más, con su propio
    # separador, sin que nada esté duplicado. Se comprueba la duplicación
    # directamente, que era la intención original (PR #42).
    assert clip.count("Prompt para inventario técnico") <= 1, "01-01 aparece duplicado"
    # Y el contrato acompaña a cada prompt, uno por prompt, sin repetirse.
    assert clip.count("## Contrato de operación") == 2, (
        f"se esperaba un contrato por prompt (2), hubo {clip.count('## Contrato de operación')}"
    )


# ─────────────────────  Modal de fórmulas  ─────────────────────

def test_formula_modal_opens_and_shows_usage_formula(app_page):
    pid = "00-B-01-scaffolding-repositorio"
    app_page.click(f'.info-btn[onclick*="{pid}\', \'es\'"]')
    app_page.wait_for_timeout(200)
    modal_open = app_page.evaluate("document.getElementById('info-modal').classList.contains('open')")
    assert modal_open
    formula_text = app_page.evaluate(
        "document.getElementById('modal-formulas').textContent"
    )
    assert "repository scaffolding" in formula_text.lower() or "scaffolding" in formula_text.lower()
    app_page.click(".modal-close-btn")
    app_page.wait_for_timeout(150)
    modal_open_after = app_page.evaluate("document.getElementById('info-modal').classList.contains('open')")
    assert not modal_open_after


# ─────────────────────  Idioma  ─────────────────────

def test_language_switch_updates_visible_cards_and_copy_content(app_page):
    assert app_page.evaluate("document.documentElement.getAttribute('lang')") == "es"
    assert app_page.locator('.card[data-lang="es"]').first.is_visible()

    app_page.click("#lang-btn")
    app_page.click('.lang-option[data-lang="en"]')
    app_page.wait_for_timeout(200)

    assert app_page.evaluate("document.documentElement.getAttribute('lang')") == "en"
    assert app_page.locator('.card[data-lang="en"]').first.is_visible()
    assert not app_page.locator('.card[data-lang="es"]').first.is_visible()

    clip = _copy_and_read_clipboard(app_page, "00-B-01-scaffolding-repositorio", "en")
    assert "Act as a Principal Software Engineer" in clip
    assert "Actúa como un Principal Software Engineer" not in clip


def test_copy_confirmation_toast_matches_active_language(app_page):
    """El toast de confirmación de copiado respeta el idioma activo (antes
    quedaba fijo en español -'Prompt copiado con éxito'- incluso en modo EN,
    la acción más usada de la app)."""
    app_page.click("#lang-btn")
    app_page.click('.lang-option[data-lang="en"]')
    app_page.wait_for_timeout(200)

    # Este prompt tiene placeholders obligatorios sin resolver -> el copiado
    # queda bloqueado por un toast .warn con acción "Copy anyway" en vez de
    # copiar directamente (validación bloqueante de placeholders, FR-VAR-04).
    # Confirmar esa acción dispara el copiado real y su propio toast .success,
    # que es el que nos interesa verificar aquí.
    btn = app_page.locator('.copy-btn[onclick*="00-B-01-scaffolding-repositorio\', \'en\'"]').first
    btn.click()
    app_page.wait_for_timeout(250)
    action = app_page.locator(".toast-action").first
    assert action.count() > 0, "se esperaba el toast bloqueante de confirmación de placeholders"
    action.click()

    toast_text = app_page.locator("#toast-container .toast.success").first.inner_text()
    assert "copied" in toast_text.lower()
    assert "copiado" not in toast_text.lower()


def test_toast_container_has_accessible_live_region(app_page):
    """Los toasts deben anunciarse a lectores de pantalla: antes el
    contenedor no tenía aria-live/role, así que un usuario de lector de
    pantalla no se enteraba si copiar funcionó, falló, o si quedaron
    placeholders sin resolver."""
    role = app_page.evaluate("document.getElementById('toast-container').getAttribute('role')")
    live = app_page.evaluate("document.getElementById('toast-container').getAttribute('aria-live')")
    assert role == "status"
    assert live == "polite"


# ─────────────────────  Búsqueda  ─────────────────────

def test_search_filters_cards_after_debounce(app_page):
    """La búsqueda por texto filtra las tarjetas visibles. El input tiene
    debounce de 150ms (auditoría de performance: antes cada tecla re-escaneaba
    el texto de las 184 tarjetas -92 prompts x ES/EN- sin ninguna espera);
    se aguarda más que ese debounce antes de leer el resultado."""
    total_before = app_page.locator("#vis-count").inner_text()
    assert "en total" in total_before

    app_page.fill(".search-bar input", "scaffolding")
    app_page.wait_for_timeout(300)

    assert app_page.locator(
        '.card-expand[onclick*="scaffolding-repositorio-es"]'
    ).first.is_visible()
    assert not app_page.locator(
        '.card-expand[onclick*="00-C-01-issue-para-agente-ia-es"]'
    ).first.is_visible()
    count_text = app_page.locator("#vis-count").inner_text()
    assert "coincidencia" in count_text


# ─────────────────────  Proyectos  ─────────────────────

def test_project_switch_isolates_variables(app_page):
    _set_variable(app_page, "vf-repositorio", "proyecto-A-valor")

    app_page.evaluate("createProject(); renderProjectSelector(); syncPanelToProject();")
    app_page.wait_for_timeout(150)
    _set_variable(app_page, "vf-repositorio", "proyecto-B-valor")

    clip_b = _copy_and_read_clipboard(app_page, "00-B-01-scaffolding-repositorio", "es")
    assert "proyecto-B-valor" in clip_b
    assert "proyecto-A-valor" not in clip_b

    projects = app_page.evaluate("loadProjects().length")
    assert projects >= 2


# ─────────────────────  Panel contextual de variables  ─────────────────────

def test_contextual_variable_panel_reflects_active_prompt_fields(app_page):
    pid = "13-05-dast-analisis-dinamico-seguridad"
    app_page.click(f'.card-expand[onclick*="{pid}-es"]')
    app_page.wait_for_timeout(150)
    app_page.evaluate(f"updateContextualVariablePanel('{pid}')")
    app_page.wait_for_timeout(150)
    status_text = app_page.evaluate(
        "(document.getElementById('var-context-status') || {}).textContent || ''"
    )
    assert isinstance(status_text, str)  # el panel contextual no debe lanzar error


# ─────────────────────  Teclado / foco / accesibilidad básica  ─────────────────────

def test_all_interactive_elements_have_accessible_name(app_page):
    result = app_page.evaluate(
        """
        () => {
          const els = Array.from(document.querySelectorAll('button, input, select, textarea, a[href]'));
          const bad = [];
          for (const el of els) {
            const text = (el.textContent || '').trim();
            const aria = el.getAttribute('aria-label');
            const title = el.getAttribute('title');
            const alt = el.getAttribute('alt');
            const labelFor = el.id ? document.querySelector('label[for="' + el.id + '"]') : null;
            const hasName = !!(text || aria || title || alt || labelFor);
            if (!hasName && el.offsetParent !== null) bad.push(el.outerHTML.slice(0, 150));
          }
          return bad;
        }
        """
    )
    assert result == [], f"Elementos sin nombre accesible: {result}"


def test_keyboard_tab_reaches_a_copy_button(app_page):
    app_page.click("body")
    reached = False
    for _ in range(40):
        app_page.keyboard.press("Tab")
        cls = app_page.evaluate("document.activeElement.className || ''")
        if "copy-btn" in cls:
            reached = True
            break
    assert reached, "El foco por teclado no alcanzó ningún botón de copia en 40 Tabs"


def test_buttons_do_not_suppress_focus_outline_in_css():
    """Chequeo estructural: ningún selector de botón interactivo fija
    outline:none/0 sin una alternativa de foco visible (border/box-shadow)
    -- ver riesgos residuales para la limitación de verificación en
    navegador headless."""
    source = (PROJECT_ROOT / "build.py").read_text(encoding="utf-8")
    assert ".copy-btn { outline: none" not in source.replace("\n", " ")
    assert "button, .info-btn { outline: none" not in source.replace("\n", " ")


def test_no_horizontal_overflow_at_320px_viewport(app_url):
    with sync_playwright() as p:
        browser = _launch_browser(p)
        context = browser.new_context(viewport={"width": 320, "height": 800})
        page = context.new_page()
        page.goto(app_url)
        page.evaluate(
            """
            localStorage.setItem('AI_SDLC_welcome_seen', '1');
            localStorage.setItem('AI_SDLC_onboarding_done', '1');
            localStorage.setItem('AI_SDLC_language', 'es');
            """
        )
        page.reload()
        page.wait_for_load_state("networkidle")
        metrics = page.evaluate(
            "() => ({scrollWidth: document.documentElement.scrollWidth, "
            "clientWidth: document.documentElement.clientWidth})"
        )
        browser.close()
    assert metrics["scrollWidth"] <= metrics["clientWidth"], (
        f"Overflow horizontal a 320px: scrollWidth={metrics['scrollWidth']} "
        f"> clientWidth={metrics['clientWidth']}"
    )


def test_dismissing_onboarding_with_close_button_persists_across_reload(app_url):
    """Cerrar el onboarding con el botón 'X' debe descartarlo permanentemente,
    igual que 'No volver a mostrar' (antes solo ese enlace persistía el
    descarte; la 'X' -el patrón universal de cierre de modal- lo mostraba
    de nuevo en cada recarga)."""
    with sync_playwright() as p:
        browser = _launch_browser(p)
        context = browser.new_context(viewport={"width": 1400, "height": 1000})
        page = context.new_page()
        page.goto(app_url)
        page.evaluate(
            """
            localStorage.setItem('AI_SDLC_welcome_seen', '1');
            localStorage.setItem('AI_SDLC_language', 'es');
            localStorage.removeItem('AI_SDLC_onboarding_done');
            """
        )
        page.reload()
        page.wait_for_load_state("networkidle")

        assert page.evaluate(
            "!document.getElementById('ob-overlay').classList.contains('hidden')"
        ), "El onboarding no se mostró en la primera visita (precondición del test)"

        page.click(".ob-close")
        page.wait_for_timeout(100)

        page.reload()
        page.wait_for_load_state("networkidle")
        assert page.evaluate(
            "document.getElementById('ob-overlay').classList.contains('hidden')"
        ), "El onboarding reapareció tras recargar pese a haberse cerrado con la 'X'"
        browser.close()


# ─────────────────────  Registro de usuarios (backend propio)  ─────────────────────

def test_auth_button_starts_github_login_through_the_backend(app_page):
    """Sin sesión, el botón de cuenta tiene nombre accesible y lleva a
    /api/auth/login con ?volver= la página actual, para regresar aquí tras
    autenticarse con GitHub. No hay SDK externo ni aviso de 'no configurado'."""
    label = app_page.evaluate(
        "(document.getElementById('auth-btn') || {}).textContent || ''"
    ).strip()
    assert label, "El botón de autenticación no tiene nombre accesible"

    app_page.click("#auth-btn")
    app_page.wait_for_timeout(500)

    logins = app_page.api["logins"]
    assert logins, "El botón no navegó a /api/auth/login"
    assert "volver=%2F" in logins[0], f"El login no indica a dónde volver: {logins[0]!r}"
    assert app_page.evaluate("typeof window.supabase") == "undefined", "No debe cargarse ningún SDK de Supabase"


def test_landing_shows_sign_in_button_that_goes_to_app(app_url):
    """La portada (sin #app) muestra su propio botón de inicio de sesión: al
    pulsarlo va a /api/auth/login con volver=/app. Con sesión, el mismo botón
    muestra el usuario de GitHub en vez de "Iniciar sesión"."""
    portada = app_url.split("#")[0]
    with sync_playwright() as p:
        browser = _launch_browser(p)
        page = browser.new_context(viewport={"width": 1400, "height": 900}).new_page()
        api = _instalar_backend_simulado(page)
        page.goto(portada)
        page.wait_for_load_state("networkidle")

        boton = page.locator("#landing-auth-btn")
        assert boton.is_visible(), "El botón de inicio de sesión no se ve en la portada"
        assert "Iniciar sesión" in boton.inner_text()

        boton.click()
        page.wait_for_timeout(500)
        assert api["logins"], "El botón de la portada no navegó a /api/auth/login"
        assert "volver=%2Fapp" in api["logins"][0], f"Debe volver a la app: {api['logins'][0]!r}"

        # Con sesión: el botón muestra el usuario.
        api["usuario"] = {"id": "u-portada", "githubLogin": "usuario-portada"}
        page.goto(portada)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(300)
        assert page.locator("#landing-auth-btn").inner_text().strip() == "usuario-portada"
        browser.close()


def test_new_project_id_is_a_valid_uuid_for_cloud_sync(app_page):
    """genId() debe producir un UUID real (no el prefijo 'proj_' anterior):
    la tabla `projects` del backend usa una columna `uuid`, y un id local
    inválido para ese tipo rompería la sincronización en cuanto el usuario
    inicia sesión (ver docs/auth-setup.md)."""
    app_page.evaluate("createProject('Proyecto UUID')")
    app_page.wait_for_timeout(100)
    new_id = app_page.evaluate("(loadProjects() || []).slice(-1)[0].id")
    uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    import re
    assert re.match(uuid_pattern, new_id, re.IGNORECASE), (
        f"id de proyecto no es un UUID v4 válido: {new_id!r}"
    )


# ─────────────────────  Muro de registro / prueba / feedback  ─────────────────────
# Ver diseño 04-01, plan 05-01 y docs/trial-gate-setup.md.
#
# Rediseño (issue #7, Opción B): el repositorio es público, así que copiar
# prompts ya NO pasa por ningún gate (protegerlo no tendría efecto real).
# El muro ahora protege la PLATAFORMA: crear un 2do proyecto o más, y
# guardar personalización/resultados de IA -- ver checkProFeatureGate() y
# docs/trial-gate-setup.md.

def test_copying_prompts_is_never_gated_regardless_of_trial_state(app_page):
    """Copiar cualquier prompt debe funcionar siempre, incluso simulando el
    estado más restrictivo posible (anónimo y con la prueba vencida en el
    backend). Confirma que copyResolvedText() ya no llama a ningún gate."""
    app_page.api["prueba"] = {"active": False, "subscribed": False}
    app_page.evaluate(
        """
        window._usuario = null;
        """
    )
    pid = "00-B-01-scaffolding-repositorio"
    clip = _copy_and_read_clipboard(app_page, pid, "es")

    is_open = app_page.evaluate(
        "(document.getElementById('register-wall-modal') || {}).classList"
        ".contains('open')"
    )
    assert not is_open, "Copiar un prompt no debe abrir ningún muro -- ya no hay gate de copia"
    assert len(clip) > 200, f"La copia debería completarse siempre, portapapeles: {clip!r}"


def test_pro_feature_gate_fails_open_while_auth_state_is_still_resolving(app_page):
    """Regresión de un bug real reportado en producción: justo tras volver
    del redirect de GitHub, /api/auth/session todavía está en viaje (red
    real) -- _usuario sigue en null
    durante esa ventana. Antes de este fix, el gate trataba eso como
    "anónimo" y volvía a mostrar el muro de registro aunque el login ya
    hubiera funcionado. Con _authStateResolved en false (simulando esa
    ventana exacta), crear un 2do proyecto debe permitirse (fail-open)."""
    app_page.evaluate(
        """
        window._authStateResolved = false;
        window._usuario = null;
        """
    )
    before = app_page.evaluate("(loadProjects() || []).length")
    app_page.evaluate("requestNewProjectFromModal()")
    app_page.wait_for_timeout(300)

    is_open = app_page.evaluate(
        "(document.getElementById('register-wall-modal') || {}).classList"
        ".contains('open')"
    )
    assert not is_open, (
        "El muro de registro no debería aparecer mientras el estado de "
        "auth sigue resolviéndose (fail-open) -- ver checkProFeatureGate()"
    )
    after = app_page.evaluate("(loadProjects() || []).length")
    assert after == before + 1, "El 2do proyecto debería haberse creado (fail-open)"


def test_register_wall_appears_when_creating_second_project_anonymously(app_page):
    """Sin sesión, intentar crear un 2do proyecto (el 1ro ya existe por
    defecto) debe abrir el muro de registro en vez de crearlo -- el límite
    de "1 proyecto gratis" se decide del lado del cliente
    (loadProjects().length), sin necesitar ningún RPC."""
    app_page.evaluate(
        """
        window._usuario = null;
        """
    )
    before = app_page.evaluate("(loadProjects() || []).length")
    assert before == 1, f"El fixture debería arrancar con exactamente 1 proyecto, tiene {before}"

    app_page.evaluate("requestNewProjectFromModal()")
    app_page.wait_for_timeout(300)

    is_open = app_page.evaluate(
        "(document.getElementById('register-wall-modal') || {}).classList"
        ".contains('open')"
    )
    assert is_open, "El muro de registro no apareció al intentar crear un 2do proyecto anónimo"

    after = app_page.evaluate("(loadProjects() || []).length")
    assert after == before, "No debería haberse creado un 2do proyecto con el muro de registro abierto"


def test_feedback_wall_blocks_second_project_until_submitted_then_renews(app_page):
    """Con sesión simulada y /api/trial/status devolviendo 'active: false'
    (prueba vencida), el intento de crear un 2do proyecto debe abrir el
    muro de feedback en vez de crearlo. Al enviarlo (/api/trial/feedback
    simulado con éxito), el modal se cierra y el usuario puede reintentar."""
    app_page.api["prueba"] = {"active": False, "subscribed": False}
    app_page.evaluate(
        """
        window._usuario = { id: 'fake-user-id', githubLogin: 'usuario-prueba' };
        """
    )
    before = app_page.evaluate("(loadProjects() || []).length")
    app_page.evaluate("requestNewProjectFromModal()")
    app_page.wait_for_timeout(300)

    is_open = app_page.evaluate(
        "(document.getElementById('feedback-wall-modal') || {}).classList"
        ".contains('open')"
    )
    assert is_open, "El muro de feedback no apareció con la prueba vencida"
    mid = app_page.evaluate("(loadProjects() || []).length")
    assert mid == before, "No debería haberse creado el 2do proyecto antes de enviar el feedback"

    app_page.click('#fb-stars .fb-star[data-value="4"]')
    app_page.fill("#fb-comments", "Muy útil, gracias.")
    app_page.click(".fb-submit-btn")
    app_page.wait_for_timeout(300)

    llamadas = app_page.api["feedback"]
    assert llamadas and llamadas[0]["rating"] == 4, f"/api/trial/feedback no recibió la calificación: {llamadas!r}"
    assert llamadas[0]["comments"] == "Muy útil, gracias."

    still_open = app_page.evaluate(
        "(document.getElementById('feedback-wall-modal') || {}).classList"
        ".contains('open')"
    )
    assert not still_open, "El muro de feedback debería cerrarse tras enviar exitosamente"

    # El backend simulado sigue respondiendo active:false -- lo relevante es
    # que el modal se cerró y el usuario puede reintentar sin quedar atascado.


def test_saving_custom_additions_is_gated_for_anonymous_users(app_page):
    """Escribir el primer carácter en 'Adiciones personalizadas' (modal ⓘ)
    sin sesión debe abrir el muro de registro y vaciar el campo -- guardar
    personalización es una función Pro, no cubierta por el proyecto #1
    gratis. Ver saveGatedPromptField()."""
    app_page.evaluate(
        """
        window._usuario = null;
        """
    )
    pid = "00-B-01-scaffolding-repositorio"
    app_page.click(f'.info-btn[onclick*="{pid}\', \'es\'"]')
    app_page.wait_for_timeout(150)
    custom_field = app_page.locator("#modal-custom-section textarea")
    custom_field.fill("Nuestro equipo siempre usa TypeScript strict mode")
    app_page.wait_for_timeout(300)

    is_open = app_page.evaluate(
        "(document.getElementById('register-wall-modal') || {}).classList"
        ".contains('open')"
    )
    assert is_open, "El muro de registro no apareció al escribir personalización sin sesión"
    assert custom_field.input_value() == "", "El campo debería vaciarse al bloquear el guardado"
