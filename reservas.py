from datetime import datetime, timedelta

BLOQUE_MIN = 1
BLOQUE_MAX = 8
MAX_POR_SEMANA = 3
ANTICIPACION_CANCELACION = timedelta(hours=2)


def bloque_valido(bloque: int) -> bool:
    return BLOQUE_MIN <= bloque <= BLOQUE_MAX


def puede_reservar(reservas_de_la_semana: int, bloque: int, tomado: bool) -> bool:
    if not bloque_valido(bloque):
        return False
    if tomado:
        return False
    return reservas_de_la_semana < MAX_POR_SEMANA


def puede_cancelar(inicio_bloque: datetime, ahora: datetime) -> bool:
    return inicio_bloque - ahora > ANTICIPACION_CANCELACION


def comprobante(nombre: str, rut: str, correo: str, bloque: int) -> str:
    return f"{nombre} | {rut} | bloque {bloque}"
