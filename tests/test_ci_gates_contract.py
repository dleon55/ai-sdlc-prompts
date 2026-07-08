#!/usr/bin/env python3
"""
tests/test_ci_gates_contract.py — Contrato del workflow de CI/CD

Bloquea que un futuro cambio a .github/workflows/deploy.yml elimine
silenciosamente alguno de los 5 gates obligatorios antes de desplegar, o
reintroduzca un umbral de smoke test hardcodeado que vuelva a quedar
obsoleto (como pasó con ">=44" cuando la biblioteca creció a 75 prompts).
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
WORKFLOW = (PROJECT_ROOT / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")

GATES_IN_ORDER = (
    "python build.py",
    "python verify_clean.py",
    "python extract_vars.py",
    "node tests/js/test_variables_runtime.js",
    "python -m pytest",
)


def test_build_job_runs_all_four_gates():
    for gate in GATES_IN_ORDER:
        assert gate in WORKFLOW, f"Gate faltante en el workflow: {gate}"


def test_gates_run_in_order_before_any_deploy_job():
    indices = [WORKFLOW.index(gate) for gate in GATES_IN_ORDER]
    assert indices == sorted(indices), "Los gates no corren en el orden esperado"
    deploy_pages_idx = WORKFLOW.index("deploy-pages:")
    assert indices[-1] < deploy_pages_idx, "Un gate corre después de que empieza el deploy"


def test_deploy_jobs_depend_on_build_job():
    assert "needs: build" in WORKFLOW
    assert "needs: [build, deploy-pages]" in WORKFLOW


def test_deploy_jobs_restricted_to_push_on_main():
    assert "github.event_name == 'push' && github.ref == 'refs/heads/main'" in WORKFLOW


def test_smoke_test_threshold_is_derived_from_build_not_hardcoded():
    assert 'card_count: ${{ steps.card_count.outputs.count }}' in WORKFLOW
    assert "needs.build.outputs.card_count" in WORKFLOW
    assert "-ge 44" not in WORKFLOW
    assert ">= 44" not in WORKFLOW
