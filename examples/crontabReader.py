from cron_descriptor.ExpressionDescriptor import ExpressionDescriptor
from cron_descriptor.Options import Options
from cron_descriptor.DescriptionTypeEnum import DescriptionTypeEnum
import re

"""
Simple example reading /etc/contab
"""
class crontabReader(object):
    rex = re.compile("^(\S{1,3}\s+\S{1,3}\s+\S{1,3}\s+\S{1,3}\s+\S{1,3}).+$")
    def __init__(self, cronfile):
        options = Options()
        options.DayOfWeekStartIndexZero = False
        options.Use24HourTimeFormat = True
        with open(cronfile) as f:
            for line in f.readlines():
                parsedLine = self.parseCronLine(line)
                if parsedLine:
                    print("{} -> {}".format(parsedLine, ExpressionDescriptor(parsedLine, options)))

    def parseCronLine(self, line):
        stripped = line.strip()

        if stripped and stripped.startswith('#') is False:
            rexres = self.rex.search(stripped)
            if rexres:
                return ' '.join(rexres.group(1).split())

        return None

crontabReader('/etc/crontab')
