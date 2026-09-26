from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import almacen
from reservas import comprobante, puede_reservar
from sala import cabe_en_sala

CAPACIDAD_SALA = 30

app = FastAPI()


class SolicitudReserva(BaseModel):
    nombre: str
    rut: str
    correo_electronico: str
    bloque: int
    personas: int


@app.post("/reservas", status_code=201)
def crear_reserva(solicitud: SolicitudReserva) -> dict:
    conexion = almacen.conectar()
    try:
        conexion.execute("BEGIN IMMEDIATE")
        tomado = almacen.bloque_tomado(conexion, solicitud.bloque)
        de_la_semana = almacen.reservas_de(conexion, solicitud.rut)
        if not cabe_en_sala(solicitud.personas, CAPACIDAD_SALA):
            raise HTTPException(status_code=409, detail="La sala no tiene ese cupo")
        if not puede_reservar(de_la_semana, solicitud.bloque, tomado):
            raise HTTPException(status_code=409, detail="La reserva no esta permitida")
        almacen.guardar(
            conexion,
            bloque=solicitud.bloque,
            rut=solicitud.rut,
            nombre=solicitud.nombre,
            correo_electronico=solicitud.correo_electronico,
        )
        almacen.registrar_evento(conexion, "reserva creada", solicitud.rut)
    finally:
        conexion.close()
    return {
        "comprobante": comprobante(
            solicitud.nombre, solicitud.rut, solicitud.correo_electronico, solicitud.bloque
        )
    }


@app.delete("/titulares/{rut}", status_code=200)
def suprimir_titular(rut: str) -> dict:
    conexion = almacen.conectar()
    try:
        almacen.suprimir_datos_de(conexion, rut)
    finally:
        conexion.close()
    return {"suprimido": rut}


INTERFAZ = Path(__file__).parent / "interfaz"
app.mount("/interfaz", StaticFiles(directory=INTERFAZ), name="interfaz")


@app.get("/")
def pagina() -> FileResponse:
    return FileResponse(INTERFAZ / "index.html")


@app.get("/bloques")
def bloques() -> dict:
    conexion = almacen.conectar()
    try:
        tomados = [b for b in range(1, 9) if almacen.bloque_tomado(conexion, b)]
    finally:
        conexion.close()
    return {"tomados": tomados}
