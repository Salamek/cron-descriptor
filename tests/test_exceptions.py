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
        ("th_TH", "เกิดข้อผิดพลาดเมื่อสร้างคําอธิบายนิพจน์ ตรวจสอบไวยากรณ์นิพจน์ cron"),
    ],
)
def test_invalid_syntax_exception_message_translated(locale_code: str, message: str) -> None:
    ceh = ExpressionDescriptor("* $ * * *", Options(locale_code=locale_code))
    with pytest.raises(FormatError, match=f"^{message}"):
        ceh.get_description(DescriptionTypeEnum.FULL)
