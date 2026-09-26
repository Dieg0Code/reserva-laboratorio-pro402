import sqlite3
from contextlib import closing
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api import app

cliente = TestClient(app)

ANA = {
    "nombre": "Ana Rivas",
    "rut": "11.111.111-1",
    "correo_electronico": "ana.rivas@ejemplo.cl",
    "personas": 5,
}


def test_un_nombre_con_codigo_sql_se_guarda_como_texto(base_de_datos_de_prueba: Path) -> None:
    nombre = "x'); DROP TABLE reservas; --"

    respuesta = cliente.post("/reservas", json=ANA | {"nombre": nombre, "bloque": 4})

    assert respuesta.status_code == 201
    with closing(sqlite3.connect(base_de_datos_de_prueba)) as conexion:
        guardado = conexion.execute("SELECT nombre FROM reservas WHERE bloque = 4").fetchone()
    assert guardado == (nombre,)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Suplantación: la API acepta cualquier RUT sin comprobar quién lo escribe. "
        "Pendiente: decidir cómo se identifican las personas."
    ),
)
def test_otra_persona_no_puede_agotar_la_cuota_de_ana(base_de_datos_de_prueba: Path) -> None:
    otra_persona = ANA | {"nombre": "Otra persona", "correo_electronico": "otra@ejemplo.cl"}
    for bloque in (1, 3, 5):
        cliente.post("/reservas", json=otra_persona | {"bloque": bloque})

    respuesta = cliente.post("/reservas", json=ANA | {"bloque": 7})

    assert respuesta.status_code == 201
