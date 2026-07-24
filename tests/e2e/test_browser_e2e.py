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
import os
import pathlib

import pytest

playwright_sync_api = pytest.importorskip(
    "playwright.sync_api", reason="playwright no instalado (pip install playwright)"
)
sync_playwright = playwright_sync_api.sync_playwright

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent
INDEX_HTML = PROJECT_ROOT / "index.html"
APP_URL = INDEX_HTML.resolve().as_uri() + "#app"
CHROMIUM_PATH = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")


def _launch_browser(playwright):
    kwargs = {"headless": True}
    if pathlib.Path(CHROMIUM_PATH).exists():
        kwargs["executable_path"] = CHROMIUM_PATH
    return playwright.chromium.launch(**kwargs)


@pytest.fixture
def app_page():
    """Página de la app ya cargada, en español, sin onboarding/banner de
    bienvenida (se seedea localStorage antes del primer render real)."""
    with sync_playwright() as p:
        browser = _launch_browser(p)
        context = browser.new_context(viewport={"width": 1400, "height": 1000})
        context.grant_permissions(["clipboard-read", "clipboard-write"])
        page = context.new_page()
        page.goto(APP_URL)
        page.evaluate(
            """
            localStorage.setItem('AI_SDLC_welcome_seen', '1');
            localStorage.setItem('AI_SDLC_onboarding_done', '1');
            localStorage.setItem('AI_SDLC_language', 'es');
            """
        )
        page.reload()
        page.wait_for_load_state("networkidle")
        # Reemplaza el SDK real de Supabase (ya cargado desde el CDN real en
        # este punto -- ver docs/trial-gate-setup.md) por un stub que jamás
        # llega a red: sin esto, cada copia en la suite incrementaría el
        # contador real de anon_usage en producción y eventualmente el
        # runner de CI quedaría "gateado", rompiendo todos los tests de
        # copiado (riesgo #2 del diseño 04-01, ver también supabase/trial_gate.sql).
        # Por defecto todo queda "permitido"; los tests que ejercitan el
        # muro de registro/feedback sobreescriben este stub explícitamente.
        page.evaluate(
            """
            window.supabase = {
                createClient: function() {
                    return {
                        auth: {
                            getSession: function() { return Promise.resolve({ data: { session: null } }); },
                            onAuthStateChange: function() {},
                            signInWithOAuth: function() {},
                            signOut: function() {}
                        },
                        rpc: function(name) {
                            if (name === 'check_anon_usage') {
                                return Promise.resolve({ data: { allowed: true, remaining: 99 }, error: null });
                            }
                            if (name === 'check_trial_status') {
                                return Promise.resolve({ data: { active: true, expires_at: null }, error: null });
                            }
                            return Promise.resolve({ data: null, error: null });
                        }
                    };
                }
            };
            window._sb = null;
            // Por defecto, el estado de auth ya está "resuelto" (sin sesión) --
            // checkCopyGate() falla abierto mientras _authStateResolved sea
            // false (ver build.py, regresión del race condition post-login),
            // así que sin esto TODOS los tests de este archivo quedarían en
            // modo fail-open permanente y el muro de registro/feedback nunca
            // se mostraría en ningún test, aunque el stub de arriba sí
            // bloqueara. Los tests que ejercitan esa ventana de carrera lo
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


# ─────────────────────  Copia individual + sustitución  ─────────────────────

def test_single_copy_matches_variable_panel_value_verbatim(app_page):
    """Un valor con HTML, &, comillas, $, / y salto de línea sobrevive
    intacto desde el textarea hasta el portapapeles (criterio: valores con
    HTML, $, barras, saltos de línea y Unicode)."""
    special = "Línea1 <b>&\"'$/tag\nLínea2 ñ 日本語 emoji:🚀"
    _set_variable(app_page, "vf-entrada", special)
    clip = _copy_and_read_clipboard(app_page, "02-05-analisis-integral-requerimientos", "es")
    assert special in clip, "El valor especial no sobrevivió verbatim en el portapapeles"


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
    assert preview.strip() in clip
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
    # sección 01 tiene 2 prompts (01-01, 01-02); separador '---' entre
    # bloques + el framework antepuesto = a lo sumo 3 separadores '---'.
    separators = clip.count("\n\n---\n\n")
    assert separators <= 3, f"Posible duplicación: {separators} separadores en {clip[:200]!r}"
    assert clip.count("Prompt para inventario técnico") <= 1, "01-01 aparece duplicado"


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

    app_page.evaluate("createProject(); renderProjFloat(); renderProjectSelector(); syncPanelToProject();")
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


def test_no_horizontal_overflow_at_320px_viewport():
    with sync_playwright() as p:
        browser = _launch_browser(p)
        context = browser.new_context(viewport={"width": 320, "height": 800})
        page = context.new_page()
        page.goto(APP_URL)
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


def test_dismissing_onboarding_with_close_button_persists_across_reload():
    """Cerrar el onboarding con el botón 'X' debe descartarlo permanentemente,
    igual que 'No volver a mostrar' (antes solo ese enlace persistía el
    descarte; la 'X' -el patrón universal de cierre de modal- lo mostraba
    de nuevo en cada recarga)."""
    with sync_playwright() as p:
        browser = _launch_browser(p)
        context = browser.new_context(viewport={"width": 1400, "height": 1000})
        page = context.new_page()
        page.goto(APP_URL)
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


# ─────────────────────  Registro de usuarios (Supabase, sin configurar)  ─────────────────────

def test_auth_button_is_inert_and_safe_when_supabase_not_configured(app_page):
    """Guarda la rama defensiva de isSupabaseConfigured() == false, sin
    depender de si build.py ya tiene credenciales reales (desde que se
    completó docs/auth-setup.md, SUPABASE_URL/SUPABASE_ANON_KEY dejaron de
    ser el centinela en el sitio publicado). Se fuerza el centinela en la
    página ya cargada para seguir cubriendo el caso "aún sin configurar":
    el botón debe seguir siendo visible y con nombre accesible, pero al
    hacer clic debe avisar que falta configuración en vez de intentar
    llamar a un backend inexistente (o lanzar un error de JS)."""
    app_page.evaluate(
        "window.SUPABASE_URL = 'PENDIENTE_CONFIGURAR'; "
        "window.SUPABASE_ANON_KEY = 'PENDIENTE_CONFIGURAR'; "
        "window._sb = null;"
    )

    label = app_page.evaluate(
        "(document.getElementById('auth-btn') || {}).textContent || ''"
    ).strip()
    assert label, "El botón de autenticación no tiene nombre accesible"

    app_page.click("#auth-btn")
    app_page.wait_for_timeout(250)
    toast_text = app_page.evaluate(
        "(document.querySelector('.toast') || {}).textContent || ''"
    )
    assert "configurad" in toast_text.lower(), (
        f"Se esperaba un aviso de 'no configurado', se obtuvo: {toast_text!r}"
    )
    # La carga (o no) del <script> del SDK de Supabase se decide una sola vez,
    # en window.load, antes de que este test pueda forzar el centinela --
    # por eso no se verifica aquí; ver test_supabase_sdk_script_is_gated_by_isSupabaseConfigured
    # en tests/test_build.py para la cobertura estática de esa condición.


def test_auth_button_attempts_github_oauth_when_supabase_is_configured(app_page):
    """Complemento del test anterior: confirma que build.py ya tiene
    credenciales reales (no el centinela) tras completar docs/auth-setup.md,
    y que en ese caso el botón intenta el flujo real de GitHub OAuth
    (signInWithOAuth) en vez de mostrar el aviso de 'no configurado'. Se
    reemplaza el SDK real por un stub para no depender de red externa ni
    de una redirección real a GitHub dentro del test."""
    assert app_page.evaluate("isSupabaseConfigured()"), (
        "SUPABASE_URL/SUPABASE_ANON_KEY siguen siendo el centinela en build.py"
    )

    app_page.evaluate(
        """
        window.__oauthCalls = [];
        window.supabase = {
            createClient: function() {
                return { auth: {
                    getSession: function() { return Promise.resolve({ data: { session: null } }); },
                    onAuthStateChange: function() {},
                    signInWithOAuth: function(opts) { window.__oauthCalls.push(opts); },
                    signOut: function() {}
                }};
            }
        };
        window._sb = null;
        """
    )

    app_page.click("#auth-btn")
    app_page.wait_for_timeout(250)

    calls = app_page.evaluate("window.__oauthCalls")
    assert calls and calls[0]["provider"] == "github", (
        f"signInWithOAuth no fue invocado con GitHub: {calls!r}"
    )

    toast_text = app_page.evaluate(
        "(document.querySelector('.toast') || {}).textContent || ''"
    )
    assert "configurad" not in toast_text.lower(), (
        f"No debería mostrarse el aviso de 'no configurado': {toast_text!r}"
    )


def test_new_project_id_is_a_valid_uuid_for_cloud_sync(app_page):
    """genId() debe producir un UUID real (no el prefijo 'proj_' anterior):
    la tabla `projects` de Supabase usa una columna `uuid`, y un id local
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

def test_copy_gate_fails_open_while_auth_state_is_still_resolving(app_page):
    """Regresión de un bug real reportado en producción: justo tras volver
    del redirect de GitHub, getSession() todavía está intercambiando el
    código por una sesión (viaje de red real) -- _sbUser sigue en null
    durante esa ventana. Antes de este fix, checkCopyGate() trataba eso
    como "anónimo" y volvía a mostrar el muro de registro aunque el login
    ya hubiera funcionado. Con _authStateResolved en false (simulando esa
    ventana exacta), la copia debe permitirse (fail-open), no bloquearse."""
    app_page.evaluate(
        """
        window._authStateResolved = false;
        window._sbUser = null;
        window.supabase.createClient = function() {
            return {
                auth: {
                    getSession: function() { return new Promise(function() {}); },
                    onAuthStateChange: function() {},
                    signInWithOAuth: function() {},
                    signOut: function() {}
                },
                rpc: function(name) {
                    if (name === 'check_anon_usage') {
                        return Promise.resolve({ data: { allowed: false, remaining: 0 }, error: null });
                    }
                    return Promise.resolve({ data: null, error: null });
                }
            };
        };
        window._sb = null;
        """
    )
    pid = "00-B-01-scaffolding-repositorio"
    clip = _copy_and_read_clipboard(app_page, pid, "es")

    is_open = app_page.evaluate(
        "(document.getElementById('register-wall-modal') || {}).classList"
        ".contains('open')"
    )
    assert not is_open, (
        "El muro de registro no debería aparecer mientras el estado de "
        "auth sigue resolviéndose (fail-open) -- ver checkCopyGate()"
    )
    # No se compara contra el pid literal -- el slug del prompt no
    # necesariamente aparece tal cual en su propio texto copiado. Un
    # portapapeles no vacío y razonablemente largo (framework + cuerpo del
    # prompt) confirma que la copia sí se completó en vez de quedar bloqueada.
    assert len(clip) > 200, f"La copia debería haberse completado (fail-open), portapapeles: {clip!r}"


def test_register_wall_appears_when_anon_copy_limit_is_reached(app_page):
    """Con check_anon_usage() stubeado devolviendo 'allowed: false' (simula
    que ya se agotaron las 2 copias gratis por IP), el siguiente intento de
    copia debe abrir el muro de registro en vez de copiar al portapapeles."""
    app_page.evaluate(
        """
        window.supabase.createClient = function() {
            return {
                auth: {
                    getSession: function() { return Promise.resolve({ data: { session: null } }); },
                    onAuthStateChange: function() {},
                    signInWithOAuth: function() {},
                    signOut: function() {}
                },
                rpc: function(name) {
                    if (name === 'check_anon_usage') {
                        return Promise.resolve({ data: { allowed: false, remaining: 0 }, error: null });
                    }
                    return Promise.resolve({ data: null, error: null });
                }
            };
        };
        window._sb = null;
        window._sbUser = null;
        """
    )
    pid = "00-B-01-scaffolding-repositorio"
    app_page.click(f'.copy-btn[onclick*="{pid}\', \'es\'"]')
    app_page.wait_for_timeout(300)

    is_open = app_page.evaluate(
        "(document.getElementById('register-wall-modal') || {}).classList"
        ".contains('open')"
    )
    assert is_open, "El muro de registro no apareció con el límite anónimo agotado"

    clip = app_page.evaluate("navigator.clipboard.readText()")
    assert pid not in clip or clip == "", (
        "El copiado no debería haberse completado con el límite agotado"
    )


def test_feedback_wall_blocks_copy_until_submitted_then_renews(app_page):
    """Con sesión simulada y check_trial_status() devolviendo 'active: false'
    (prueba vencida), el intento de copia debe abrir el muro de feedback en
    vez de copiar. Al enviarlo (submit_feedback_and_renew stubeado con
    éxito), el modal se cierra y confirma la renovación."""
    app_page.evaluate(
        """
        window._sbUser = { id: 'fake-user-id', email: 'test@example.com' };
        window.supabase.createClient = function() {
            return {
                auth: {
                    getSession: function() { return Promise.resolve({ data: { session: null } }); },
                    onAuthStateChange: function() {},
                    signInWithOAuth: function() {},
                    signOut: function() {}
                },
                rpc: function(name, args) {
                    if (name === 'check_trial_status') {
                        return Promise.resolve({ data: { active: false, expires_at: '2020-01-01' }, error: null });
                    }
                    if (name === 'submit_feedback_and_renew') {
                        window.__renewCall = args;
                        return Promise.resolve({ data: { renewed: true, new_expires_at: '2099-01-01' }, error: null });
                    }
                    return Promise.resolve({ data: null, error: null });
                }
            };
        };
        window._sb = null;
        """
    )
    pid = "00-B-01-scaffolding-repositorio"
    app_page.click(f'.copy-btn[onclick*="{pid}\', \'es\'"]')
    app_page.wait_for_timeout(300)

    is_open = app_page.evaluate(
        "(document.getElementById('feedback-wall-modal') || {}).classList"
        ".contains('open')"
    )
    assert is_open, "El muro de feedback no apareció con la prueba vencida"

    app_page.click('#fb-stars .fb-star[data-value="4"]')
    app_page.fill("#fb-comments", "Muy útil, gracias.")
    app_page.click(".fb-submit-btn")
    app_page.wait_for_timeout(300)

    call = app_page.evaluate("window.__renewCall")
    assert call and call["p_rating"] == 4, f"submit_feedback_and_renew no recibió la calificación: {call!r}"

    still_open = app_page.evaluate(
        "(document.getElementById('feedback-wall-modal') || {}).classList"
        ".contains('open')"
    )
    assert not still_open, "El muro de feedback debería cerrarse tras enviar exitosamente"
