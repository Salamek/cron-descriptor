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

            # Validate each field
            self.validate_expression(parsed, expression_parts_temp_length)

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

    def validate_expression(self, expression_parts, expr_length):
        """Validation for each expression fields
        Args:
            expression_parts: expression list
            expr_length: length of the list
        """

        """
        Apply different index for varying length of the expression parts as it is mutated by parse().
        Does not validate the case for having both DOW,DOM value because it is already causing exception.
        """
        if expr_length == 5:
            self.second_minute(expression_parts[1], 'Second and Minute')
            self.hour(expression_parts[2], 'Hour')
            self.dayofmonth(expression_parts[3], 'DayOfMonth')
            self.month(expression_parts[4], 'Month')
            self.dayofweek(expression_parts[5], 'DayOfWeek')
        elif expr_length == 6:
            self.second_minute(expression_parts[0], 'Second and Minute')
            self.second_minute(expression_parts[1], 'Second and Minute')
            self.hour(expression_parts[2], 'Hour')
            self.dayofmonth(expression_parts[3], 'DayOfMonth')
            self.month(expression_parts[4], 'Month')
            self.dayofweek(expression_parts[5], 'DayOfWeek')
        else:
            self.second_minute(expression_parts[0], 'Second and Minute')
            self.second_minute(expression_parts[1], 'Second and Minute')
            self.hour(expression_parts[2], 'Hour')
            self.dayofmonth(expression_parts[3], 'DayOfMonth')
            self.month(expression_parts[4], 'Month')
            self.dayofweek(expression_parts[5], 'DayOfWeek')
            self.year(expression_parts[6], 'Year')

    def second_minute(self, expr, prefix):
        """ sec/min expressions (n : Number, s: String)
        *
        nn (1~59)
        nn-nn
        nn/nn
        nn-nn/nn
        */nn
        nn,nn,nn (Maximum 24 elements)
        """
        mi, mx = (0, 59)
        if re.match(r"\d{1,2}$", expr):
            self.check_range(expr=expr, mi=mi, mx=mx, prefix=prefix)
            
        elif re.search(r"[-*,/]", expr):
            if '*' == expr:
                pass

            elif re.match(r"\d{1,2}-\d{1,2}$", expr):
                parts = expr.split("-")
                self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range(expr=parts[1], mi=mi, mx=mx, prefix=prefix)
                self.compare_range(st=parts[0], ed=parts[1], mi=mi, mx=mx, prefix=prefix)
                
            elif re.match(r"\d{1,2}/\d{1,2}$", expr):
                parts = expr.split("/")
                self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range('interval', expr=parts[1], mi=mi, mx=mx, prefix=prefix)
                
            elif re.match(r"\d{1,2}-\d{1,2}/\d{1,2}$", expr):
                parts = expr.split("/")
                fst_parts = parts[0].split("-")
                self.check_range(expr=fst_parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range(expr=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
                self.compare_range(st=fst_parts[0], ed=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
                self.check_range('interval', expr=parts[1], mi=mi, mx=mx, prefix=prefix)
                
            elif re.match(r"\*/\d{1,2}$", expr):
                parts = expr.split("/")
                self.check_range('interval', expr=parts[1], mi=mi, mx=mx, prefix=prefix)
                
            elif re.match(r"^\d{1,2}(,\d{1,2})+$", expr):
                limit = 60
                expr_ls = expr.split(",")
                if len(expr_ls) > limit:
                    msg = "({0}) Exceeded maximum number({1}) of specified value. '{2}' is provided".format(prefix, limit, len(expr_ls))
                    raise FormatException(msg)
                else:
                    for n in expr_ls:
                        self.check_range(expr=n, mi=mi, mx=mx, prefix=prefix)
            else:
                msg = "({0}) Illegal Expression Format '{1}'".format(prefix, expr)
                raise FormatException(msg)
            
        else:
            msg = "({0}) Illegal Expression Format '{1}'".format(prefix, expr)
            raise FormatException(msg)

    def hour(self, expr, prefix):
        """ hour expressions (n : Number, s: String)
        *
        nn (1~23)
        nn-nn
        nn/nn
        nn-nn/nn
        */nn
        nn,nn,nn (Maximum 24 elements)
        """
        mi, mx = (0, 23)
        if re.match(r"\d{1,2}$", expr):
            self.check_range(expr=expr, mi=mi, mx=mx, prefix=prefix)
            
        elif re.search(r"[-*,/]", expr):
            if '*' == expr:
                pass

            elif re.match(r"\d{1,2}-\d{1,2}$", expr):
                parts = expr.split("-")
                self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range(expr=parts[1], mi=mi, mx=mx, prefix=prefix)
                self.compare_range(st=parts[0], ed=parts[1], mi=mi, mx=mx, prefix=prefix)
                
            elif re.match(r"\d{1,2}/\d{1,2}$", expr):
                parts = expr.split("/")
                self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range('interval', expr=parts[1], mi=mi, mx=mx, prefix=prefix)
                
            elif re.match(r"\d{1,2}-\d{1,2}/\d{1,2}$", expr):
                parts = expr.split("/")
                fst_parts = parts[0].split("-")
                self.check_range(expr=fst_parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range(expr=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
                self.compare_range(st=fst_parts[0], ed=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
                self.check_range('interval', expr=parts[1], mi=mi, mx=mx, prefix=prefix)
                
            elif re.match(r"\*/\d{1,2}$", expr):
                parts = expr.split("/")
                self.check_range('interval', expr=parts[1], mi=mi, mx=mx, prefix=prefix)
                
            elif re.match(r"^\d{1,2}(,\d{1,2})+$", expr):
                limit = 24
                expr_ls = expr.split(",")
                if len(expr_ls) > limit:
                    msg = "({0}) Exceeded maximum number({1}) of specified value. '{2}' is provided".format(prefix, 24, len(limit))
                    raise FormatException(msg)
                else:
                    for n in expr_ls:
                        self.check_range(expr=n, mi=mi, mx=mx, prefix=prefix)
            else:
                msg = "({0}) Illegal Expression Format '{1}'".format(prefix, expr)
                raise FormatException(msg)
        else:
            msg = "({0}) Illegal Expression Format '{1}'".format(prefix, expr)
            raise FormatException(msg)

    def dayofmonth(self, expr, prefix):
        """ DAYOfMonth expressions (n : Number, s: String)
        *
        ?
        nn (1~31)
        nn-nn
        nn/nn
        nn-nn/nn
        */nn
        nn,nn,nn (Maximum 31 elements)
        L-nn
        LW
        nW
        """
        mi, mx = (1, 31)
        if re.match(r"\d{1,2}$", expr):
            self.check_range(expr=expr, mi=mi, mx=mx, prefix=prefix)
        elif re.search(r"[-*,/?]", expr):
            if '*' == expr:
                pass

            elif '?' == expr:
                pass

            elif re.match(r"\d{1,2}-\d{1,2}$", expr):
                parts = expr.split("-")
                self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range(expr=parts[1], mi=mi, mx=mx, prefix=prefix)
                self.compare_range(st=parts[0], ed=parts[1], mi=mi, mx=mx, prefix=prefix)
                
            elif re.match(r"\d{1,2}/\d{1,2}$", expr):
                parts = expr.split("/")
                self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range('interval', expr=parts[1], mi=0, mx=mx, prefix=prefix)
                
            elif re.match(r"\d{1,2}-\d{1,2}/\d{1,2}$", expr):
                parts = expr.split("/")
                fst_parts = parts[0].split("-")
                self.check_range(expr=fst_parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range(expr=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
                self.compare_range(st=fst_parts[0], ed=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
                self.check_range('interval', expr=parts[1], mi=0, mx=mx, prefix=prefix)
                
            elif re.match(r"\*/\d{1,2}$", expr):
                parts = expr.split("/")
                self.check_range('interval', expr=parts[1], mi=0, mx=mx, prefix=prefix)
                
            elif re.match(r"^\d{1,2}(,\d{1,2})+$", expr):
                limit = 31
                expr_ls = expr.split(",")
                if len(expr_ls) > 31:
                    msg = "({0}) Exceeded maximum number({1}) of specified value. '{2}' is provided".format(prefix, limit, len(expr_ls))
                    raise FormatException(msg)
                else:
                    for dayofmonth in expr_ls:
                        self.check_range(expr=dayofmonth, mi=mi, mx=mx, prefix=prefix)
            elif re.match(r"^(L|l)-(\d{1,2})$", expr):
                parts = expr.split("-")
                self.check_range(expr=parts[1], mi=mi, mx=mx, prefix=prefix)
            else:
                msg = "Illegal Expression Format '{0}'".format(expr)
                raise FormatException(msg)
            
        elif re.match(r"^(L|l)(W|w)?$", expr):
            pass
            
        elif re.match(r"^(\d{1,2})(w{1}|W{1})$", expr):
            self.check_range(expr=expr[:-1], mi=mi, mx=mx, prefix=prefix)
            
        else:
            msg = "({0}) Illegal Expression Format '{1}'".format(prefix, expr)
            raise FormatException(msg)
    
    def month(self, expr, prefix):
        """ month expressions (n : Number, s: String)
        *
        nn (1~12)
        sss (JAN~DEC)
        nn-nn
        sss-sss
        nn/nn
        nn-nn/nn
        */nn
        nn,nn,nn (Maximum 12 elements)
        """
        mi, mx = (1, 12)
        if re.match(r"\d{1,2}$", expr):
            self.check_range(expr=expr, mi=mi, mx=mx, prefix=prefix)

        elif re.match(r"\D{3}$", expr):
            matched_month = [m for m in self._cron_months.values() if expr == m]
            if len(matched_month) == 0:
                msg = "Invalid Month value '{}'".format(expr)
                raise FormatException(msg)

        elif re.search(r"[-*,/]", expr):
            if '*' == expr:
                pass

            elif re.match(r"\d{1,2}-\d{1,2}$", expr):
                parts = expr.split("-")
                self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range(expr=parts[1], mi=mi, mx=mx, prefix=prefix)
                self.compare_range(st=parts[0], ed=parts[1], mi=mi, mx=mx, prefix=prefix)

            elif re.match(r"\D{3}-\D{3}$", expr):
                parts = expr.split("-")
                cron_months = {v: k for (k, v) in self._cron_months.items()}
                st_not_exist = parts[0] not in cron_months
                ed_not_exist = parts[1] not in cron_months
                if st_not_exist or ed_not_exist:
                    msg = "Invalid Month value '{}'".format(expr)
                    raise FormatException(msg)
                self.compare_range(st=cron_months[parts[0]], ed=cron_months[parts[1]], mi=mi, mx=mx, prefix=prefix)

            elif re.match(r"\d{1,2}/\d{1,2}$", expr):
                parts = expr.split("/")
                self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range('interval', expr=parts[1], mi=0, mx=mx, prefix=prefix)

            elif re.match(r"\d{1,2}-\d{1,2}/\d{1,2}$", expr):
                parts = expr.split("/")
                fst_parts = parts[0].split("-")
                self.check_range(expr=fst_parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range(expr=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
                self.compare_range(st=fst_parts[0], ed=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
                self.check_range('interval', expr=parts[1], mi=0, mx=12, prefix=prefix)

            elif re.match(r"\*/\d{1,2}$", expr):
                parts = expr.split("/")
                self.check_range('interval', expr=parts[1], mi=0, mx=12, prefix=prefix)

            elif re.match(r"^\d{1,2}(,\d{1,2})+$", expr):
                limit = 12
                expr_ls = expr.split(",")
                if len(expr_ls) > limit:
                    msg = "({0}) Exceeded maximum number({1}) of specified value. '{2}' is provided".format(prefix, limit, len(expr_ls))
                    raise FormatException(msg)
                else:
                    for month in expr_ls:
                        self.check_range(expr=month, mi=mi, mx=mx, prefix=prefix)

            elif re.match(r"^(\d{1,2}|\D{3})((,\d{1,2})+|(,\D{3})*)*$", expr):
                limit = 12
                expr_ls = expr.split(",")
                if len(expr_ls) > limit:
                    msg = "({0}) Exceeded maximum number({1}) of specified value. '{2}' is provided".format(prefix, limit, len(expr_ls))
                    raise FormatException(msg)
                else:
                    cron_months = {v: k for (k, v) in self._cron_months.items()}
                    for month in expr_ls:
                        month = cron_months[month.upper()] if len(month) == 3 else month
                        self.check_range(expr=month, mi=mi, mx=mx, prefix=prefix)
            else:
                msg = "({0}) Illegal Expression Format '{1}'".format(prefix, expr)
                raise FormatException(msg)
        else:
            msg = "({0}) Illegal Expression Format '{1}'".format(prefix, expr)
            raise FormatException(msg)
    
    def dayofweek(self, expr, prefix):
        """ DAYOfWeek expressions (n : Number, s: String)
        *
        ?
        n (0~7) - 0 and 7 used interchangeable as Sunday
        sss (SUN~SAT)
        n/n
        n-n/n
        */n
        n-n
        sss-sss
        n|sss,n|sss,n|sss (maximum 7 elements)
        nL
        n#n
        """
        mi, mx = (0, 7)

        if '*' == expr:
            pass

        elif '?' == expr:
            pass

        elif re.match(r"\d{1}$", expr):
            self.check_range(expr=expr, mi=mi, mx=mx, prefix=prefix)

        elif re.match(r"\D{3}$", expr):
            cron_days = {v: k for (k, v) in self._cron_days.items()}
            if expr.upper() in cron_days:
                pass
            else:
                msg = "Invalid DayOfWeek value '{}'".format(expr)
                raise FormatException(msg)

        elif re.match(r"\d{1}/\d{1}$", expr):
            parts = expr.split("/")
            self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
            self.check_range('interval', expr=parts[1], mi=0, mx=mx, prefix=prefix)

        elif re.match(r"\d{1}-\d{1}/\d{1}$", expr):
            parts = expr.split("/")
            fst_parts = parts[0].split("-")
            self.check_range(expr=fst_parts[0], mi=mi, mx=mx, prefix=prefix)
            self.check_range(expr=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
            self.compare_range(st=fst_parts[0], ed=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
            self.check_range('interval', expr=parts[1], mi=0, mx=mx, prefix=prefix)

        elif re.match(r"[*]/\d{1}$", expr):
            parts = expr.split("/")
            self.check_range('interval', expr=parts[1], mi=0, mx=mx, prefix=prefix)

        elif re.match(r"\d{1}-\d{1}$", expr):
            parts = expr.split("-")
            self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
            self.check_range(expr=parts[1], mi=mi, mx=mx, prefix=prefix)
            self.compare_range(st=parts[0], ed=parts[1], mi=mi, mx=mx, prefix=prefix)

        elif re.match(r"\D{3}-\D{3}$", expr):
            parts = expr.split("-")
            cron_days = {v: k for (k, v) in self._cron_days.items()}
            try:
                st_day = cron_days[parts[0].upper()]
                ed_day = cron_days[parts[1].upper()]
            except KeyError:
                msg = "({0}) Invalid DayOfWeek value '{1}'".format(prefix, expr)
                raise FormatException(msg)
            self.compare_range(st=st_day, ed=ed_day, mi=mi, mx=mx, prefix=prefix, type='dow')

        elif re.match(r"^(\d{1}|\D{3})((,\d{1})+|(,\D{3})*)*$", expr):
            limit = 7
            expr_ls = expr.split(",")
            if len(expr_ls) > limit:
                msg = "({0}) Exceeded maximum number({1}) of specified value. '{2}' is provided".format(prefix, limit, len(expr_ls))
                raise FormatException(msg)
            else:
                cron_days = {v: k for (k, v) in self._cron_days.items()}
                for day in expr_ls:
                    day = cron_days[day.upper()] + 1 if len(day) == 3 else day # syncronize by add 1 to cron_days index
                    self.check_range(expr=day, mi=mi, mx=mx, prefix=prefix)

        elif re.match(r"\d{1}(l|L)$", expr):
            parts = expr.upper().split('L')
            self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)

        elif re.match(r"\d{1}#\d{1}$", expr):
            parts = expr.split('#')
            self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
            self.check_range(expr=parts[1], mi=mi, mx=5, prefix=prefix, type='dow')
        else:
            msg = "({0}) Illegal Expression Format '{1}'".format(prefix, expr)
            raise FormatException(msg)
        
    def year(self, expr, prefix):
        """ Year - valid expression (n : Number)
        *
        nnnn(1970~2099) - 4 digits number
        nnnn-nnnn(1970~2099)
        nnnn/nnn(0~129)
        */nnn(0~129)
        nnnn,nnnn,nnnn(1970~2099) - maximum 86 elements
        """
        mi, mx = (1970, 2099)
        if re.match(r"\d{4}$", expr):
            self.check_range(expr=expr, mi=mi, mx=mx, prefix=prefix)
            
        elif re.search(r"[-*,/]", expr):

            if '*' == expr:
                pass

            elif re.match(r"\d{4}-\d{4}$", expr):
                parts = expr.split("-")
                self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range(expr=parts[1], mi=mi, mx=mx, prefix=prefix)
                self.compare_range(st=parts[0], ed=parts[1], mi=mi, mx=mx, prefix=prefix)
                
            elif re.match(r"\d{4}/\d{1,3}$", expr):
                parts = expr.split("/")
                self.check_range(expr=parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range('interval', expr=parts[1], mi=0, mx=129, prefix=prefix)
                
            elif re.match(r"\d{4}-\d{4}/\d{1,3}$", expr):
                parts = expr.split("/")
                fst_parts = parts[0].split("-")
                self.check_range(expr=fst_parts[0], mi=mi, mx=mx, prefix=prefix)
                self.check_range(expr=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
                self.compare_range(st=fst_parts[0], ed=fst_parts[1], mi=mi, mx=mx, prefix=prefix)
                self.check_range('interval', expr=parts[1], mi=0, mx=129, prefix=prefix)
                
            elif re.match(r"\*/\d{1,3}$", expr):
                parts = expr.split("/")
                self.check_range('interval', expr=parts[1], mi=0, mx=129, prefix=prefix)
                
            elif re.match(r"^\d{4}(,\d{4})+$", expr):
                limit = 84
                expr_ls = expr.split(",")
                if len(expr_ls) > limit:
                    msg = "({0}) Exceeded maximum number({1}) of specified value. '{2}' is provided".format(prefix, limit, len(expr_ls))
                    raise FormatException(msg)
                else:
                    for year in expr_ls:
                        self.check_range(expr=year, mi=mi, mx=mx, prefix=prefix)
            else:
                msg = "({0}) Illegal Expression Format '{1}'".format(prefix, expr)
                raise FormatException(msg)
        else:
            msg = "({0}) Illegal Expression Format '{1}'".format(prefix, expr)
            raise FormatException(msg)

    def check_range(self, type=None, **kwargs):
        """
        check if expression value within range of specified limit
        """
        prefix = kwargs["prefix"]
        mi = kwargs["mi"]
        mx = kwargs["mx"]
        expr = kwargs["expr"]
        if int(expr) < mi or mx < int(expr):
            if type is None:
                msg = "{0} values must be between {1} and {2} but '{3}' is provided".format(prefix, mi, mx, expr)
            elif type == "interval":
                msg = "({0}) Accepted increment value range is {1}~{2} but '{3}' is provided".format(prefix,
                                                                                                     mi, mx, expr)
            elif type == 'dow':
                msg = "({0}) Accepted week value is {1}~{2} but '{3}' is provided".format(prefix,mi, mx, expr)
            raise FormatException(msg)
        else:
            pass

    def compare_range(self, type=None, **kwargs):
        """ check 2 expression values size
        does not allow {st} value to be greater than {ed} value
        """
        prefix = kwargs["prefix"]
        st = kwargs["st"]
        ed = kwargs["ed"]
        mi = kwargs["mi"]
        mx = kwargs["mx"]
        if int(st) > int(ed):
            if type is None:
                msg = "({0}) Invalid range '{1}-{2}'. Accepted range is {3}-{4}".format(prefix, st, ed, mi, mx)
            elif type == 'dow':
                msg = "({0}) Invalid range '{1}-{2}'. Accepted range is {3}-{4}".format(prefix,
                                                                                        self._cron_days[st],
                                                                                        self._cron_days[ed], mi, mx)
            raise FormatException(msg)
