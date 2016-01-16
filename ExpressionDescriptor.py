import locale
import re
import calendar

from CasingTypeEnum import CasingTypeEnum
from CultureInfo import CultureInfo
from DescriptionTypeEnum import DescriptionTypeEnum
from ExpressionParser import ExpressionParser

def NumberToDay(dayNumber):
    return ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][dayNumber]

def NumberToMonth(monthNumber):
    return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][monthNumber]


"""
 Converts a Cron Expression into a human readable string
"""
class ExpressionDescriptor(object):
    m_specialCharacters = [ '/', '-', ',', '*' ]
    m_expression = ''
    m_options = None #Options CLASS
    m_expressionParts = [] #ARRAY OR string ?
    m_parsed = False
    m_culture = None # CultureInfo class

    """
    Initializes a new instance of the <see cref="ExpressionDescriptor"/> class
    @param: expression: The cron expression string
    @param: options: Options to control the output description
    """

    def __init__(sefl, expression, options):
        self.m_expression = expression
        self.m_options = options
        self.m_expressionParts = [] #????
        self.m_parsed = False
        self.m_culture = None#????? Thread.CurrentThread.CurrentUICulture

    """
    Generates a human readable string for the Cron Expression
    @param type: Which part(s) of the expression to describe
    @returns: The cron expression description
    """
    def GetDescription(type):
        description = ''

        try:
            if self.m_parsed is False:
                parser = ExpressionParser(self.m_expression, self.m_options)
                self.m_expressionParts = parser.Parse()
                self.m_parsed = True

            if type == DescriptionTypeEnum.FULL:
                description = GetFullDescription()
            if type == DescriptionTypeEnum.TIMEOFDAY:
                description = GetTimeOfDayDescription()
            if type == DescriptionTypeEnum.HOURS:
                description = GetHoursDescription()
            if type == DescriptionTypeEnum.MINUTES:
                description = GetMinutesDescription()
            if type == DescriptionTypeEnum.SECONDS:
                description = GetSecondsDescription()
            if type == DescriptionTypeEnum.DAYOFMONTH:
                description = GetDayOfMonthDescription()
            if type == DescriptionTypeEnum.MONTH:
                description = GetMonthDescription()
            if type == DescriptionTypeEnum.DAYOFWEEK:
                description = GetDayOfWeekDescription()
            if type == DescriptionTypeEnum.YEAR:
                description = GetYearDescription()
            else:
                description = GetSecondsDescription()
        except Exception as ex:
            if self.m_options.ThrowExceptionOnParseError:
                raise
            else:
                description = str(ex)

        return description

    """
    Generates the FULL description
    @returns: The FULL description
    """
    def GetFullDescription(self):
        description = ''

        try:
            timeSegment = GetTimeOfDayDescription()
            dayOfMonthDesc = GetDayOfMonthDescription()
            monthDesc = GetMonthDescription()
            dayOfWeekDesc = GetDayOfWeekDescription()
            yearDesc = GetYearDescription()

            description = "{0}{1}{2}{3}".format(
                timeSegment,
                dayOfWeekDesc if self.m_expressionParts[3] == "*" else dayOfMonthDesc,
                monthDesc,
                yearDesc)

            description = TransformVerbosity(description, self.m_options.Verbose)
            description = TransformCase(description, self.m_options.CasingType)
        except Exception as ex:
            description = CronExpressionDescriptor.Resources.AnErrorOccuredWhenGeneratingTheExpressionD
            if self.m_options.ThrowExceptionOnParseError:
                #throw new FormatException(description, ex)
                raise Exception(description)

        return description

    """
    Generates a description for only the TIMEOFDAY portion of the expression
    @returns: The TIMEOFDAY description
    """
    def GetTimeOfDayDescription(self):
        secondsExpression = self.m_expressionParts[0]
        minuteExpression = self.m_expressionParts[1]
        hourExpression = self.m_expressionParts[2]

        description = []

        #handle special cases first
        if minuteExpression.find(self.m_specialCharacters) == -1 and hourExpression.find(self.m_specialCharacters) == -1 and secondsExpression.find(self.m_specialCharacters) == -1:
            #specific time of day (i.e. 10 14)
            description.append(CronExpressionDescriptor.Resources.AtSpace)
            description.append(FormatTime(hourExpression, minuteExpression, secondsExpression))
        elif "-" in minuteExpression and "," not in minuteExpression and hourExpression.find(self.m_specialCharacters) == -1:
            #minute range in single hour (i.e. 0-10 11)
            minuteParts = minuteExpression.split('-')
            description.append(CronExpressionDescriptor.Resources.EveryMinuteBetweenX0AndX1.format(FormatTime(hourExpression, minuteParts[0]), FormatTime(hourExpression, minuteParts[1])))
        elif "," in hourExpression and minuteExpression.find(self.m_specialCharacters) == -1:
            #hours list with single minute (o.e. 30 6,14,16)
            hourParts = hourExpression.split(',')
            description.append(CronExpressionDescriptor.Resources.At)
            for i in range(0, hourParts.Length):
                description.append(" ")
                description.Append(FormatTime(hourParts[i], minuteExpression))

                if i < (hourParts.Length - 2):
                    description.append(",")

                if i == hourParts.Length - 2:
                    description.append(CronExpressionDescriptor.Resources.SpaceAnd)
        else:
            #default time description
            secondsDescription = GetSecondsDescription()
            minutesDescription = GetMinutesDescription()
            hoursDescription = GetHoursDescription()

            description.append(secondsDescription)

            if len(description) > 0:
                description.append(", ")

            description.append(minutesDescription)

            if len(description) > 0:
                description.Append(", ")

            description.append(hoursDescription)


        return ''.join(description)

    """
    Generates a description for only the SECONDS portion of the expression
    @returns: The SECONDS description
    """
    def GetSecondsDescription(self):
        return GetSegmentDescription(self.m_expressionParts[0], CronExpressionDescriptor.Resources.EverySecond,lambda s: s.PadLeft(2, '0'),lambda s: string.Format(CronExpressionDescriptor.Resources.EveryX0Seconds, s),lambda s: CronExpressionDescriptor.Resources.SecondsX0ThroughX1PastTheMinute,lambda s: CronExpressionDescriptor.Resources.AtX0SecondsPastTheMinute)

    """
    Generates a description for only the MINUTE portion of the expression
    @returns: The MINUTE description
    """
    def GetMinutesDescription(self):
        return GetSegmentDescription(self.m_expressionParts[1],CronExpressionDescriptor.Resources.EveryMinute,lambda s: s.PadLeft(2, '0'),lambda s: string.Format(CronExpressionDescriptor.Resources.EveryX0Minutes, s.PadLeft(2, '0')),lambda s: CronExpressionDescriptor.Resources.MinutesX0ThroughX1PastTheHour,lambda s: '' if s == "0" else CronExpressionDescriptor.Resources.AtX0MinutesPastTheHour)

    """
    Generates a description for only the HOUR portion of the expression
    @returns: The HOUR description
    """
    def GetHoursDescription(self):
        expression = self.m_expressionParts[2]
        return GetSegmentDescription(expression,CronExpressionDescriptor.Resources.EveryHour, lambda s: FormatTime(s, "0"), lambda s: string.Format(CronExpressionDescriptor.Resources.EveryX0Hours, s.PadLeft(2, '0')), lambda s: CronExpressionDescriptor.Resources.BetweenX0AndX1, lambda s: CronExpressionDescriptor.Resources.AtX0)

    """
    Generates a description for only the DAYOFWEEK portion of the expression
    @returns: The DAYOFWEEK description
    """
    def GetDayOfWeekDescription(self):

        def GetDayName(s):
             exp = s
             if "#" in s:
                 exp = s.replace("#", '')
             elif "L" in s:
                 exp = exp.replace("L", '')

             return self.m_culture.DateTimeFormat.GetDayName(int(exp))

        def GetFormat(s):
            format = None
            if "#" in s:
                dayOfWeekOfMonthNumber = s[s.find("#") + 1:]
                dayOfWeekOfMonthDescription = None
                if dayOfWeekOfMonthNumber == "1":
                    dayOfWeekOfMonthDescription = CronExpressionDescriptor.Resources.First
                elif dayOfWeekOfMonthNumber == "2":
                    dayOfWeekOfMonthDescription = CronExpressionDescriptor.Resources.Second
                elif dayOfWeekOfMonthNumber == "3":
                    dayOfWeekOfMonthDescription = CronExpressionDescriptor.Resources.Third
                elif dayOfWeekOfMonthNumber == "4":
                    dayOfWeekOfMonthDescription = CronExpressionDescriptor.Resources.Forth
                elif dayOfWeekOfMonthNumber == "5":
                    dayOfWeekOfMonthDescription = CronExpressionDescriptor.Resources.Fifth


                format = "{}{}{}".format(CronExpressionDescriptor.Resources.ComaOnThe,dayOfWeekOfMonthDescription, CronExpressionDescriptor.Resources.SpaceX0OfTheMonth)
            elif "L" in s:
                format = CronExpressionDescriptor.Resources.ComaOnTheLastX0OfTheMonth
            else:
                format = CronExpressionDescriptor.Resources.ComaOnlyOnX0

            return format

        return GetSegmentDescription(self.m_expressionParts[5], CronExpressionDescriptor.Resources.ComaEveryDay, lambda s: GetDayName(s), lambda s: string.Format(CronExpressionDescriptor.Resources.ComaEveryX0DaysOfTheWeek, s), lambda s: CronExpressionDescriptor.Resources.ComaX0ThroughX1, lambda s: GetFormat(s))

    """
    Generates a description for only the MONTH portion of the expression
    @returns: The MONTH description
    """
    def GetMonthDescription(self):
        return GetSegmentDescription(self.m_expressionParts[4], '',
        lambda s: datetime.date(datetime.date.today().year, int(s), 1).strftime("%B"),
        lambda s: CronExpressionDescriptor.Resources.ComaEveryX0Months.format(s),
        lambda s: CronExpressionDescriptor.Resources.ComaX0ThroughX1,
        lambda s: CronExpressionDescriptor.Resources.ComaOnlyInX0)


    """
    Generates a description for only the DAYOFMONTH portion of the expression
    @returns: The DAYOFMONTH description
    """
    def GetDayOfMonthDescription(self):
        description = None
        expression = self.m_expressionParts[3]
        expression = expression.replace("?", "*")


        if expression == "L":
            description = CronExpressionDescriptor.Resources.ComaOnTheLastDayOfTheMonth
        elif expression == "LW" or expression == "WL":
            description = CronExpressionDescriptor.Resources.ComaOnTheLastWeekdayOfTheMonth
        else:
            regex = re.compile("(\\d{1,2}W)|(W\\d{1,2})")
            if regex.match(expression):
                m = regex.match(expression)
                dayNumber = int(m.group.replace("W", ""))

                dayString =  CronExpressionDescriptor.Resources.FirstWeekday if dayNumber == 1 else CronExpressionDescriptor.Resources.WeekdayNearestDayX0.format(dayNumber)
                description = CronExpressionDescriptor.Resources.ComaOnTheX0OfTheMonth.format(dayString)
            else:
                description = GetSegmentDescription(expression,CronExpressionDescriptor.Resources.ComaEveryDay,lambda s: s,lambda s: CronExpressionDescriptor.Resources.ComaEveryDay if s == "1" else CronExpressionDescriptor.Resources.ComaEveryX0Days,lambda s: CronExpressionDescriptor.Resources.ComaBetweenDayX0AndX1OfTheMonth,lambda s: CronExpressionDescriptor.Resources.ComaOnDayX0OfTheMonth)

        return description

    """
    Generates a description for only the YEAR portion of the expression
    @returns: The YEAR description
    """
    def GetYearDescription(self):
        return GetSegmentDescription(self.m_expressionParts[6],'',
        lambda s: datetime.date(int(s), 1, 1).strftime("%B"),
        lambda s: CronExpressionDescriptor.Resources.ComaEveryX0Years.format(s),
        lambda s: CronExpressionDescriptor.Resources.ComaX0ThroughX1,
        lambda s: CronExpressionDescriptor.Resources.ComaOnlyInX0)

    """
    Returns segment description
    @param: expression
    @param: allDescription
    @param: getSingleItemDescription
    @param: getIntervalDescriptionFormat
    @param: getBetweenDescriptionFormat
    @param: getDescriptionFormat
    @returns segment description
    """

    def GetSegmentDescription(self, expression, allDescription,getSingleItemDescription,getIntervalDescriptionFormat,getBetweenDescriptionFormat,getDescriptionFormat):
        description = None

        if expression is None or expression == '':
            description = ''
        elif expression == "*":
            description = allDescription
        elif any(ext in expression for ext in [ '/', '-', ',' ]):
            description = getDescriptionFormat(expression).format(getSingleItemDescription(expression))
        elif "/" in expression:
            segments = expression.split('/')
            description = getIntervalDescriptionFormat(segments[1]).format(getSingleItemDescription(segments[1]))

            #interval contains 'between' piece (i.e. 2-59/3 )
            if "-" in segments[0]:
                betweenSegmentOfInterval = segments[0]
                betweenSegements = betweenSegmentOfInterval.split('-')
                betweenSegment1Description = getSingleItemDescription(betweenSegements[0])
                betweenSegment2Description = getSingleItemDescription(betweenSegements[1])
                betweenSegment2Description = betweenSegment2Description.replace(":00", ":59")
                description += ", " + getBetweenDescriptionFormat(betweenSegmentOfInterval).format(betweenSegment1Description, betweenSegment2Description)
        elif "-" in expression:
            segments = expression.split('-')
            betweenSegment1Description = getSingleItemDescription(segments[0])
            betweenSegment2Description = getSingleItemDescription(segments[1])
            betweenSegment2Description = betweenSegment2Description.replace(":00", ":59")
            description = getBetweenDescriptionFormat(expression).format(betweenSegment1Description, betweenSegment2Description)
        elif "," in expression:
            segments = expression.split(',')

            descriptionContent = ''
            for i in range(0, len(segments)):
                if i > 0 and len(segments) > 2:
                    descriptionContent += ","

                    if i < segments.Length - 1:
                        descriptionContent += " "

                if i > 0 and segments.Length > 1 and (i == segments.Length - 1 or segments.Length == 2):
                    descriptionContent += CronExpressionDescriptor.Resources.SpaceAndSpace

                descriptionContent += getSingleItemDescription(segments[i])

            description = getDescriptionFormat(expression).format(descriptionContent)

        return description


    """
    Given time parts, will contruct a formatted time description
    @param: hourExpression Hours part
    @param: minuteExpression Minutes part
    @param: secondExpression Seconds part
    @returns: Formatted time description
    """
    def FormatTime(self, hourExpression, minuteExpression, secondExpression = ''):
        hour = int(hourExpression)

        period = ''
        if self.m_options.Use24HourTimeFormat is False:
            period =  " PM" if (hour >= 12) else " AM"
            if hour > 12:
                hour -= 12

        minute = str(int(minuteExpression)) #!FIXME WUT ???
        second = ''
        if string is not None and len(string) > 0:
            second = "{}{}".format(":", str(int(secondExpression)).zfill(2))

        return "{0}:{1}{2}{3}".format(str(hour).zfill(2), minute.zfill(2), second, period)

    """
    Transforms the verbosity of the expression description by stripping verbosity from original description
    @param: description The description to transform
    @param: isVerbose If true, will leave description as it, if false, will strip verbose parts
    @returns: The transformed description with proper verbosity
    """
    def TransformVerbosity(self, description, useVerboseFormat):
        if useVerboseFormat is False:
            description = description.replace(CronExpressionDescriptor.Resources.ComaEveryMinute, '')
            description = description.replace(CronExpressionDescriptor.Resources.ComaEveryHour, '')
            description = description.replace(CronExpressionDescriptor.Resources.ComaEveryDay, '')
        return description

    """
    Transforms the case of the expression description, based on options
    @param: description The description to transform
    @param: caseType The casing type that controls the output casing
    @returns: The transformed description with proper casing
    """
    def TransformCase(self, description, caseType):
        if caseType == CasingTypeEnum.Sentence:
            description = "{}{}".format(Thread.CurrentThread.CurrentCulture.TextInfo.ToUpper(description[0]), description[1:])
        elif caseType == CasingTypeEnum.Title:
            description = Thread.CurrentThread.CurrentCulture.TextInfo.ToTitleCase(description)
        else:
            description = description.lower()
        return description

    """
    Generates a human readable string for the Cron Expression
    @param: expression The cron expression string
    @param: options Options to control the output description
    @returns: The cron expression description
    """
    def GetDescription(self, expression, options = None):
        descripter = ExpressionDescriptor(expression, options)
        return descripter.GetDescription(DescriptionTypeEnum.FULL)
