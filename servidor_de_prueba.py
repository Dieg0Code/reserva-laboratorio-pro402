"""Arranca la aplicacion para las pruebas de extremo a extremo.

Parte con una base de datos vacia, ofrece una ruta para vaciarla antes de cada prueba,
y puede agregar una demora aleatoria a cada respuesta para simular una red real.
"""

import asyncio
import os
import random
from pathlib import Path

import uvicorn
from fastapi import Request

import almacen
from api import app

almacen.RUTA_BASE = Path("reservas-e2e.db")
almacen.RUTA_BASE.unlink(missing_ok=True)

LATENCIA_MAXIMA = float(os.environ.get("LATENCIA_MAXIMA", "0"))


@app.middleware("http")
async def latencia_variable(request: Request, llamar_siguiente):
    if LATENCIA_MAXIMA:
        await asyncio.sleep(random.uniform(0, LATENCIA_MAXIMA))
    return await llamar_siguiente(request)


@app.post("/_prueba/reiniciar", status_code=204)
def reiniciar() -> None:
    conexion = almacen.conectar()
    conexion.execute("DELETE FROM reservas")
    conexion.commit()
    conexion.close()


uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
