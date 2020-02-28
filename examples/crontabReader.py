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

try:
    from cron_descriptor import Options, ExpressionDescriptor
except ImportError:
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('\033[1mFailed to import cron_descriptor, maybe ? "pip install cron-descriptor ?"\033[0m')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    raise


class CrontabReader(object):

    """
    Simple example reading /etc/contab
    """
    rex = re.compile(r"^(\S{1,3}\s+\S{1,3}\s+\S{1,3}\s+\S{1,3}\s+\S{1,3}).+$")

    def __init__(self, cronfile):
        """Initialize CrontabReader

        Args:
            cronfile: Path to cronfile
        Returns:
            None
        """
        options = Options()
        options.day_of_week_start_index_zero = False
        options.use_24hour_time_format = True
        with open(cronfile) as f:
            for line in f.readlines():
                parsed_line = self.parse_cron_line(line)
                if parsed_line:
                    print("{} -> {}".format(parsed_line, ExpressionDescriptor(parsed_line, options)))

    def parse_cron_line(self, line):
        """Parses crontab line and returns only starting time string

        Args:
            line: crontab line
        Returns:
            Time part of cron line
        """
        stripped = line.strip()

        if stripped and stripped.startswith('#') is False:
            rexres = self.rex.search(stripped)
            if rexres:
                return ' '.join(rexres.group(1).split())

        return None


CrontabReader('/etc/crontab')
