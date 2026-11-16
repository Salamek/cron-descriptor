"""Multilingual description regression tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict, cast

import pytest

from cron_descriptor import ExpressionDescriptor, Options


class LocaleCase(TypedDict):
    id: str
    locale: str
    expression: str
    expected: str
    comparison: str
    options: dict[str, bool]
    normalize_apostrophe: bool


class KnownGap(TypedDict):
    reason: str
    actual: str


_FIXTURES = Path(__file__).parent / "fixtures" / "locales"
_CASES = cast("list[LocaleCase]", json.loads((_FIXTURES / "locale_cases.json").read_text(encoding="utf-8")))
_CASES += cast("list[LocaleCase]", json.loads((_FIXTURES / "additional_locale_cases.json").read_text(encoding="utf-8")))
_KNOWN_GAPS = cast("dict[str, KnownGap]", json.loads((_FIXTURES / "known_gaps.json").read_text(encoding="utf-8")))


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    "case",
    [
        pytest.param(case, id=case["id"], marks=pytest.mark.xfail(reason=_KNOWN_GAPS[case["id"]]["reason"], strict=True, raises=AssertionError))
        if case["id"] in _KNOWN_GAPS else pytest.param(case, id=case["id"])
        for case in _CASES
    ],
)
def test_locale_format(case: LocaleCase) -> None:
    settings = case["options"]
    options = Options(
        locale_code=case["locale"],
        use_24hour_time_format=settings["use_24hour_time_format"],
        day_of_week_start_index_zero=settings.get("day_of_week_start_index_zero", True),
        verbose=settings.get("verbose", False),
    )
    actual = ExpressionDescriptor(case["expression"], options).get_description()
    if case.get("normalize_apostrophe", False):
        actual = actual.replace("'", "\u02bc")
    matches = (
        case["expected"].casefold() in actual.casefold()
        if case["comparison"] == "contains_casefold" else actual == case["expected"]
    )
    gap = _KNOWN_GAPS.get(case["id"])
    if gap is not None and not matches and actual != gap["actual"]:
        # Only the documented discrepancy is expected; a different wrong result
        # is a regression, and must not be swallowed by the xfail marker.
        msg = f"Locale output regressed: {actual!r}; previous output: {gap['actual']!r}"
        raise RuntimeError(msg)
    assert matches, f"Expected {case['expected']!r}, got {actual!r}"
