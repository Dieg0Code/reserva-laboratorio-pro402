from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api import app

cliente = TestClient(app)

SOLICITUD = {
    "nombre": "Ana Rivas",
    "rut": "11.111.111-1",
    "correo_electronico": "ana.rivas@ejemplo.cl",
    "bloque": 4,
    "personas": 12,
}


@pytest.mark.requisito("RF-06")
def test_reserva_aceptada_responde_201(base_de_datos_de_prueba: Path) -> None:
    respuesta = cliente.post("/reservas", json=SOLICITUD)
    assert respuesta.status_code == 201


@pytest.mark.requisito("RF-01")
def test_bloque_fuera_de_jornada_responde_409(base_de_datos_de_prueba: Path) -> None:
    respuesta = cliente.post("/reservas", json=SOLICITUD | {"bloque": 12})
    assert respuesta.status_code == 409


@pytest.mark.requisito("RF-02")
def test_bloque_ya_tomado_responde_409(base_de_datos_de_prueba: Path) -> None:
    respuesta = cliente.post("/reservas", json=SOLICITUD | {"bloque": 2})
    assert respuesta.status_code == 409


def test_la_base_de_datos_existe_durante_la_prueba(base_de_datos_de_prueba: Path) -> None:
    assert base_de_datos_de_prueba.exists()
