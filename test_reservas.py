import pytest

from reservas import bloque_valido, puede_reservar


@pytest.mark.requisito("RF-01")
@pytest.mark.parametrize(
    ("bloque", "esperado"),
    [(-5, False), (4, True), (12, False)],
    ids=["antes-jornada", "dentro-jornada", "despues-jornada"],
)
def test_validez_por_particion(bloque: int, esperado: bool) -> None:
    obtenido = bloque_valido(bloque)
    assert obtenido is esperado


@pytest.mark.requisito("RF-01")
@pytest.mark.parametrize(
    ("bloque", "esperado"),
    [(0, False), (1, True), (8, True), (9, False)],
    ids=["antes", "primero", "ultimo", "despues"],
)
def test_limites_del_requisito(bloque: int, esperado: bool) -> None:
    assert bloque_valido(bloque) is esperado


@pytest.mark.parametrize(
    ("reservas", "bloque", "tomado", "esperado"),
    [
        pytest.param(1, 0, False, False, marks=pytest.mark.requisito("RF-01")),
        pytest.param(1, 4, True, False, marks=pytest.mark.requisito("RF-02")),
        pytest.param(3, 4, False, False, marks=pytest.mark.requisito("RF-03")),
        pytest.param(1, 4, False, True, marks=pytest.mark.requisito("RF-03")),
    ],
    ids=["R1-fuera-jornada", "R2-ocupado", "R3-sin-cupo", "R4-permitida"],
)
def test_reglas_de_reserva(
    reservas: int, bloque: int, tomado: bool, esperado: bool
) -> None:
    obtenido = puede_reservar(reservas, bloque, tomado)
    assert obtenido is esperado


@pytest.mark.requisito("RF-01")
def test_regla_permitida_incluye_el_bloque_8() -> None:
    assert puede_reservar(1, 8, tomado=False) is True
