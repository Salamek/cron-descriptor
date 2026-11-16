from unittest.mock import patch

from cron_descriptor import CasingTypeEnum, ExpressionDescriptor, Options


def test_time_format_override_can_restore_autodetection() -> None:
    options = Options(locale_code="de_DE", use_24hour_time_format=False)
    assert str(ExpressionDescriptor("0 18 * * *", options)) == "Um 06:00"
    assert str(ExpressionDescriptor("0 18 * * *", options, use_24hour_time_format=None)) == "Um 18:00"
    assert options.use_24hour_time_format is False


def test_locale_override_can_restore_autodetection() -> None:
    options = Options(locale_code="en_US")
    with patch("locale.getlocale", return_value=("de_DE", "UTF-8")):
        assert str(ExpressionDescriptor("0 18 * * *", options)) == "At 06:00 PM"
        assert str(ExpressionDescriptor("0 18 * * *", options, locale_code=None)) == "Um 18:00"
    assert options.locale_code == "en_US"


def test_locale_location_override_can_restore_default() -> None:
    options = Options(locale_code="de_DE", locale_location="/nonexistent-cron-descriptor-locales")
    # A missing custom catalog falls back to English.
    assert str(ExpressionDescriptor("0 18 * * *", options)) == "At 18:00"
    assert str(ExpressionDescriptor("0 18 * * *", options, locale_location=None)) == "Um 18:00"


def test_six_field_override_can_restore_autodetection() -> None:
    options = Options(locale_code="en_US", six_field_expression_has_seconds=False)
    assert str(ExpressionDescriptor("0 0 12 * * *", options)) == "At 12:00 AM, on day 12 of the month"
    assert str(ExpressionDescriptor("0 0 12 * * *", options, six_field_expression_has_seconds=None)) == "At 12:00 PM"
    assert options.six_field_expression_has_seconds is False


def test_omitted_configuration_resolves_defaults() -> None:
    with patch("locale.getlocale", return_value=("en_US", "UTF-8")):
        assert str(ExpressionDescriptor("0 18 * * *")) == "At 06:00 PM"


def test_locale_keyword_controls_default_time_format() -> None:
    with patch("locale.getlocale", return_value=("en_US", "UTF-8")):
        assert str(ExpressionDescriptor("0 18 * * *", locale_code="de_DE")) == "Um 18:00"


def test_explicit_keywords_without_options_are_preserved() -> None:
    descriptor = ExpressionDescriptor(
        "* * * * 1",
        locale_code="en_US",
        verbose=True,
        casing_type=CasingTypeEnum.LowerCase,
        day_of_week_start_index_zero=False,
    )
    assert str(descriptor) == "every minute, every hour, only on sunday"


def test_false_keywords_override_true_options() -> None:
    options = Options(locale_code="en_US", verbose=True, day_of_week_start_index_zero=True, use_24hour_time_format=True)
    descriptor = ExpressionDescriptor(
        "0 18 * * 1", options, verbose=False, day_of_week_start_index_zero=False, use_24hour_time_format=False,
    )
    assert str(descriptor) == "At 06:00 PM, only on Sunday"
