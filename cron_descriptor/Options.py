# Copyright (C) 2016 Adam Schubert <adam.schubert@sg1-game.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import locale

from .CasingTypeEnum import CasingTypeEnum
"""
Options for parsing and describing a Cron Expression
"""


class Options(object):

    def __init__(self):
        self.ThrowExceptionOnParseError = True
        self.CasingType = CasingTypeEnum.Sentence
        self.Verbose = False
        self.DayOfWeekStartIndexZero = True
        self.Use24HourTimeFormat = False

        code, encoding = locale.getlocale()
        self.Use24HourTimeFormat = code in [
            "ru_RU", "uk_UA", "de_DE", "it_IT", "tr_TR", "cs_CZ"]
