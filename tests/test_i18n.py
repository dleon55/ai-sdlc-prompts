#!/usr/bin/env python3
"""
test_i18n.py — Pruebas unitarias para sistema de internacionalización
Fase 5: Pruebas y Validación — Issue #28
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from i18n_strings import (
    get_string, get_landing_string, get_section_label,
    SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, UI_STRINGS, LANDING_STRINGS
)


def test_supported_languages() -> None:
    """Validar que hay exactamente 2 idiomas soportados"""
    assert len(SUPPORTED_LANGUAGES) == 2
    assert 'es' in SUPPORTED_LANGUAGES
    assert 'en' in SUPPORTED_LANGUAGES
    print("✓ SUPPORTED_LANGUAGES: es, en")


def test_default_language() -> None:
    """Validar que el idioma por defecto es español"""
    assert DEFAULT_LANGUAGE == 'es'
    print("✓ DEFAULT_LANGUAGE: es")


def test_get_string_fallback() -> None:
    """Validar fallback a idioma por defecto cuando el idioma no existe"""
    result = get_string('card_copy', 'fr')  # Francés no soportado
    assert result == UI_STRINGS['es']['card_copy']
    print("✓ get_string fallback: fr → es")


def test_get_string_es():
    """Validar obtención de string en español"""
    result = get_string('card_copy', 'es')
    assert result == 'Copiar'
    print("✓ get_string('card_copy', 'es'): 'Copiar'")


def test_get_string_en():
    """Validar obtención de string en inglés"""
    result = get_string('card_copy', 'en')
    assert result == 'Copy'
    print("✓ get_string('card_copy', 'en'): 'Copy'")


def test_get_landing_string_es():
    """Validar string de landing page en español"""
    result = get_landing_string('cta_primary', 'es')
    assert result == 'Probar gratis'
    print("✓ get_landing_string('cta_primary', 'es'): 'Probar gratis'")


def test_get_landing_string_en():
    """Validar string de landing page en inglés"""
    result = get_landing_string('cta_primary', 'en')
    assert result == 'Try for free'
    print("✓ get_landing_string('cta_primary', 'en'): 'Try for free'")


def test_all_ui_strings_have_both_languages():
    """Validar que todos los UI strings tienen versión ES y EN"""
    es_keys = set(UI_STRINGS['es'].keys())
    en_keys = set(UI_STRINGS['en'].keys())
    
    missing_in_en = es_keys - en_keys
    missing_in_es = en_keys - es_keys
    
    assert not missing_in_en, f"Keys faltantes en EN: {missing_in_en}"
    assert not missing_in_es, f"Keys faltantes en ES: {missing_in_es}"
    print(f"✓ UI_STRINGS: {len(es_keys)} keys con traducción ES/EN")


def test_all_landing_strings_have_both_languages():
    """Validar que todos los landing strings tienen versión ES y EN"""
    es_keys = set(LANDING_STRINGS['es'].keys())
    en_keys = set(LANDING_STRINGS['en'].keys())
    
    missing_in_en = es_keys - en_keys
    missing_in_es = en_keys - es_keys
    
    assert not missing_in_en, f"Keys faltantes en EN: {missing_in_en}"
    assert not missing_in_es, f"Keys faltantes en ES: {missing_in_es}"
    print(f"✓ LANDING_STRINGS: {len(es_keys)} keys con traducción ES/EN")


def test_section_labels():
    """Validar que todas las secciones tienen label en ambos idiomas"""
    from i18n_strings import SECTION_LABELS_I18N
    
    for section_num in range(13):  # 00-12
        section_key = f"{section_num:02d}"
        assert section_key in SECTION_LABELS_I18N['es'], f"Sección {section_key} sin label ES"
        assert section_key in SECTION_LABELS_I18N['en'], f"Sección {section_key} sin label EN"
    
    print(f"✓ SECTION_LABELS_I18N: 13 secciones con traducción ES/EN")


def run_all_tests() -> bool:
    """Ejecutar todas las pruebas"""
    print("=" * 60)
    print("PRUEBAS UNITARIAS I18N — Fase 5")
    print("=" * 60)
    
    tests = [
        test_supported_languages,
        test_default_language,
        test_get_string_fallback,
        test_get_string_es,
        test_get_string_en,
        test_get_landing_string_es,
        test_get_landing_string_en,
        test_all_ui_strings_have_both_languages,
        test_all_landing_strings_have_both_languages,
        test_section_labels,
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
    
    print("=" * 60)
    print(f"RESULTADO: {passed} pasadas, {failed} fallidas")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
