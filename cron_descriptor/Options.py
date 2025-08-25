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

import locale

from .CasingTypeEnum import CasingTypeEnum


class Options:
    """
    Options for parsing and describing a Cron Expression
    """

    locale_code: str
    casing_type: CasingTypeEnum
    verbose: bool
    day_of_week_start_index_zero: bool
    use_24hour_time_format: bool
    locale_location: str | None

    _twelve_hour_locales = (
        "en_US",  # United States
        "en_CA",  # Canada (English)
        "fr_CA",  # Canada (French)
        "en_AU",  # Australia
        "en_NZ",  # New Zealand
        "en_IE",  # Ireland
        "en_PH",  # Philippines
        "es_MX",  # Mexico
        "en_PK",  # Pakistan
        "en_IN",  # India
        "ar_SA",  # Saudi Arabia
        "bn_BD",  # Bangladesh
        "es_HN",  # Honduras
        "es_SV",  # El Salvador
        "es_NI",  # Nicaragua
        "ar_JO",  # Jordan
        "ar_EG",  # Egypt
        "es_CO",  # Colombia
    )

    def __init__(self) -> None:
        self.casing_type = CasingTypeEnum.Sentence
        self.verbose = False
        self.day_of_week_start_index_zero = True
        self.use_24hour_time_format = False
        self.locale_location = None

        code, _encoding = locale.getlocale()
        if not code:
            msg = "Failed to retrieve locale code"
            raise ValueError(msg)
        self.locale_code = code
        self.use_24hour_time_format = code not in self._twelve_hour_locales
