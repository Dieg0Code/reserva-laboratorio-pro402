from pathlib import Path

import pytest

import almacen


@pytest.fixture
def base_de_datos_de_prueba(tmp_path: Path) -> Path:
    ruta_real = almacen.RUTA_BASE
    almacen.RUTA_BASE = tmp_path / "reservas-de-prueba.db"

    conexion = almacen.conectar()
    almacen.guardar(conexion, bloque=2)
    conexion.close()

    yield almacen.RUTA_BASE

    almacen.RUTA_BASE.unlink(missing_ok=True)
    assert not almacen.RUTA_BASE.exists(), "la base de datos de prueba no se eliminó"
    almacen.RUTA_BASE = ruta_real
