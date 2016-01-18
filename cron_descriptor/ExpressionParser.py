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

from .CultureInfo import CultureInfo
from .Tools import NumberToDay, NumberToMonth
from .Exception import MissingFieldException, FormatException


class ExpressionParser(object):
    m_expression = ''
    m_options = None

    """
    Initializes a new instance of the <see cref="ExpressionParser"/> class
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

    def Parse(self):
        # Initialize all elements of parsed array to empty strings
        parsed = ['', '', '', '', '', '', '']

        if self.m_expression is None or len(self.m_expression) == 0:
            raise MissingFieldException("ExpressionDescriptor.expression")
        else:
            expressionPartsTemp = self.m_expression.split(' ')
            expressionPartsTempLength = len(expressionPartsTemp)
            if expressionPartsTempLength < 5:
                raise FormatException(
                    "Error: Expression only has {0} parts.  At least 5 part are required.".format(
                        expressionPartsTempLength))
            elif expressionPartsTempLength == 5:
                # 5 part cron so shift array past seconds element
                parsed[1] = expressionPartsTemp[0]
                parsed[2] = expressionPartsTemp[1]
                parsed[3] = expressionPartsTemp[2]
                parsed[4] = expressionPartsTemp[3]
                parsed[5] = expressionPartsTemp[4]

            elif expressionPartsTempLength == 6:
                # If last element ends with 4 digits, a year element has been
                # supplied and no seconds element
                yearRegex = re.compile("\d{4}$")
                if yearRegex.search(expressionPartsTemp[5]) is not None:
                    parsed[1] = expressionPartsTemp[0]
                    parsed[2] = expressionPartsTemp[1]
                    parsed[3] = expressionPartsTemp[2]
                    parsed[4] = expressionPartsTemp[3]
                    parsed[5] = expressionPartsTemp[4]
                    parsed[6] = expressionPartsTemp[5]
                else:
                    for i in range(0, expressionPartsTempLength):
                        parsed[i] = expressionPartsTemp[i]
            elif expressionPartsTempLength == 7:
                parsed = expressionPartsTemp
            else:
                raise FormatException(
                    "Error: Expression has too many parts ({0}).  Expression must not have more than 7 parts.".format(
                        expressionPartsTempLength))
        self.NormalizeExpression(parsed)

        return parsed

    """
    Converts cron expression components into consistent, predictable formats.
    @param: expressionParts A 7 part string array, one part for each component of the cron expression
    """

    def NormalizeExpression(self, expressionParts):
        # convert ? to * only for DOM and DOW
        expressionParts[3] = expressionParts[3].replace("?", "*")
        expressionParts[5] = expressionParts[5].replace("?", "*")

        # convert 0/, 1/ to */
        if expressionParts[0].startswith("0/"):
            expressionParts[0] = expressionParts[
                0].replace("0/", "*/")  # seconds

        if expressionParts[1].startswith("0/"):
            expressionParts[1] = expressionParts[
                1].replace("0/", "*/")  # minutes

        if expressionParts[2].startswith("0/"):
            expressionParts[2] = expressionParts[
                2].replace("0/", "*/")  # hours

        if expressionParts[3].startswith("1/"):
            expressionParts[3] = expressionParts[3].replace("1/", "*/")  # DOM

        if expressionParts[4].startswith("1/"):
            expressionParts[4] = expressionParts[
                4].replace("1/", "*/")  # Month

        if expressionParts[5].startswith("1/"):
            expressionParts[5] = expressionParts[5].replace("1/", "*/")  # DOW

        # convert */1 to *
        length = len(expressionParts)
        for i in range(0, length):
            if expressionParts[i] == "*/1":
                expressionParts[i] = "*"

        # handle DayOfWeekStartIndexZero option where SUN=1 rather than SUN=0
        if self.m_options.DayOfWeekStartIndexZero is False:
            dowChars = list(expressionParts[5])
            for i in range(0, len(dowChars)):
                if i == 0 or dowChars[i - 1] != '#':
                    try:
                        charNumeric = int(dowChars[i])
                        dowChars[i] = str(charNumeric - 1)[0]
                    except ValueError:
                        pass
            expressionParts[5] = ''.join(dowChars)

        # convert SUN-SAT format to 0-6 format
        for i in range(0, 6):
            expressionParts[5] = expressionParts[
                5].replace(NumberToDay(i)[:3].upper(), str(i))

        # convert JAN-DEC format to 1-12 format
        for i in range(1, 13):
            expressionParts[4] = expressionParts[4].replace(
                NumberToMonth(i)[:3].upper(), str(i))

        # convert 0 second to (empty)
        if expressionParts[0] == "0":
            expressionParts[0] = ''
