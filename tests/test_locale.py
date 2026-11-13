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
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from cron_descriptor import ExpressionDescriptor, Options


def describe_in_c_locale(expression: str, locale_code: str, *, without_babel: bool = False) -> str:
    # A fresh interpreter starts with LC_TIME=C; never change pytest's process locale.
    script = """
import locale
import sys

assert locale.setlocale(locale.LC_TIME) == "C"
if sys.argv[3] == "True":
    sys.modules["babel"] = None

from cron_descriptor import ExpressionDescriptor

print(ExpressionDescriptor(
    sys.argv[1], locale_code=sys.argv[2], use_24hour_time_format=True,
).get_description())
"""
    result = subprocess.run(  # noqa: S603 - fixed script executed by the current Python interpreter
        [sys.executable, "-c", script, expression, locale_code, str(without_babel)],
        cwd=Path(__file__).resolve().parents[1],
        env={**os.environ, "LC_ALL": "C", "PYTHONIOENCODING": "utf-8"},
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout.strip()


def test_calendar_names_use_explicit_locale() -> None:
    pytest.importorskip("babel")
    expression = "0 0 * 1 1"
    english = describe_in_c_locale(expression, "en_US")
    german = describe_in_c_locale(expression, "de_DE")
    assert german
    for name in ("Monday", "January"):
        assert name in english
        assert name not in german


def test_description_generation_without_babel() -> None:
    assert describe_in_c_locale("0 0 * 1 1", "de_DE", without_babel=True)


@pytest.mark.parametrize("locale_code", ["xx_XX", "invalid-locale"])  # type: ignore[untyped-decorator]
def test_description_generation_with_locale_unknown_to_babel(locale_code: str) -> None:
    pytest.importorskip("babel")
    assert describe_in_c_locale("0 0 * 1 1", locale_code)


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
