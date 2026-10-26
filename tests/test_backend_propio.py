"""Salida de Supabase (issue #241): el sitio usa solo el backend propio.

Login con GitHub, sesión, prueba, proyectos, estadísticas y el webhook de
Paddle viven en backend/, publicado por nginx en /api/ del mismo dominio.
"""
import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NGINX = (RAIZ / "nginx_prompts.conf").read_text(encoding="utf-8")
BUILD = (RAIZ / "build.py").read_text(encoding="utf-8")


def test_nginx_publica_el_backend_por_loopback_con_limite():
    m = re.search(r"location /api/ \{(.*?)\n    \}", NGINX, re.S)
    assert m, "falta location /api/ en nginx_prompts.conf"
    cuerpo = m.group(1)
    assert "proxy_pass http://127.0.0.1:8787;" in cuerpo
    assert "limit_req zone=ai_sdlc_api" in cuerpo
    assert "limit_req_status 429;" in cuerpo
    assert "client_max_body_size 1m;" in cuerpo
    assert re.search(r"^limit_req_zone \$binary_remote_addr zone=ai_sdlc_api:", NGINX, re.M)


def test_el_sitio_no_usa_ningun_sdk_ni_rpc_de_supabase():
    assert "supabase" not in BUILD.lower()
    assert ".rpc(" not in BUILD
    assert not re.search(r"\.from\(['\"](projects|project_prompt_state)['\"]\)", BUILD)


def test_el_sitio_llama_a_las_rutas_del_backend():
    for ruta in (
        "/api/auth/session", "/api/auth/logout", "/api/auth/login?volver=",
        "/api/trial/status", "/api/trial/feedback",
        "/api/projects", "/api/project-prompt-state", "/api/prompt-stats/track",
        "/api/founding/spots-left",
    ):
        assert ruta in BUILD, ruta


def test_backend_api_usa_la_cookie_del_mismo_origen_y_nunca_lanza():
    m = re.search(r"function backendApi\(method, path, body\) \{(.*?)\n\}\n", BUILD, re.S)
    assert m, "falta backendApi en build.py"
    cuerpo = m.group(1)
    assert "credentials: 'same-origin'" in cuerpo
    assert "Authorization" not in cuerpo, "la sesión viaja en la cookie httpOnly, no en un header"
    assert cuerpo.count("resolve(null)") >= 4 and "catch" in cuerpo


def test_el_checkout_manda_el_usuario_de_la_sesion_propia():
    assert "customData:{user_id:_pxUser.id}" in BUILD
    assert "_pxUser=(res&&res.user)?res.user:null;" in BUILD


# Filas de tablas de historial de versiones ("| 1.1 | 2026-08-02 | ... |"):
# registran lo que se hizo entonces y no se reescriben.
_FILA_DE_HISTORIAL = re.compile(r"^\|\s*\d+(\.\d+)+\s*\|\s*\d{4}-\d{2}-\d{2}\s*\|")


def test_no_queda_rastro_de_supabase_en_el_repositorio_salvo_la_historia():
    salida = subprocess.run(
        ["git", "grep", "-in", "supabase", "--", ".",
         ":!CHANGELOG.md", ":!docs/PLAN_MIGRACION_SUPABASE_A_LOCAL.md", ":!tests/test_backend_propio.py",
         ":!tests/test_build.py", ":!tests/test_nginx_security_headers.py", ":!tests/test_cobro_transversal.py",
         ":!tests/e2e/test_browser_e2e.py"],
        cwd=RAIZ, capture_output=True, text=True,
    )
    restos = []
    for linea in salida.stdout.splitlines():
        partes = linea.split(":", 2)
        if len(partes) == 3 and _FILA_DE_HISTORIAL.match(partes[2].strip()):
            continue
        restos.append(linea)
    assert restos == [], "todavía se menciona Supabase:\n" + "\n".join(restos)


def test_la_portada_tiene_boton_de_inicio_de_sesion_visible():
    """El botón de cuenta de la app vive en /app; la portada tenía solo
    "Explorar prompts" y un visitante nuevo no encontraba cómo entrar."""
    index = (RAIZ / "index.html").read_text(encoding="utf-8")
    assert re.search(r'<nav class="landing-nav">.*id="landing-auth-btn".*</nav>', index, re.S)
    assert "signInWithGitHub('/app')" in BUILD, "desde la portada se entra directo a la app"
    assert "function renderLandingAuth()" in BUILD
    assert re.search(r"function renderAuthUI\(\) \{\n  renderLandingAuth\(\);", BUILD)
