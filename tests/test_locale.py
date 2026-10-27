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

import logging
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from cron_descriptor import ExpressionDescriptor, Options


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("system_locale", "locale_code", "expected"),
    [
        ("de_DE", "en_US", "At 06:00 PM"),
        ("en_US", "de_DE", "Um 18:00"),
    ],
)
def test_locale_keyword_uses_locale_time_format(system_locale: str, locale_code: str, expected: str) -> None:
    with patch("locale.getlocale", return_value=(system_locale, "UTF-8")):
        descriptor = ExpressionDescriptor("0 18 * * *", locale_code=locale_code)
    assert descriptor.get_description() == expected


def test_locale_keyword_respects_explicit_time_format() -> None:
    with patch("locale.getlocale", return_value=("de_DE", "UTF-8")):
        descriptor = ExpressionDescriptor("0 18 * * *", locale_code="en_US", use_24hour_time_format=True)
    assert descriptor.get_description() == "At 18:00"


def test_locale_keyword_keeps_provided_options_time_format() -> None:
    options = Options(locale_code="en_US", use_24hour_time_format=False)
    descriptor = ExpressionDescriptor("0 18 * * *", options, locale_code="de_DE")
    assert descriptor.get_description() == "Um 06:00"


def test_locale_de() -> None:
    options = Options(locale_code="de_DE")
    assert ExpressionDescriptor("* * * * *", options).get_description() == "Jede Minute"

def test_locale_de_custom_location() -> None:
    logger = logging.getLogger("cron_descriptor.GetText")
    with patch.object(logger, "debug") as mock_logger:
        # Copy existing .mo file to temp directory:
        temp_dir = Path(tempfile.gettempdir())
        temp_path = temp_dir.joinpath( "de_DE.mo")

        source_path_file = Path(__file__).resolve().parent.joinpath("../cron_descriptor/locale/de_DE.mo")

        shutil.copyfile(source_path_file.absolute(), temp_path)

        options = Options(
            locale_code="de_DE",
            locale_location=str(temp_dir.absolute()),
        )

        assert ExpressionDescriptor("* * * * *", options).get_description() == "Jede Minute"
        mock_logger.assert_called_once_with("%s Loaded", temp_path)
