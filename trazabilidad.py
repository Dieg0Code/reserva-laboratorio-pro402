"""Genera la matriz de trazabilidad leyendo los marcadores de la suite."""

import re
from pathlib import Path

import pytest

REQUISITOS = Path("REQUISITOS.md")


class Recolector:
    """Se entera de cada prueba que pytest recolecta, sin ejecutarla."""

    def __init__(self) -> None:
        self.pruebas: dict[str, list[str]] = {}

    def pytest_collection_modifyitems(self, items: list[pytest.Item]) -> None:
        for item in items:
            marcas = [m.args[0] for m in item.iter_markers(name="requisito")]
            self.pruebas[item.nodeid] = marcas


def requisitos_declarados() -> list[str]:
    texto = REQUISITOS.read_text(encoding="utf-8")
    return re.findall(r"RF-\d+", texto)


def main() -> None:
    recolector = Recolector()
    pytest.main(["--collect-only", "-p", "no:terminal"], plugins=[recolector])

    declarados = requisitos_declarados()
    cobertura = {rid: [] for rid in declarados}
    huerfanas = []

    for nodeid, marcas in recolector.pruebas.items():
        if not marcas:
            huerfanas.append(nodeid)
        for rid in marcas:
            cobertura.setdefault(rid, []).append(nodeid)

    print("MATRIZ DE TRAZABILIDAD")
    print(f"{'requisito':<12}{'pruebas':>8}   estado")
    for rid in declarados:
        n = len(cobertura[rid])
        estado = "cubierto" if n else "SIN PRUEBA"
        print(f"{rid:<12}{n:>8}   {estado}")

    sin_prueba = [rid for rid in declarados if not cobertura[rid]]
    print(f"\nRequisitos sin prueba: {len(sin_prueba)}")
    for rid in sin_prueba:
        print(f"  {rid}")

    print(f"\nPruebas sin requisito: {len(huerfanas)}")
    for nodeid in huerfanas:
        print(f"  {nodeid}")


if __name__ == "__main__":
    main()
