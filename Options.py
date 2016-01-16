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

        #culture specific default options

        self.Use24HourTimeFormat = CultureInfo().getCode() in ["ru-RU", "uk-UA", "de-DE", "it-IT", "tr-TR", "cs-CZ"]

    def ThrowExceptionOnParseError(self):
        pass
         #{ get; set; }
    def CasingType(self):
         #{ get; set; }
         pass
    def Verbose(self):
         #{ get; set; }
         pass
    def DayOfWeekStartIndexZero(self):
        pass
         #{ get; set; }
    def Use24HourTimeFormat(self):
        pass
         #{ get; set; }
