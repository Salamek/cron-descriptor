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


def describe_in_c_locale(expression: str, locale_code: str) -> str:
    # A fresh interpreter starts with LC_TIME=C; never change pytest's process locale.
    script = """
import locale
import sys

assert locale.setlocale(locale.LC_TIME) == "C"
from cron_descriptor import ExpressionDescriptor

print(ExpressionDescriptor(
    sys.argv[1], locale_code=sys.argv[2], use_24hour_time_format=True,
).get_description())
"""
    result = subprocess.run(  # noqa: S603 - fixed script executed by the current Python interpreter
        [sys.executable, "-c", script, expression, locale_code],
        cwd=Path(__file__).resolve().parents[1],
        env={**os.environ, "LC_ALL": "C", "PYTHONIOENCODING": "utf-8"},
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return result.stdout.strip()


def test_calendar_names_use_explicit_locale() -> None:
    expression = "0 0 * 1 1"
    assert describe_in_c_locale(expression, "en_US") == "At 00:00, only on Monday, only in January"
    assert describe_in_c_locale(expression, "de_DE") == "Um 00:00, nur am Montag, nur im Januar"
    assert describe_in_c_locale("0 10 * * 1", "es_ES") == "A las 10:00, sólo el lunes"


@pytest.mark.parametrize("locale_code", ["xx_XX", "invalid-locale", "de_AT"])  # type: ignore[untyped-decorator]
def test_description_generation_with_locale_unknown_to_babel(locale_code: str) -> None:
    assert describe_in_c_locale("0 0 * 1 1", locale_code) == "At 00:00, only on Monday, only in January"


def test_locale_de() -> None:
    options = Options(locale_code="de_DE")
    assert ExpressionDescriptor("* * * * *", options).get_description() == "Jede Minute"

@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("expression", "expected"),
    [
        ("* 0-7,19-23 * * *", "Ogni minuto, dalle 00:00 alle 07:59 e dalle 19:00 alle 23:59"),
        ("0 8,12-14 * * *", "Alle 08:00 e dalle 12:00 alle 14:59"),
        ("0 12-14,8 * * *", "Dalle 12:00 alle 14:59 e alle 08:00"),
        ("0 6-7,12,18 * * *", "Dalle 06:00 alle 07:59, alle 12:00, e alle 18:00"),
        ("0 6,12-14,18 * * *", "Alle 06:00, dalle 12:00 alle 14:59, e alle 18:00"),
        ("* 12-14,8 * * *", "Ogni minuto, dalle 12:00 alle 14:59 e alle 08:00"),
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


def test_custom_catalog_with_unknown_calendar_locale(tmp_path: Path) -> None:
    source = Path(__file__).resolve().parents[1] / "cron_descriptor" / "locale" / "de_DE.mo"
    (tmp_path / "xx_XX.mo").write_bytes(source.read_bytes())
    descriptor = ExpressionDescriptor(
        "0 0 * 1 1", locale_code="xx_XX", locale_location=str(tmp_path), use_24hour_time_format=True,
    )
    assert str(descriptor) == "Um 00:00, nur am Monday, nur im January"


def test_missing_translation_keeps_optional_key_fallback() -> None:
    descriptor = ExpressionDescriptor("* * * * *", locale_code="en_US")
    assert descriptor.translate("at {0} [hourRanges]") == ""
    assert descriptor.translate("at {0}") == "at {0}"
