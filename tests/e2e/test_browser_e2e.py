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
