#!/usr/bin/env python3
"""El deploy aplica la configuración de nginx, y lo hace sin tumbar 8 sitios.

Durante meses el deploy copió HTML pero **nunca** `nginx_prompts.conf`, así
que el archivo del repositorio y el del servidor divergieron en silencio. Se
descubrió por dos síntomas que parecían no tener relación:

  - la CSP del servidor bloqueaba el favicon del propio sitio;
  - la compresión era nivel 1 en vez de 6, porque al servidor le faltaba
    `gzip_comp_level` -- por eso `index.html` pesaba 284 KB en la red y no
    los 222 KB del cálculo local.

**Este nginx sirve 8 sitios**, entre ellos un Odoo de producción y una API.
Un `reload` con configuración inválida los tumba todos, no solo este. Estas
pruebas protegen las propiedades que hacen seguro aplicarla automáticamente.
"""

import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
SCRIPT = RAIZ / "scripts" / "aplicar-nginx.sh"
WORKFLOW = RAIZ / ".github" / "workflows" / "deploy.yml"
CONF = RAIZ / "nginx_prompts.conf"


@pytest.fixture(scope="module")
def script():
    return SCRIPT.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def codigo():
    """El script sin comentarios.

    El encabezado documenta el orden de las operaciones y menciona
    `nginx -t` y `reload` en prosa. Comprobar posiciones sobre el archivo
    crudo comparaba comentarios en vez de código: una mutación que recargaba
    nginx ANTES de validar pasaba el test sin problema. Lo detectó la propia
    verificación por mutación de estas pruebas.
    """
    return "\n".join(
        l for l in SCRIPT.read_text(encoding="utf-8").splitlines()
        if not l.lstrip().startswith("#")
    )


# ── El deploy la aplica ───────────────────────────────────────────────

def test_el_deploy_envia_la_configuracion_y_el_script():
    w = WORKFLOW.read_text(encoding="utf-8")
    assert "nginx_prompts.conf.new" in w, "el deploy no envía la configuración al servidor"
    assert "scripts/aplicar-nginx.sh" in w, "el deploy no envía el script que la aplica"
    assert "aplicar-nginx.sh\"" in w, "el deploy no ejecuta el script"


# ── Nunca se recarga con una configuración inválida ───────────────────

def test_valida_antes_de_recargar(codigo):
    """La invariante que protege a los otros 7 sitios."""
    i_test = codigo.index("nginx -t")
    i_reload = codigo.index("systemctl reload")
    assert i_test < i_reload, "se recargaría nginx antes de validar la configuración"


def test_si_no_valida_restaura_y_no_recarga(script):
    bloque = script[script.index("if ! sudo nginx -t"):]
    bloque = bloque[:bloque.index("systemctl reload")]
    assert 'cp -p "$RESPALDO" "$DEST"' in bloque, "no restaura el respaldo cuando falla la validación"
    assert "exit 1" in bloque, "no aborta cuando la configuración es inválida"


def test_recarga_en_caliente_nunca_reinicia(codigo):
    """`restart` corta las conexiones de los 8 sitios; `reload` no."""
    assert "systemctl reload nginx" in codigo
    assert "restart nginx" not in codigo, "un restart cortaría el servicio de los demás sitios"


def test_respalda_antes_de_tocar_nada(codigo):
    i_respaldo = codigo.index('cp -p "$DEST" "$RESPALDO"')
    i_install = codigo.index("install -o root")
    assert i_respaldo < i_install, "instala la nueva configuración antes de respaldar la anterior"


def test_no_hace_nada_si_la_configuracion_no_cambio(script):
    """El caso normal: casi todos los despliegues no tocan nginx."""
    assert 'cmp -s "$NUEVO" "$DEST"' in script


def test_no_crea_sitios_nuevos(script):
    """Crear un vhost requiere además symlink y certificado: eso es manual."""
    assert '[ -f "$DEST" ]' in script


# ── La comprobación de salud ──────────────────────────────────────────

def test_la_comprobacion_de_salud_usa_https(script):
    """El sitio responde 301 en HTTP (redirige a HTTPS).

    Una comprobación por HTTP que espere 200 revertiría en CADA despliegue
    aunque la configuración fuera correcta. Se detectó probando el script
    contra el servidor real antes de conectarlo al deploy.
    """
    bloque = script[script.index("CODIGO=$("):script.index("if [ \"$CODIGO\"")]
    assert "https://" in bloque, "la comprobación por HTTP daría 301 y revertiría siempre"
    assert "--resolve" in bloque, "sin --resolve la comprobación depende del DNS externo"


def test_si_el_sitio_no_responde_revierte(script):
    bloque = script[script.index('if [ "$CODIGO" != "200" ]'):]
    assert 'cp -p "$RESPALDO" "$DEST"' in bloque
    assert "systemctl reload nginx" in bloque, "restaura el archivo pero no recarga: quedaría sin efecto"


# ── HSTS: una puerta de un solo sentido ───────────────────────────────

def test_hsts_no_vuelve_a_valores_irreversibles():
    """HSTS obliga al navegador a rechazar HTTP durante todo el `max-age`,
    aunque se quite la cabecera del servidor.

    El valor anterior (2 años + `includeSubDomains` + `preload`) convertía
    un certificado vencido en un sitio inalcanzable, sin forma práctica de
    revertir. Se decidió empezar en 1 día y subir por pasos.

    Si alguien sube el valor, que sea una decisión y no un descuido.
    """
    conf = CONF.read_text(encoding="utf-8")
    m = re.search(r'Strict-Transport-Security "([^"]+)"', conf)
    assert m, "falta la cabecera HSTS"
    valor = m.group(1)

    edad = int(re.search(r"max-age=(\d+)", valor).group(1))
    assert edad <= 604800, (
        f"max-age={edad} son {edad // 86400} días de compromiso irreversible. "
        "Subirlo por pasos (1 día -> 1 semana -> 1 año) y solo tras semanas estable."
    )
    assert "preload" not in valor, (
        "`preload` exige enviarlo a hstspreload.org y salir de esa lista tarda meses"
    )
