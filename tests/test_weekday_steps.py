import pytest

from cron_descriptor import ExpressionDescriptor


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("weekday", "one_based", "expected"),
    [
        ("1/6", False, "At 12:00 AM, every 6 days of the week, Monday through Sunday"),
        ("1/7", False, "At 12:00 AM, only on Monday"),
        ("MON/6", False, "At 12:00 AM, every 6 days of the week, Monday through Sunday"),
        ("MON/6", True, "At 12:00 AM, only on Monday"),
        ("2/6", True, "At 12:00 AM, only on Monday"),
        ("FRI/2", False, "At 12:00 AM, every 2 days of the week, Friday through Sunday"),
        ("FRI/2", True, "At 12:00 AM, only on Friday"),
        ("5/2", False, "At 12:00 AM, every 2 days of the week, Friday through Sunday"),
        ("6/2", True, "At 12:00 AM, only on Friday"),
        ("7/2", False, "At 12:00 AM, only on Sunday"),
        ("SUN/2", False, "At 12:00 AM, every 2 days of the week, Sunday through Saturday"),
        ("WED-FRI/3", False, "At 12:00 AM, only on Wednesday"),
        ("TUE,FRI/4", False, "At 12:00 AM, only on Tuesday and Friday"),
        ("TUE,FRI/4", True, "At 12:00 AM, only on Tuesday and Friday"),
        ("3-6/3", False, "At 12:00 AM, every 3 days of the week, Wednesday through Saturday"),
        ("1-7/7", False, "At 12:00 AM, only on Monday"),
        ("0-7/2", False, "At 12:00 AM, every 2 days of the week, Sunday through Saturday"),
        ("0-7/7", False, "At 12:00 AM, only on Sunday"),
        (
            "1/2,5", False,
            "At 12:00 AM, only on every 2 days of the week, Monday through Sunday and Friday",
        ),
        (
            "5,1/2", False,
            "At 12:00 AM, only on Friday and every 2 days of the week, Monday through Sunday",
        ),
        ("1/2,5", True, "At 12:00 AM, only on every 2 days of the week and Thursday"),
        (
            "5,1/2", True,
            "At 12:00 AM, only on Thursday and every 2 days of the week, Sunday through Saturday",
        ),
    ],
)
def test_weekday_steps(weekday: str, expected: str, *, one_based: bool) -> None:
    assert str(ExpressionDescriptor(
        f"0 0 * * {weekday}", locale_code="en_US", day_of_week_start_index_zero=not one_based,
    )) == expected
