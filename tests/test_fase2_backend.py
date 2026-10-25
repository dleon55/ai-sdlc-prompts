"""Fase 2 de la salida de Supabase (issue #241).

Proyectos, progreso y estadísticas de copia pasan al backend propio; el login,
la prueba y los pagos siguen en Supabase hasta la Fase 3. Estas pruebas fijan
ese reparto en nginx y en el sitio generado.
"""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NGINX = (RAIZ / "nginx_prompts.conf").read_text(encoding="utf-8")
BUILD = (RAIZ / "build.py").read_text(encoding="utf-8")


def _bloque_api():
    m = re.search(r"location ~ \^/api/\(([^)]*)\)\(/\|\$\) \{(.*?)\n    \}", NGINX, re.S)
    assert m, "falta el location del backend en nginx_prompts.conf"
    return m.group(1).split("|"), m.group(2)


def test_nginx_publica_solo_las_rutas_de_la_fase_2():
    rutas, _ = _bloque_api()
    assert sorted(rutas) == sorted(["projects", "project-prompt-state", "prompt-stats/track", "health"])
    for ruta_de_fase_3 in ("auth", "trial", "webhooks", "founding"):
        assert ruta_de_fase_3 not in rutas, f"/api/{ruta_de_fase_3} no se publica hasta la Fase 3"


def test_nginx_llega_al_backend_por_loopback_con_limite():
    _, cuerpo = _bloque_api()
    assert "proxy_pass http://127.0.0.1:8787;" in cuerpo
    assert "limit_req zone=ai_sdlc_api" in cuerpo
    assert "client_max_body_size 1m;" in cuerpo
    assert re.search(r"^limit_req_zone \$binary_remote_addr zone=ai_sdlc_api:", NGINX, re.M)


def test_otras_rutas_api_dan_404_y_no_el_index():
    assert re.search(r"location /api/ \{\s*return 404;\s*\}", NGINX)


def test_el_sitio_ya_no_usa_supabase_para_los_datos_migrados():
    assert not re.search(r"\.from\(['\"](projects|project_prompt_state)['\"]\)", BUILD)
    assert "rpc('track_prompt_copy'" not in BUILD
    for ruta in ("/api/projects", "/api/project-prompt-state", "/api/prompt-stats/track"):
        assert ruta in BUILD


def test_la_prueba_y_los_pagos_siguen_en_supabase():
    # Fase 3: no deben moverse en este cambio.
    assert "rpc('check_trial_status')" in BUILD
    assert "rpc('submit_feedback_and_renew'" in BUILD
    assert "customData:{user_id:_pxUser.id}" in BUILD


def test_backend_api_manda_el_token_de_supabase_y_no_cookies():
    m = re.search(r"function backendApi\(method, path, body, conSesion\) \{(.*?)\n\}\n", BUILD, re.S)
    assert m, "falta backendApi en build.py"
    cuerpo = m.group(1)
    assert "client.auth.getSession()" in cuerpo
    assert "'Bearer ' + t" in cuerpo
    assert "credentials: 'omit'" in cuerpo
    assert "resolve(null)" in cuerpo and "catch" in cuerpo
