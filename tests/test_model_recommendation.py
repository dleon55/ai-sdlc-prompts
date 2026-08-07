#!/usr/bin/env python3
"""Contrato de la recomendación de modelo (etapa 2 de gobernanza).

No se puede pedirle lo mismo a un modelo de razonamiento profundo que a
uno rápido, pero la biblioteca daba una sola versión y el usuario
adivinaba. Esta capa deriva una sugerencia de datos que YA existen en el
contrato editorial: `Riesgo esperado` y `Autonomía permitida`.

La regla en una línea: el riesgo fija el piso, la autonomía lo mueve.
"""
import build


def test_risk_sets_the_floor():
    assert build.recommend_model_tier(["low"], [])["tier"] == "rapido"
    assert build.recommend_model_tier(["medium"], [])["tier"] == "general"
    assert build.recommend_model_tier(["high"], [])["tier"] == "razonamiento"


def test_executing_changes_raises_the_bar():
    """A2/A3 significa que el agente ESCRIBE, no solo propone. Un error
    deja de ser un mal párrafo y pasa a ser código o infraestructura
    tocada, así que se exige más capacidad."""
    base = build.recommend_model_tier(["low"], ["A1"])["tier"]
    con_ejecucion = build.recommend_model_tier(["low"], ["A1", "A3"])["tier"]

    assert base == "rapido"
    assert con_ejecucion == "general"
    assert "ejecuta_cambios" in build.recommend_model_tier(["low"], ["A3"])["razones"]


def test_analysis_only_lowers_the_bar():
    """A0 no escribe nada: el peor caso es una lectura equivocada que un
    humano descarta. No hace falta pagar el modelo caro."""
    rec = build.recommend_model_tier(["medium"], ["A0"])
    assert rec["tier"] == "rapido"
    assert "solo_analiza" in rec["razones"]


def test_the_scale_never_overflows():
    """Subir desde el nivel máximo o bajar desde el mínimo no debe
    reventar por índice fuera de rango."""
    assert build.recommend_model_tier(["high"], ["A3"])["tier"] == "razonamiento"
    assert build.recommend_model_tier(["low"], ["A0"])["tier"] == "rapido"


def test_high_risk_plus_execution_demands_human_review():
    """Riesgo alto Y ejecución es donde un humano debe mirar antes de que
    el resultado toque algo real."""
    assert build.recommend_model_tier(["high"], ["A3"])["revision_humana"] is True
    # Alto riesgo pero solo proponiendo: no hace falta la marca.
    assert build.recommend_model_tier(["high"], ["A1"])["revision_humana"] is False
    # Ejecuta, pero el riesgo es bajo: tampoco.
    assert build.recommend_model_tier(["low"], ["A3"])["revision_humana"] is False


def test_no_recommendation_without_a_basis():
    """Preferible callar a inventar. Los meta-prompts de enrutamiento
    declaran riesgo 'variable' porque heredan el del prompt al que
    derivan: no hay nivel fijo que sugerir."""
    assert build.recommend_model_tier(["variable"], ["A1"]) is None
    assert build.recommend_model_tier([], []) is None
    assert build.recommend_model_tier(None, None) is None


def test_the_hint_explains_why_not_just_what():
    """Sin el porqué, la recomendación es un oráculo y el usuario nunca
    aprende a decidir solo."""
    rec = build.recommend_model_tier(["high"], ["A3"])
    for lang in ("es", "en"):
        texto = build._model_hint_text(rec, lang)
        assert build.MODEL_EXAMPLES_REVIEWED in texto, "los ejemplos deben ir fechados"
        assert len(texto) > 60, "debe explicar, no solo etiquetar"


def test_model_examples_are_dated_in_a_single_place():
    """Los nombres de modelo caducan en meses. Deben vivir en UNA tabla
    fechada: recomendar un modelo descontinuado es peor que no
    recomendar nada."""
    assert build.MODEL_EXAMPLES_REVIEWED
    # La logica razona en niveles, no en nombres.
    assert "Opus" not in str(build._MODEL_TIERS)
    assert set(build._TIER_EXAMPLES) == set(build._MODEL_TIERS)


def test_every_prompt_gets_a_recommendation_or_an_explicit_none():
    """Sobre el catálogo real: ningún prompt debe reventar la regla."""
    import json
    from pathlib import Path

    raw = json.loads(Path("prompts-index.json").read_text(encoding="utf-8"))
    prompts = raw if isinstance(raw, list) else raw.get("prompts", raw)
    prompts = prompts if isinstance(prompts, list) else list(prompts.values())
    assert prompts, "no se cargó el índice"

    con_rec = 0
    for p in prompts:
        es = (p.get("contract") or {}).get("es") or {}
        rt = build._extract_tags(es.get("expected_risk", ""), build._RISK_TAGS)
        at = build._extract_autonomy_tags(es.get("permitted_autonomy", ""))
        rec = build.recommend_model_tier(rt, at)  # no debe lanzar
        if rec:
            assert rec["tier"] in build._MODEL_TIERS
            con_rec += 1

    # Si la cobertura cae drasticamente, algo se rompio en la extraccion
    # de tags y la recomendacion dejaria de aparecer sin aviso.
    assert con_rec > len(prompts) * 0.8, (
        f"solo {con_rec}/{len(prompts)} prompts obtienen recomendación"
    )
