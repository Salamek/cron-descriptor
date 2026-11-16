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

from dataclasses import dataclass

from .CasingTypeEnum import CasingTypeEnum


@dataclass
class Options:
    """
    Options for parsing and describing a Cron Expression
    """

    locale_code: str | None
    casing_type: CasingTypeEnum
    verbose: bool
    day_of_week_start_index_zero: bool
    use_24hour_time_format: bool | None
    locale_location: str | None
    six_field_expression_has_seconds: bool | None

    def __init__(self,
                 casing_type: CasingTypeEnum = CasingTypeEnum.Sentence,
                 *,
                 verbose: bool = False,
                 day_of_week_start_index_zero: bool = True,
                 use_24hour_time_format: bool | None = None,
                 locale_code: str | None = None,
                 locale_location: str | None = None,
                 six_field_expression_has_seconds: bool | None = None,
                 ) -> None:
        self.casing_type = casing_type
        self.verbose = verbose
        self.day_of_week_start_index_zero = day_of_week_start_index_zero
        self.locale_location = locale_location
        self.six_field_expression_has_seconds = six_field_expression_has_seconds
        self.locale_code = locale_code
        self.use_24hour_time_format = use_24hour_time_format
