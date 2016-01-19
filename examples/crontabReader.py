from cron_descriptor import Options, ExpressionDescriptor
import re

"""
Simple example reading /etc/contab
"""


class CrontabReader(object):
    rex = re.compile("^(\S{1,3}\s+\S{1,3}\s+\S{1,3}\s+\S{1,3}\s+\S{1,3}).+$")

    def __init__(self, cronfile):
        options = Options()
        options.day_of_week_start_index_zero = False
        options.use_24hour_time_format = True
        with open(cronfile) as f:
            for line in f.readlines():
                parsed_line = self.parse_cron_line(line)
                if parsed_line:
                    print("{} -> {}".format(parsed_line, ExpressionDescriptor(parsed_line, options)))

    def parse_cron_line(self, line):
        stripped = line.strip()

        if stripped and stripped.startswith('#') is False:
            rexres = self.rex.search(stripped)
            if rexres:
                return ' '.join(rexres.group(1).split())

        return None

CrontabReader('/etc/crontab')
