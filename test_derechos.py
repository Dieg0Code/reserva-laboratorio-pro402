from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import almacen
from api import app

cliente = TestClient(app)

RUT = "11.111.111-1"
SOLICITUD = {
    "nombre": "Ana Rivas",
    "rut": RUT,
    "correo_electronico": "ana.rivas@ejemplo.cl",
    "bloque": 4,
    "personas": 12,
}


@pytest.mark.requisito("RF-07")
def test_supresion_elimina_las_reservas(base_de_datos_de_prueba: Path) -> None:
    cliente.post("/reservas", json=SOLICITUD)

    cliente.delete(f"/titulares/{RUT}")

    conexion = almacen.conectar()
    assert almacen.reservas_de(conexion, RUT) == 0
    conexion.close()


@pytest.mark.requisito("RF-07")
def test_supresion_no_deja_rastro_del_titular(base_de_datos_de_prueba: Path) -> None:
    cliente.post("/reservas", json=SOLICITUD)

    cliente.delete(f"/titulares/{RUT}")

    conexion = almacen.conectar()
    rastro = almacen.rastro_de(conexion, RUT)
    conexion.close()
    assert rastro == {"reservas": 0, "eventos": 0}
