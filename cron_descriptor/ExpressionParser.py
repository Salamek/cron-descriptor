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

import re

from .Exception import MissingFieldException, FormatException


class ExpressionParser(object):

    """
     Parses and validates a Cron Expression into list of fixed len()
    """

    _expression = ''
    _options = None

    _cron_days = {
        0: 'SUN',
        1: 'MON',
        2: 'TUE',
        3: 'WED',
        4: 'THU',
        5: 'FRI',
        6: 'SAT'
    }

    _cron_months = {
        1: 'JAN',
        2: 'FEB',
        3: 'MAR',
        4: 'APR',
        5: 'MAY',
        6: 'JUN',
        7: 'JUL',
        8: 'AUG',
        9: 'SEP',
        10: 'OCT',
        11: 'NOV',
        12: 'DEC'
    }

    def __init__(self, expression, options):
        """Initializes a new instance of the ExpressionParser class
        Args:
            expression: The cron expression string
            options: Parsing options

        """
        self._expression = expression
        self._options = options

    def parse(self):
        """Parses the cron expression string
        Returns:
            A 7 part string array, one part for each component of the cron expression (seconds, minutes, etc.)
        Raises:
            MissingFieldException: if _expression is empty or None
            FormatException: if _expression has wrong format
        """
        # Initialize all elements of parsed array to empty strings
        parsed = ['', '', '', '', '', '', '']

        if self._expression is None or len(self._expression) == 0:
            raise MissingFieldException("ExpressionDescriptor.expression")
        else:
            expression_parts_temp = self._expression.split()
            expression_parts_temp_length = len(expression_parts_temp)
            if expression_parts_temp_length < 5:
                raise FormatException(
                    "Error: Expression only has {0} parts.  At least 5 part are required.".format(
                        expression_parts_temp_length))
            elif expression_parts_temp_length == 5:
                # 5 part cron so shift array past seconds element
                for i, expression_part_temp in enumerate(expression_parts_temp):
                    parsed[i + 1] = expression_part_temp
            elif expression_parts_temp_length == 6:
                # If last element ends with 4 digits, a year element has been
                # supplied and no seconds element
                year_regex = re.compile(r"\d{4}$")
                if year_regex.search(expression_parts_temp[5]) is not None:
                    for i, expression_part_temp in enumerate(expression_parts_temp):
                        parsed[i + 1] = expression_part_temp
                else:
                    for i, expression_part_temp in enumerate(expression_parts_temp):
                        parsed[i] = expression_part_temp
            elif expression_parts_temp_length == 7:
                parsed = expression_parts_temp
            else:
                raise FormatException(
                    "Error: Expression has too many parts ({0}).  Expression must not have more than 7 parts.".format(
                        expression_parts_temp_length))
        self.normalize_expression(parsed)

        return parsed

    def normalize_expression(self, expression_parts):
        """Converts cron expression components into consistent, predictable formats.
        Args:
            expression_parts: A 7 part string array, one part for each component of the cron expression
        Returns:
            None
        """
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

        if expression_parts[6].startswith("1/"):
            expression_parts[6] = expression_parts[6].replace("1/", "*/")

        # handle DayOfWeekStartIndexZero option where SUN=1 rather than SUN=0
        if self._options.day_of_week_start_index_zero is False:
            expression_parts[5] = self.decrease_days_of_week(expression_parts[5])

        if expression_parts[3] == "?":
            expression_parts[3] = "*"

        # convert SUN-SAT format to 0-6 format
        for day_number in self._cron_days:
            expression_parts[5] = expression_parts[5].upper().replace(self._cron_days[day_number], str(day_number))

        # convert JAN-DEC format to 1-12 format
        for month_number in self._cron_months:
            expression_parts[4] = expression_parts[4].upper().replace(
                self._cron_months[month_number], str(month_number))

        # convert 0 second to (empty)
        if expression_parts[0] == "0":
            expression_parts[0] = ''

        # Loop through all parts and apply global normalization
        length = len(expression_parts)
        for i in range(length):

            # convert all '*/1' to '*'
            if expression_parts[i] == "*/1":
                expression_parts[i] = "*"

            """
            Convert Month,DOW,Year step values with a starting value (i.e. not '*') to between expressions.
            This allows us to reuse the between expression handling for step values.

            For Example:
            - month part '3/2' will be converted to '3-12/2' (every 2 months between March and December)
            - DOW part '3/2' will be converted to '3-6/2' (every 2 days between Tuesday and Saturday)
            """

            if "/" in expression_parts[i] and any(exp in expression_parts[i] for exp in ['*', '-', ',']) is False:
                choices = {
                    4: "12",
                    5: "6",
                    6: "9999"
                }

                step_range_through = choices.get(i)

                if step_range_through is not None:
                    parts = expression_parts[i].split('/')
                    expression_parts[i] = "{0}-{1}/{2}".format(parts[0], step_range_through, parts[1])

    def decrease_days_of_week(self, day_of_week_expression_part):
        dow_chars = list(day_of_week_expression_part)
        for i, dow_char in enumerate(dow_chars):
            if i == 0 or dow_chars[i - 1] != '#' and dow_chars[i - 1] != '/':
                try:
                    char_numeric = int(dow_char)
                    dow_chars[i] = str(char_numeric - 1)[0]
                except ValueError:
                    pass
        return ''.join(dow_chars)
