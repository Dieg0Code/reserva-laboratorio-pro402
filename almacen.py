import sqlite3
from pathlib import Path

RUTA_BASE = Path("reservas.db")

ESQUEMA = """
CREATE TABLE IF NOT EXISTS reservas (
    bloque INTEGER NOT NULL,
    rut TEXT,
    nombre TEXT,
    correo_electronico TEXT
);
CREATE TABLE IF NOT EXISTS eventos (
    momento TEXT NOT NULL,
    accion TEXT NOT NULL,
    rut TEXT
)
"""


def conectar() -> sqlite3.Connection:
    conexion = sqlite3.connect(RUTA_BASE)
    conexion.executescript(ESQUEMA)
    return conexion


def guardar(conexion: sqlite3.Connection, **campos: object) -> None:
    columnas = ", ".join(campos)
    marcas = ", ".join("?" for _ in campos)
    conexion.execute(
        f"INSERT INTO reservas ({columnas}) VALUES ({marcas})", tuple(campos.values())
    )
    conexion.commit()


def registrar_evento(conexion: sqlite3.Connection, accion: str, rut: str) -> None:
    conexion.execute(
        "INSERT INTO eventos (momento, accion, rut) VALUES (datetime('now'), ?, ?)",
        (accion, rut),
    )
    conexion.commit()


def bloque_tomado(conexion: sqlite3.Connection, bloque: int) -> bool:
    fila = conexion.execute(
        "SELECT COUNT(*) FROM reservas WHERE bloque = ?", (bloque,)
    ).fetchone()
    return fila[0] > 0


def reservas_de(conexion: sqlite3.Connection, rut: str) -> int:
    fila = conexion.execute(
        "SELECT COUNT(*) FROM reservas WHERE rut = ?", (rut,)
    ).fetchone()
    return fila[0]


def suprimir_datos_de(conexion: sqlite3.Connection, rut: str) -> None:
    conexion.execute("DELETE FROM reservas WHERE rut = ?", (rut,))
    conexion.execute("UPDATE eventos SET rut = NULL WHERE rut = ?", (rut,))
    conexion.commit()


def rastro_de(conexion: sqlite3.Connection, rut: str) -> dict[str, int]:
    """Cuenta en cuantas filas de cada tabla aparece ese RUT."""
    rastro = {}
    tablas = conexion.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()
    for (tabla,) in tablas:
        fila = conexion.execute(
            f"SELECT COUNT(*) FROM {tabla} WHERE rut = ?", (rut,)
        ).fetchone()
        rastro[tabla] = fila[0]
    return rastro
