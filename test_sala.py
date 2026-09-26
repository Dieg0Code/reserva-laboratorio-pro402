import pytest

from sala import cabe_en_sala


@pytest.mark.requisito("RF-04")
@pytest.mark.parametrize(
    ("personas", "capacidad", "esperado"),
    [(12, 30, True), (30, 30, True), (31, 30, False), (0, 30, False)],
    ids=["holgado", "justo-al-limite", "excedido", "sin-personas"],
)
def test_cupo_de_la_sala(personas: int, capacidad: int, esperado: bool) -> None:
    assert cabe_en_sala(personas, capacidad) is esperado
