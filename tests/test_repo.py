"""Lo que `.gitignore` deja fuera no está en el repo: notas internas, claves, datos grandes y archivos locales.

`.gitignore` es la lista de lo que no se publica. Si alguien agrega a la fuerza un archivo de esa lista
(`git add -f`), esta prueba falla.
"""
import subprocess
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent


def test_nada_de_lo_que_excluye_gitignore_esta_rastreado():
    try:
        r = subprocess.run(["git", "ls-files", "--cached", "--ignored", "--exclude-standard", "-z"],
                           cwd=RAIZ, capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("sin git o fuera de un repositorio")
    rastreados = [x for x in r.stdout.decode("utf-8", "replace").split("\0") if x]
    assert rastreados == []
