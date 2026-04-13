#!/usr/bin/env python3
"""
test_coverage.py — Validación de cobertura de traducciones
Fase 5: Pruebas y Validación — Paso 5.8 — Issue #28

Valida que los 44 prompts tengan archivo .en.md correspondiente
"""

import sys
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = PROJECT_ROOT / "ai_sdlc_pro_prompts"


def get_all_prompts():
    """Obtener lista de todos los prompts (archivos .md sin .en.md)"""
    all_files = sorted(PROMPTS_DIR.glob("*.md"))
    prompts = []
    
    for f in all_files:
        name = f.stem
        # Ignorar archivos .en.md y framework
        if name.endswith(".en") or name == "00-framework":
            continue
        prompts.append(name)
    
    return prompts


def check_translation_coverage(prompts):
    """Verificar que cada prompt tenga traducción EN"""
    results = {
        'translated': [],
        'missing': [],
        'by_section': defaultdict(lambda: {'total': 0, 'translated': 0})
    }
    
    for prompt in prompts:
        section = prompt.split("-")[0]
        en_file = PROMPTS_DIR / f"{prompt}.en.md"
        
        results['by_section'][section]['total'] += 1
        
        if en_file.exists():
            results['translated'].append(prompt)
            results['by_section'][section]['translated'] += 1
        else:
            results['missing'].append(prompt)
    
    return results


def print_section_report(by_section):
    """Imprimir reporte por sección"""
    print("\n📊 COBERTURA POR SECCIÓN:")
    print("-" * 50)
    print(f"{'Sección':<10} {'Total':<8} {'Traducidos':<12} {'%':<8}")
    print("-" * 50)
    
    total_prompts = 0
    total_translated = 0
    
    for section in sorted(by_section.keys()):
        data = by_section[section]
        total = data['total']
        translated = data['translated']
        percentage = (translated / total * 100) if total > 0 else 0
        
        total_prompts += total
        total_translated += translated
        
        status = "✓" if translated == total else "⚠"
        print(f"{section:<10} {total:<8} {translated:<12} {percentage:>5.1f}% {status}")
    
    print("-" * 50)
    overall_pct = (total_translated / total_prompts * 100) if total_prompts > 0 else 0
    print(f"{'TOTAL':<10} {total_prompts:<8} {total_translated:<12} {overall_pct:>5.1f}%")
    print("-" * 50)
    
    return total_prompts, total_translated, overall_pct


def main():
    print("=" * 60)
    print("VALIDACIÓN DE COBERTURA I18N — Fase 5.8")
    print("=" * 60)
    
    # Obtener todos los prompts
    prompts = get_all_prompts()
    print(f"\n📁 Total prompts encontrados: {len(prompts)}")
    
    # Verificar cobertura
    results = check_translation_coverage(prompts)
    
    # Reporte por sección
    total, translated, percentage = print_section_report(results['by_section'])
    
    # Reporte de faltantes
    if results['missing']:
        print(f"\n⚠️  PROMPTS SIN TRADUCCIÓN ({len(results['missing'])}):")
        for p in results['missing']:
            print(f"   - {p}")
    else:
        print("\n✅ Todos los prompts tienen traducción EN")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN:")
    print(f"  • Total prompts: {total}")
    print(f"  • Traducidos: {translated}")
    print(f"  • Faltantes: {len(results['missing'])}")
    print(f"  • Cobertura: {percentage:.1f}%")
    
    if percentage == 100:
        print("  • Estado: ✅ COBERTURA COMPLETA")
    elif percentage >= 90:
        print("  • Estado: ⚠️  COBERTURA ALTA (≥90%)")
    else:
        print("  • Estado: ❌ COBERTURA INSUFICIENTE (<90%)")
    
    print("=" * 60)
    
    # Éxito si 100% de cobertura
    return len(results['missing']) == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
