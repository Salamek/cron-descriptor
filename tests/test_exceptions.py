# The MIT License (MIT)
#
# Copyright (c) 2016 Adam Schubert
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest

from cron_descriptor import DescriptionTypeEnum, ExpressionDescriptor, FormatError, MissingFieldError, Options

"""
Tests that Exceptions are/not properly raised
"""

def test_empty_cron_expression_exception(options: Options) -> None:
    with pytest.raises(MissingFieldError):
        ExpressionDescriptor("", options)

def test_invalid_cron_expression_exception(options: Options) -> None:
    with pytest.raises(FormatError):
        ExpressionDescriptor("INVALID", options)

def test_invalid_syntax_exception(options: Options) -> None:
    ceh = ExpressionDescriptor("* $ * * *", options)
    with pytest.raises(FormatError):
        ceh.get_description(DescriptionTypeEnum.FULL)


def test_invalid_syntax_exception_message(options: Options) -> None:
    ceh = ExpressionDescriptor("* $ * * *", options)
    with pytest.raises(FormatError, match=r"^An error occurred when generating the expression description"):
        ceh.get_description(DescriptionTypeEnum.FULL)

@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("locale_code", "message"),
    [
        ("cs_CZ", "Nastala chyba při generování popisu výrazu"),
        ("es_ES", "Ocurrió un error mientras se generaba la descripción de la expresión"),
        ("th_TH", "เกิดข้อผิดพลาดเมื่อสร้างคําอธิบายนิพจน์ ตรวจสอบไวยากรณ์นิพจน์ cron"),
    ],
)
def test_invalid_syntax_exception_message_translated(locale_code: str, message: str) -> None:
    ceh = ExpressionDescriptor("* $ * * *", Options(locale_code=locale_code))
    with pytest.raises(FormatError, match=f"^{message}"):
        ceh.get_description(DescriptionTypeEnum.FULL)

def test_day_of_week_zero_with_start_index_zero_false_exception(options: Options) -> None:
    options.day_of_week_start_index_zero = False
    with pytest.raises(FormatError):
        ExpressionDescriptor("* * * * 0", options).get_description(DescriptionTypeEnum.FULL)

def test_day_of_week_out_of_range_with_start_index_zero_false_exception(options: Options) -> None:
    options.day_of_week_start_index_zero = False
    with pytest.raises(FormatError):
        ExpressionDescriptor("* * * * 8", options).get_description(DescriptionTypeEnum.FULL)


@pytest.mark.parametrize("one_based", [False, True])  # type: ignore[untyped-decorator]
@pytest.mark.parametrize("weekday", ["8", "10", "1,10", "1-10", "10L", "10#2", "10/2"])  # type: ignore[untyped-decorator]
def test_out_of_range_weekday_tokens(weekday: str, *, one_based: bool) -> None:
    with pytest.raises(FormatError, match=r"Day of week '(8|10)' is out of range"):
        ExpressionDescriptor(f"0 0 * * {weekday}", locale_code="en_US", day_of_week_start_index_zero=not one_based)


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("expression", "description_type", "cause"),
    [
        ("* $ * * *", DescriptionTypeEnum.HOURS, ValueError),
        ("* $ * * *", DescriptionTypeEnum.TIMEOFDAY, ValueError),
        ("* $ * * *", DescriptionTypeEnum.FULL, ValueError),
        ("0 0 * 0 *", DescriptionTypeEnum.MONTH, KeyError),
        ("0 0 * 0 *", DescriptionTypeEnum.FULL, KeyError),
        ("0 0 * * BAD", DescriptionTypeEnum.DAYOFWEEK, ValueError),
    ],
)
@pytest.mark.parametrize("locale_code", ["en_US", "cs_CZ"])  # type: ignore[untyped-decorator]
def test_description_conversion_errors(expression: str, description_type: DescriptionTypeEnum, cause: type[Exception], locale_code: str) -> None:
    descriptor = ExpressionDescriptor(expression, locale_code=locale_code)
    message = "An error occurred" if locale_code == "en_US" else "Nastala chyba"
    with pytest.raises(FormatError, match=f"^{message}") as error:
        descriptor.get_description(description_type)
    assert isinstance(error.value.__cause__, cause)
