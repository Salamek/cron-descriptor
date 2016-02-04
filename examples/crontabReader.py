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
    rex = re.compile("^(\S{1,3}\s+\S{1,3}\s+\S{1,3}\s+\S{1,3}\s+\S{1,3}).+$")

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
