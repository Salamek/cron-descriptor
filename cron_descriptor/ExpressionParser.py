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

import re

from .Tools import number_to_day, number_to_month
from .Exception import MissingFieldException, FormatException


class ExpressionParser(object):
    m_expression = ''
    m_options = None

    """
    Initializes a new instance of the ExpressionParser class
    @param: expression The cron expression string
    @param: options Parsing options
    """

    def __init__(self, expression, options):
        self.m_expression = expression
        self.m_options = options

    """
    Parses the cron expression string
    @returns: A 7 part string array, one part for each component of the cron expression (seconds, minutes, etc.)
    """

    def parse(self):
        # Initialize all elements of parsed array to empty strings
        parsed = ['', '', '', '', '', '', '']

        if self.m_expression is None or len(self.m_expression) == 0:
            raise MissingFieldException("ExpressionDescriptor.expression")
        else:
            expression_parts_temp = self.m_expression.split()
            expression_parts_temp_length = len(expression_parts_temp)
            if expression_parts_temp_length < 5:
                raise FormatException(
                    "Error: Expression only has {0} parts.  At least 5 part are required.".format(
                        expression_parts_temp_length))
            elif expression_parts_temp_length == 5:
                # 5 part cron so shift array past seconds element
                parsed[1] = expression_parts_temp[0]
                parsed[2] = expression_parts_temp[1]
                parsed[3] = expression_parts_temp[2]
                parsed[4] = expression_parts_temp[3]
                parsed[5] = expression_parts_temp[4]

            elif expression_parts_temp_length == 6:
                # If last element ends with 4 digits, a year element has been
                # supplied and no seconds element
                year_regex = re.compile("\d{4}$")
                if year_regex.search(expression_parts_temp[5]) is not None:
                    parsed[1] = expression_parts_temp[0]
                    parsed[2] = expression_parts_temp[1]
                    parsed[3] = expression_parts_temp[2]
                    parsed[4] = expression_parts_temp[3]
                    parsed[5] = expression_parts_temp[4]
                    parsed[6] = expression_parts_temp[5]
                else:
                    for i in range(0, expression_parts_temp_length):
                        parsed[i] = expression_parts_temp[i]
            elif expression_parts_temp_length == 7:
                parsed = expression_parts_temp
            else:
                raise FormatException(
                    "Error: Expression has too many parts ({0}).  Expression must not have more than 7 parts.".format(
                        expression_parts_temp_length))
        self.normalize_expression(parsed)

        return parsed

    """
    Converts cron expression components into consistent, predictable formats.
    @param: expression_parts A 7 part string array, one part for each component of the cron expression
    """

    def normalize_expression(self, expression_parts):
        # convert ? to * only for DOM and DOW
        expression_parts[3] = expression_parts[3].replace("?", "*")
        expression_parts[5] = expression_parts[5].replace("?", "*")

        # convert 0/, 1/ to */
        if expression_parts[0].startswith("0/"):
            expression_parts[0] = expression_parts[
                0].replace("0/", "*/")  # seconds

        if expression_parts[1].startswith("0/"):
            expression_parts[1] = expression_parts[
                1].replace("0/", "*/")  # minutes

        if expression_parts[2].startswith("0/"):
            expression_parts[2] = expression_parts[
                2].replace("0/", "*/")  # hours

        if expression_parts[3].startswith("1/"):
            expression_parts[3] = expression_parts[3].replace("1/", "*/")  # DOM

        if expression_parts[4].startswith("1/"):
            expression_parts[4] = expression_parts[
                4].replace("1/", "*/")  # Month

        if expression_parts[5].startswith("1/"):
            expression_parts[5] = expression_parts[5].replace("1/", "*/")  # DOW

        # convert */1 to *
        length = len(expression_parts)
        for i in range(0, length):
            if expression_parts[i] == "*/1":
                expression_parts[i] = "*"

        # handle DayOfWeekStartIndexZero option where SUN=1 rather than SUN=0
        if self.m_options.day_of_week_start_index_zero is False:
            dow_chars = list(expression_parts[5])
            for i in range(0, len(dow_chars)):
                if i == 0 or dow_chars[i - 1] != '#':
                    try:
                        char_numeric = int(dow_chars[i])
                        dow_chars[i] = str(char_numeric - 1)[0]
                    except ValueError:
                        pass
            expression_parts[5] = ''.join(dow_chars)

        # convert SUN-SAT format to 0-6 format
        for i in range(0, 6):
            expression_parts[5] = expression_parts[
                5].replace(number_to_day(i)[:3].upper(), str(i))

        # convert JAN-DEC format to 1-12 format
        for i in range(1, 13):
            expression_parts[4] = expression_parts[4].replace(
                number_to_month(i)[:3].upper(), str(i))

        # convert 0 second to (empty)
        if expression_parts[0] == "0":
            expression_parts[0] = ''
