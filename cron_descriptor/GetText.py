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
from __future__ import annotations

import locale
import logging
from pathlib import Path

from babel import Locale, UnknownLocaleError
from babel.support import NullTranslations, Translations

logger = logging.getLogger(__name__)


class FallBackNull(NullTranslations):
    def gettext(self, _message: str)  -> str:
        # If we get here, that means that original translator failed, we will return empty string
        return ""


class GetText:
    """Handles language translations
    """

    def __init__(self, locale_code: str, locale_location: str | None = None) -> None:
        """Initialize GetText
        :param locale_code selected locale
        """
        try:
            self.trans = self.load_locale(locale_code, locale_location)
        except OSError:
            logger.debug("Failed to find locale %s", locale_code)
            logger.debug("Attempting to load en_US as fallback")
            self.trans = self.load_locale("en_US")
            locale_code = "en_US"

        self.locale = self.parse_locale(locale_code)

        # Add fallback that does not return original string, this is hack to add
        # support for _("") or _("")
        self.trans.add_fallback(FallBackNull())

    def load_locale(self, locale_code: str, locale_location: str | None=None) -> Translations:
        dir_path = Path(locale_location) if locale_location else Path(__file__).resolve().parent.joinpath("locale")
        filename = dir_path.joinpath(f"{locale_code}.mo")
        with filename.open("rb") as f:
            trans = Translations(f)
        logger.debug("%s Loaded", filename)
        return trans

    @staticmethod
    def parse_locale(locale_code: str) -> Locale:
        """Custom catalogs can use locale identifiers unknown to CLDR."""
        try:
            return Locale.parse(locale_code)
        except (UnknownLocaleError, ValueError):
            return Locale("en", "US")

    @staticmethod
    def weekday_name(day_number: int, babel_locale: Locale | None = None) -> str:
        """Return a weekday name using cron's Sunday=0 numbering."""
        try:
            weekday = (6, 0, 1, 2, 3, 4, 5)[day_number]
        except IndexError as e:
            msg = f"Day {day_number} is out of range!"
            raise IndexError(msg) from e
        if babel_locale is None:
            babel_locale = GetText.parse_locale(locale.getlocale()[0] or "en_US")
        return str(babel_locale.days["stand-alone"]["wide"][weekday])

    def day_name(self, day_number: int) -> str:
        return self.weekday_name(day_number, self.locale)

    def month_name(self, month: int) -> str:
        return str(self.locale.months["stand-alone"]["wide"][month])
