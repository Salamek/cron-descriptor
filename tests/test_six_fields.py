from __future__ import annotations

import pytest

from cron_descriptor import ExpressionDescriptor, Options, get_description


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("expression", "expected"),
    [
        ("* * * * * *", "Every minute"),
        ("*/5 * * * * *", "Every 5 minutes"),
        ("15 6 * * * *", "At 06:15 AM"),
        ("30 9 15 JAN * *", "At 09:30 AM, on day 15 of the month, only in January"),
        ("30 9 * JAN MON *", "At 09:30 AM, only on Monday, only in January"),
        ("15 6 * * * */2", "At 06:15 AM, every 2 years"),
        ("15 6 * * * 2026/2", "At 06:15 AM, every 2 years, 2026 through 9999"),
        ("15 6 * * * 2026-2030/2", "At 06:15 AM, every 2 years, 2026 through 2030"),
    ],
)
def test_six_fields_without_seconds(expression: str, expected: str) -> None:
    options = Options(locale_code="en_US", six_field_expression_has_seconds=False)
    assert get_description(expression, options) == expected


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("expression", "expected"),
    [
        ("* * * * * *", "Every second"),
        ("30 15 10 * * MON", "At 10:15:30 AM, only on Monday"),
        ("30 9 * * * 2026", "At 09:30 AM, only in 2026"),
        ("30 9 ? * MON *", "At 09:30 AM, only on Monday"),
        ("30 9 * * ? *", "At 09:30 AM"),
    ],
)
def test_six_fields_default_detection(expression: str, expected: str, options: Options) -> None:
    assert get_description(expression, options) == expected


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("expression", "expected"),
    [
        ("* * * * * *", "Every second"),
        ("30 15 10 * * MON", "At 10:15:30 AM, only on Monday"),
    ],
)
def test_six_fields_with_seconds(expression: str, expected: str) -> None:
    options = Options(locale_code="en_US", six_field_expression_has_seconds=True)
    assert get_description(expression, options) == expected


@pytest.mark.parametrize("has_seconds", [None, False, True])  # type: ignore[untyped-decorator]
@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("expression", "expected"),
    [
        ("30 9 * JAN MON", "At 09:30 AM, only on Monday, only in January"),
        ("15 30 9 * JAN MON 2026", "At 09:30:15 AM, only on Monday, only in January, only in 2026"),
    ],
)
def test_other_field_counts(expression: str, expected: str, *, has_seconds: bool | None) -> None:
    options = Options(locale_code="en_US", six_field_expression_has_seconds=has_seconds)
    assert get_description(expression, options) == expected


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("has_seconds", "expected"),
    [(None, "Every second"), (False, "Every minute"), (True, "Every second")],
)
def test_six_fields_keyword_argument(*, has_seconds: bool | None, expected: str) -> None:
    descriptor = ExpressionDescriptor(
        "* * * * * *",
        locale_code="en_US",
        six_field_expression_has_seconds=has_seconds,
    )
    assert descriptor.get_description() == expected


def test_six_fields_keyword_overrides_options() -> None:
    options = Options(locale_code="en_US", six_field_expression_has_seconds=True)
    descriptor = ExpressionDescriptor("* * * * * *", options, six_field_expression_has_seconds=False)
    assert descriptor.get_description() == "Every minute"


def test_six_fields_with_day_index_and_time_options() -> None:
    options = Options(
        locale_code="en_US",
        use_24hour_time_format=True,
        day_of_week_start_index_zero=False,
        six_field_expression_has_seconds=False,
    )
    assert get_description("30 19 * JAN 2 *", options) == "At 19:30, only on Monday, only in January"


def test_six_fields_locale() -> None:
    options = Options(locale_code="de_DE", six_field_expression_has_seconds=False)
    assert get_description("* * * * * *", options) == "Jede Minute"
