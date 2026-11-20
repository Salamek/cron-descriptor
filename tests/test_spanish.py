"""Regression coverage for Spanish translation completeness."""

import pytest

from cron_descriptor import ExpressionDescriptor, Options


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("expression", "use_24hour_time_format", "expected"),
    [
        ("0 6 * * *", False, "A las 06:00 a. m."),
        ("0 18 * * *", False, "A las 06:00 p. m."),
        ("0 18 * * *", True, "A las 18:00"),
        ("0 0 L-5 * *", True, "A las 00:00, 5 días antes del último día del mes"),
        ("* 0-7,19-23 * * *", True, "Cada minuto, de las 00:00 a las 07:59 y de las 19:00 a las 23:59"),
        ("0 8,12-14 * * *", True, "A las 08:00 y de las 12:00 a las 14:59"),
        ("0 8-10,12 * * *", True, "De las 08:00 a las 10:59 y a las 12:00"),
        ("0-10,30 * * * *", True, "A los 0 a 10 y 30 minutos de la hora"),
        ("0-10,30 * * * * *", True, "A los 0 a 10 y 30 segundos del minuto"),
        ("* * * * MON#1", True, "Cada minuto, en el primer lunes del mes"),
        ("10-20/5 * * * * *", True, "Cada 5 segundos, en los segundos 10 al 20 de cada minuto"),
    ],
)
def test_spanish_descriptions(expression: str, expected: str, *, use_24hour_time_format: bool) -> None:
    options = Options(locale_code="es_ES", use_24hour_time_format=use_24hour_time_format)
    assert ExpressionDescriptor(expression, options).get_description() == expected
