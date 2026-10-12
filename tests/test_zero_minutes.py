import pytest

from cron_descriptor import CasingTypeEnum, DescriptionTypeEnum, ExpressionDescriptor, Options, get_description


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("expression", "expected"),
    [
        ("0 0-13 * * *", "At 0 minutes past the hour, between 12:00 AM and 01:59 PM"),
        ("0 0 0-13 * * *", "At 0 minutes past the hour, between 12:00 AM and 01:59 PM"),
        ("0 0-13 * * * 2026", "At 0 minutes past the hour, between 12:00 AM and 01:59 PM, only in 2026"),
        ("0 0 0-13 * * * 2026", "At 0 minutes past the hour, between 12:00 AM and 01:59 PM, only in 2026"),
        ("0 0-23 * * *", "At 0 minutes past the hour, between 12:00 AM and 11:59 PM"),
        ("0 13-23 * * *", "At 0 minutes past the hour, between 01:00 PM and 11:59 PM"),
    ],
)
def test_zero_minutes_with_hour_ranges(expression: str, expected: str, options: Options) -> None:
    assert get_description(expression, options) == expected


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("expression", "expected"),
    [
        ("0 * * * *", "Every hour"),
        ("0 */2 * * *", "Every 2 hours"),
        ("0 0-13/2 * * *", "Every 2 hours, between 12:00 AM and 01:59 PM"),
        ("0 0,6-13 * * *", "At 12:00 AM and 06:00 AM through 01:59 PM"),
        ("0 0-3,6-13 * * *", "At 12:00 AM through 03:59 AM and 06:00 AM through 01:59 PM"),
        ("0 0,6-13/2 * * *", "At 12:00 AM and every 2 hours, 06:00 AM through 01:59 PM"),
        ("0 6 * * *", "At 06:00 AM"),
        ("0 6,14 * * *", "At 06:00 AM and 02:00 PM"),
        ("30 0-13 * * *", "At 30 minutes past the hour, between 12:00 AM and 01:59 PM"),
        ("* 0-13 * * *", "Every minute, between 12:00 AM and 01:59 PM"),
        ("*/5 0-13 * * *", "Every 5 minutes, between 12:00 AM and 01:59 PM"),
        ("5 0 0-13 * * *", "At 5 seconds past the minute, at 0 minutes past the hour, between 12:00 AM and 01:59 PM"),
        ("* 0 0-13 * * *", "Every second, at 0 minutes past the hour, between 12:00 AM and 01:59 PM"),
        ("*/10 0 0-13 * * *", "Every 10 seconds, at 0 minutes past the hour, between 12:00 AM and 01:59 PM"),
    ],
)
def test_other_time_descriptions(expression: str, expected: str, options: Options) -> None:
    assert get_description(expression, options) == expected


def test_zero_minutes_with_hour_range_24_hour_format(options: Options) -> None:
    options.use_24hour_time_format = True
    assert get_description("0 0-13 * * *", options) == "At 0 minutes past the hour, between 00:00 and 13:59"


def test_zero_minutes_with_hour_range_verbose(options: Options) -> None:
    options.verbose = True
    assert get_description("0 0-13 * * *", options) == "At 0 minutes past the hour, between 12:00 AM and 01:59 PM, every day"


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("casing", "expected"),
    [
        (CasingTypeEnum.Title, "At 0 Minutes Past The Hour, Between 12:00 Am And 01:59 Pm"),
        (CasingTypeEnum.LowerCase, "at 0 minutes past the hour, between 12:00 am and 01:59 pm"),
    ],
)
def test_zero_minutes_with_hour_range_casing(casing: CasingTypeEnum, expected: str, options: Options) -> None:
    options.casing_type = casing
    assert get_description("0 0-13 * * *", options) == expected


def test_zero_minutes_with_hour_range_locale() -> None:
    options = Options(locale_code="de_DE")
    assert get_description("0 0-13 * * *", options) == "Bei Minute 0, zwischen 00:00 und 13:59"


def test_zero_minutes_with_hour_range_time_description(options: Options) -> None:
    descriptor = ExpressionDescriptor("0 0-13 * * *", options)
    assert descriptor.get_description(DescriptionTypeEnum.TIMEOFDAY) == "at 0 minutes past the hour, between 12:00 AM and 01:59 PM"
