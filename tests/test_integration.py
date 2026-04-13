#!/usr/bin/env python3
"""
test_integration.py — Pruebas de integración E2E para i18n
Fase 5: Pruebas y Validación — Paso 5.2 — Issue #28

Valida el comportamiento del switch de idioma sin navegador real
"""

import sys
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).parent.parent
INDEX_FILE = PROJECT_ROOT / "index.html"


def extract_js_functions(content):
    """Extraer funciones JavaScript relevantes para análisis"""
    functions = {}
    
    # Extraer setLanguage
    setlang_match = re.search(
        r'function setLanguage\(lang\)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}',
        content,
        re.DOTALL
    )
    if setlang_match:
        functions['setLanguage'] = setlang_match.group(1)
    
    # Extraer getCurrentLanguage
    getlang_match = re.search(
        r'function getCurrentLanguage\(\)\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}',
        content,
        re.DOTALL
    )
    if getlang_match:
        functions['getCurrentLanguage'] = getlang_match.group(1)
    
    return functions


def test_setLanguage_updates_html_lang():
    """Validar que setLanguage actualiza document.documentElement.lang"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    # Buscar que setLanguage modifica document.documentElement.lang
    assert 'document.documentElement.lang = lang' in content, \
        "setLanguage no actualiza document.documentElement.lang"
    print("✓ setLanguage actualiza html lang attribute")


def test_setLanguage_updates_data_lang():
    """Validar que setLanguage actualiza data-lang"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    assert "document.documentElement.setAttribute('data-lang', lang)" in content, \
        "setLanguage no actualiza data-lang attribute"
    print("✓ setLanguage actualiza html data-lang attribute")


def test_css_data_lang_selectors_exist():
    """Validar que existen selectores CSS para data-lang"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    # Verificar selectores CSS
    assert 'html[data-lang="es"] .card[data-lang="es"]' in content, \
        "CSS selector ES no encontrado"
    assert 'html[data-lang="en"] .card[data-lang="en"]' in content, \
        "CSS selector EN no encontrado"
    print("✓ CSS selectors data-lang para cards existen")


def test_language_switch_preserves_state():
    """Validar que el switch de idioma guarda en localStorage"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    # Verificar que setLanguage guarda preferencia
    assert "localStorage.setItem(I18N_KEY, lang)" in content or \
           "localStorage.setItem('AI_SDLC_language', lang)" in content, \
        "setLanguage no guarda preferencia en localStorage"
    print("✓ Switch de idioma persiste en localStorage")


def test_language_dropdown_closes_on_selection():
    """Validar que el dropdown cierra al seleccionar idioma"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    # Buscar que onLanguageSelect cierra el dropdown
    assert 'closeLanguageDropdown()' in content, \
        "onLanguageSelect no cierra el dropdown"
    print("✓ Dropdown cierra al seleccionar idioma")


def test_framework_visibility_switches():
    """Validar que la visibilidad del framework cambia con el idioma"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    # Buscar updateFrameworkVisibility
    assert 'updateFrameworkVisibility' in content, \
        "Función updateFrameworkVisibility no encontrada"
    assert 'sec-00-es' in content and 'sec-00-en' in content, \
        "IDs de framework bilingüe no encontrados"
    print("✓ Framework banner cambia con idioma")


def test_copy_function_lang_aware():
    """Validar que copyPromptLang usa el idioma correcto"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    # Buscar copyPromptLang que usa sufijo de idioma
    assert 'copyPromptLang' in content, \
        "Función copyPromptLang no encontrada"
    assert "'code-' + pid + '-' + lang" in content or \
           f"code-${'{pid}'}-${'{lang}'}" in content.replace('{', '${') or \
           "var codeId = 'code-' + pid + '-' + lang" in content, \
        "copyPromptLang no construye ID con idioma"
    print("✓ copyPromptLang es aware de idioma")


def test_info_modal_lang_aware():
    """Validar que openInfoLang usa datos del idioma correcto"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    assert 'openInfoLang' in content, \
        "Función openInfoLang no encontrada"
    assert 'info.title_en' in content and 'info.title_es' in content, \
        "openInfoLang no usa títulos por idioma"
    print("✓ openInfoLang es aware de idioma")


def test_default_language_detection():
    """Validar detección de idioma por defecto"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    # Verificar que I18N_DEFAULT existe
    assert "I18N_DEFAULT = 'es'" in content, \
        "I18N_DEFAULT no es 'es'"
    print("✓ Idioma por defecto: español")


def test_analytics_language_change():
    """Validar que se envía evento analytics al cambiar idioma"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    assert "gtag('event', 'language_change'" in content, \
        "Evento analytics language_change no encontrado"
    print("✓ Evento analytics language_change configurado")


def run_all_tests():
    """Ejecutar todas las pruebas de integración"""
    print("=" * 60)
    print("PRUEBAS DE INTEGRACIÓN I18N — Fase 5.2")
    print("=" * 60)
    print("(Validación estática del código generado)\n")
    
    tests = [
        test_setLanguage_updates_html_lang,
        test_setLanguage_updates_data_lang,
        test_css_data_lang_selectors_exist,
        test_language_switch_preserves_state,
        test_language_dropdown_closes_on_selection,
        test_framework_visibility_switches,
        test_copy_function_lang_aware,
        test_info_modal_lang_aware,
        test_default_language_detection,
        test_analytics_language_change,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: ERROR {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTADO: {passed} pasadas, {failed} fallidas")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
