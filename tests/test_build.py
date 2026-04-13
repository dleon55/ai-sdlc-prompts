#!/usr/bin/env python3
"""
test_build.py — Pruebas de validación del build
Fase 5: Pruebas y Validación — Issue #28
"""

import sys
import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_index_html_exists():
    """Validar que index.html existe"""
    index_file = PROJECT_ROOT / "index.html"
    assert index_file.exists(), "index.html no encontrado"
    print("✓ index.html existe")


def test_index_html_size():
    """Validar que index.html está dentro del tamaño esperado (< 1MB)"""
    index_file = PROJECT_ROOT / "index.html"
    size_bytes = index_file.stat().st_size
    size_kb = size_bytes / 1024
    assert size_kb < 1024, f"index.html muy grande: {size_kb:.1f}KB (esperado < 1024KB)"
    print(f"✓ index.html tamaño: {size_kb:.1f}KB (< 1024KB)")


def test_data_lang_es_present():
    """Validar presencia de atributos data-lang='es'"""
    index_file = PROJECT_ROOT / "index.html"
    content = index_file.read_text(encoding='utf-8')
    matches = re.findall(r'data-lang="es"', content)
    assert len(matches) > 0, "No se encontraron atributos data-lang='es'"
    print(f"✓ data-lang='es' encontrado: {len(matches)} veces")


def test_data_lang_en_present():
    """Validar presencia de atributos data-lang='en'"""
    index_file = PROJECT_ROOT / "index.html"
    content = index_file.read_text(encoding='utf-8')
    matches = re.findall(r'data-lang="en"', content)
    assert len(matches) > 0, "No se encontraron atributos data-lang='en'"
    print(f"✓ data-lang='en' encontrado: {len(matches)} veces")


def test_hreflang_es_present():
    """Validar presencia de hreflang es"""
    index_file = PROJECT_ROOT / "index.html"
    content = index_file.read_text(encoding='utf-8')
    assert 'hreflang="es"' in content, "hreflang='es' no encontrado"
    print("✓ hreflang='es' presente")


def test_hreflang_en_present():
    """Validar presencia de hreflang en"""
    index_file = PROJECT_ROOT / "index.html"
    content = index_file.read_text(encoding='utf-8')
    assert 'hreflang="en"' in content, "hreflang='en' no encontrado"
    print("✓ hreflang='en' presente")


def test_html_lang_attribute():
    """Validar que html lang se establece correctamente"""
    index_file = PROJECT_ROOT / "index.html"
    content = index_file.read_text(encoding='utf-8')
    # El HTML generado debe tener lang="es" por defecto
    assert '<html lang="es"' in content or 'document.documentElement.lang' in content, \
        "Atributo lang no configurado correctamente"
    print("✓ html lang atributo configurado")


def test_css_i18n_selectors_present():
    """Validar que los selectores CSS para i18n están presentes"""
    index_file = PROJECT_ROOT / "index.html"
    content = index_file.read_text(encoding='utf-8')
    assert 'html[data-lang="es"]' in content, "CSS selector html[data-lang='es'] no encontrado"
    assert 'html[data-lang="en"]' in content, "CSS selector html[data-lang='en'] no encontrado"
    print("✓ CSS selectors html[data-lang] presentes")


def test_framework_dual_language():
    """Validar que el framework está en ambos idiomas"""
    index_file = PROJECT_ROOT / "index.html"
    content = index_file.read_text(encoding='utf-8')
    # Buscar IDs de framework en ambos idiomas
    assert 'sec-00-es' in content or 'code-fw-es' in content, "Framework ES no encontrado"
    assert 'sec-00-en' in content or 'code-fw-en' in content, "Framework EN no encontrado"
    print("✓ Framework bilingüe presente")


def test_js_i18n_functions_present():
    """Validar que funciones i18n de JavaScript están presentes"""
    index_file = PROJECT_ROOT / "index.html"
    content = index_file.read_text(encoding='utf-8')
    assert 'setLanguage' in content, "Función setLanguage no encontrada"
    assert 'getCurrentLanguage' in content, "Función getCurrentLanguage no encontrada"
    assert 'openInfoLang' in content, "Función openInfoLang no encontrada"
    assert 'copyPromptLang' in content, "Función copyPromptLang no encontrada"
    print("✓ Funciones JavaScript i18n presentes")


def run_all_tests():
    """Ejecutar todas las pruebas de build"""
    print("=" * 60)
    print("PRUEBAS DE BUILD — Fase 5")
    print("=" * 60)
    
    tests = [
        test_index_html_exists,
        test_index_html_size,
        test_data_lang_es_present,
        test_data_lang_en_present,
        test_hreflang_es_present,
        test_hreflang_en_present,
        test_html_lang_attribute,
        test_css_i18n_selectors_present,
        test_framework_dual_language,
        test_js_i18n_functions_present,
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
