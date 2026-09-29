import subprocess
import sys

import pytest

from cron_descriptor import FormatError
from cron_descriptor.ExpressionValidator import ExpressionValidator

"""
Tests validator
"""

valid = [
    "57,59 * * 1 * 1",
    "1,2,3-15 * * 1 * 1",
    "1-2,2,3-15 * * 1 * 1",
    "* 1,59 * 1 * 1",
    "* 1,2,3-15 * 1 * 1",
    "* 1-2,2,3-15 * 1 * 1",
    "* * 1 ? * *",
    "* 1-12 ? * *",
    "* 1/12 ? * *",
    "* 1-5/12 ? * *",
    "* 1,23 ? * *",
    "* 1,2,7-23 ? * *",
    "* 1-2,2,7-23 ? * *",
    "* * ? * *",
    "* * 1 * *",
    "* * 31 * *",
    "* * 1-2/31 * *",
    "* * 1,20 * *",
    "* * LW * *",
    "* * 1W * *",
    "* * 31W * *",
    "* * ? 1 *",
    "* * ? 12 *",
    "* * ? JAN *",
    "* * ? 1-12 *",
    "* * ? JAN-DEC *",
    "* * ? 1/12 *",
    "* * ? 1-5/12 *",
    "* * ? 1,2,3 *",
    "* * ? 1,Feb,3 *",
    "* * ? 1,5,6-12 *",
    "* * ? 1-2,5,6-12 *",
    "* * ? JAN-FEB,5,6-12 *",
    "* * ? * 0",
    "* * ? * 6",
    "* * ? * SUN",
    "* * ? * 0/6",
    "* * ? * 0-1/6",
    "* * ? * 0-1",
    "* * ? * MON-wed",
    "* * ? * MON-wed,sun,4",
    "* * ? * MON,3",
    "* * ? * 2L",
    "* * ? * 6L",
    "* * ? * 0#3",
    "* * ? * * 1970",
    "* * ? * * 2099",
    "* * ? * * 1970-2099",
    "* * ? * * 1970/129",
    "* * * ? * * 1970-2001/129",
    "* * * ? * * 1970,1971,2099",
    "* * * ? * * 1970-1971,1972,2000-2002",
    "* * * * * 2013",
]

invalid = [

    "0-59 * * 1 * 1",     # invalid DOW range
    "1-2/59 * * 1 * 1",   # invalid step
    "* * /31 * *",        # stray slash
    "* * l-31 * *",       # lowercase 'l'
    "* * lw * *",         # lowercase 'lw'
    "* * ? * /6",         # stray slash
    "* * ? * * /129",     # stray slash
    "* /12 ? * *",        # stray slash
    "* * W21 * * 0/2",    # W before number
]

def test_validator_expression() -> None:
    for expression in valid:
        ExpressionValidator().validate(expression)


@pytest.mark.parametrize(("field", "token"), [(3, "1"), (3, "JAN"), (4, "1"), (4, "MON")])  # type: ignore[untyped-decorator]
def test_malformed_lists_finish_validation(field: int, token: str) -> None:
    code = """
import sys
from cron_descriptor import FormatError
from cron_descriptor.ExpressionValidator import ExpressionValidator

fields = ["*", "*", "*", "*", "*"]
fields[int(sys.argv[1])] = ",".join([sys.argv[2]] * 1000) + "X"
try:
    ExpressionValidator().validate(" ".join(fields))
except FormatError:
    pass
else:
    raise AssertionError("Malformed list was accepted")
"""
    subprocess.run(  # noqa: S603
        [sys.executable, "-c", code, str(field), token],
        check=True,
        capture_output=True,
        timeout=5,
    )


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "expression",
    [
        "* * * JAN,2,MAR-MAY,6-12 *",
        "* * * 1-2,mar,4,may-jun *",
        "* * * * SUN,1,TUE-THU,5-6",
        "* * * * 0-1,tue,3,thu-sat",
        "* * * " + ",".join(["JAN"] * 12) + " *",
        "* * * * " + ",".join(["MON"] * 7),
    ],
)
def test_valid_month_and_weekday_lists(expression: str) -> None:
    ExpressionValidator().validate(expression)


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "expression",
    [
        "* * * JAN,,FEB *",
        "* * * JAN, *",
        "* * * ,JAN *",
        "* * * JAN,2-3X *",
        "* * * * MON,,TUE",
        "* * * * MON,",
        "* * * * ,MON",
        "* * * * MON,2-3X",
        "* * * " + ",".join(["JAN"] * 13) + " *",
        "* * * * " + ",".join(["MON"] * 8),
    ],
)
def test_invalid_month_and_weekday_lists(expression: str) -> None:
    with pytest.raises(FormatError):
        ExpressionValidator().validate(expression)
