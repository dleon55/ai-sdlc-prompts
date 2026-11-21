"""Fixtures compartidas.

`paquete_mcp`: el servidor MCP se movió a https://github.com/dleon55/ai-sdlc-mcp
(nov-2026). Las pruebas de aquí que lo verifican (paridad del contrato de
operación, licencia del paquete) se corren contra el paquete publicado en npm,
que es lo que realmente reciben los usuarios. AI_SDLC_MCP_PKG_DIR permite
apuntar a un checkout local de ai-sdlc-mcp en su lugar.

Sin npm o sin red se omiten en local; en CI (variable CI) fallan, para que no
dejen de correr en silencio.
"""

import os
import shutil
import subprocess
import tarfile
from pathlib import Path

import pytest

PAQUETE_NPM = "ai-sdlc-prompts-mcp"


def _no_disponible(motivo):
    if os.environ.get("CI"):
        pytest.fail(f"paquete MCP no disponible en CI: {motivo}")
    pytest.skip(f"paquete MCP no disponible: {motivo}")


@pytest.fixture(scope="session")
def paquete_mcp(tmp_path_factory):
    local = os.environ.get("AI_SDLC_MCP_PKG_DIR", "").strip()
    if local:
        return Path(local)
    npm = shutil.which("npm")
    if not npm:
        _no_disponible("npm no está instalado")
    destino = tmp_path_factory.mktemp("paquete-mcp")
    try:
        r = subprocess.run(
            [npm, "pack", f"{PAQUETE_NPM}@latest", "--silent", "--pack-destination", str(destino)],
            capture_output=True, text=True, timeout=120, check=True,
        )
    except (subprocess.SubprocessError, OSError) as e:
        _no_disponible(f"npm pack falló: {e}")
    tgz = destino / r.stdout.strip().splitlines()[-1]
    with tarfile.open(tgz) as tar:
        tar.extractall(destino, filter="data")
    return destino / "package"
