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


def test_locale_de() -> None:
    options = Options(locale_code="de_DE")
    assert ExpressionDescriptor("* * * * *", options).get_description() == "Jede Minute"

@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("expression", "expected"),
    [
        ("* 0-7,19-23 * * *", "Ogni minuto, dalle 00:00 alle 07:59 e dalle 19:00 alle 23:59"),
        ("0 8,12-14 * * *", "Alle 08:00 e dalle 12:00 alle 14:59"),
        ("*/5 8,12 * * *", "Ogni 5 minuti, alle 08:00 e 12:00"),
        ("0,30 6-17 * * *", "Al 0 e 30 minuto passata l'ora, tra le 06:00 e le 17:59"),
    ],
)
def test_locale_it_hours(expression: str, expected: str) -> None:
    options = Options(locale_code="it_IT", use_24hour_time_format=True)
    assert ExpressionDescriptor(expression, options).get_description() == expected

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
