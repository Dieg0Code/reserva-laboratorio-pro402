import sqlite3
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api import app

PERSONAS = 20


def reservar_bloque_4(i: int) -> int:
    solicitud = {
        "nombre": f"Persona {i}",
        "rut": f"{10_000_000 + i}-{i % 10}",
        "correo_electronico": f"persona{i}@ejemplo.cl",
        "bloque": 4,
        "personas": 5,
    }
    return TestClient(app).post("/reservas", json=solicitud).status_code


@pytest.mark.requisito("RF-02")
def test_reservas_simultaneas_del_mismo_bloque_aceptan_una_sola(
    base_de_datos_de_prueba: Path,
) -> None:
    with ThreadPoolExecutor(max_workers=PERSONAS) as grupo:
        codigos = list(grupo.map(reservar_bloque_4, range(PERSONAS)))

    with closing(sqlite3.connect(base_de_datos_de_prueba)) as conexion:
        guardadas = conexion.execute(
            "SELECT COUNT(*) FROM reservas WHERE bloque = 4"
        ).fetchone()[0]

    assert codigos.count(201) == 1
    assert guardadas == 1
