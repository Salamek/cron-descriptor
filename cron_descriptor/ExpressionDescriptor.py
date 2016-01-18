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
import datetime

from .CasingTypeEnum import CasingTypeEnum
from .CultureInfo import CultureInfo
from .DescriptionTypeEnum import DescriptionTypeEnum
from .ExpressionParser import ExpressionParser
from .Options import Options
from .Resources import Resources
from .Tools import NumberToDay, NumberToMonth
from .StringBuilder import StringBuilder
from .Exception import FormatException

"""
 Converts a Cron Expression into a human readable string
"""


class ExpressionDescriptor(object):
    m_specialCharacters = ['/', '-', ',', '*']
    m_expression = ''
    m_options = None
    m_expressionParts = []
    m_parsed = False

    """
    Initializes a new instance of the <see cref="ExpressionDescriptor"/> class
    @param: expression: The cron expression string
    @param: options: Options to control the output description
    """

    def __init__(self, expression, options):
        self.m_expression = expression
        self.m_options = options
        self.m_expressionParts = []
        self.m_parsed = False

    """
    Generates a human readable string for the Cron Expression
    @param type: Which part(s) of the expression to describe
    @returns: The cron expression description
    """

    def GetDescription(self, type):
        description = ''

        try:
            if self.m_parsed is False:
                parser = ExpressionParser(self.m_expression, self.m_options)
                self.m_expressionParts = parser.Parse()
                self.m_parsed = True

            if type == DescriptionTypeEnum.FULL:
                description = self.GetFullDescription()
            elif type == DescriptionTypeEnum.TIMEOFDAY:
                description = self.GetTimeOfDayDescription()
            elif type == DescriptionTypeEnum.HOURS:
                description = self.GetHoursDescription()
            elif type == DescriptionTypeEnum.MINUTES:
                description = self.GetMinutesDescription()
            elif type == DescriptionTypeEnum.SECONDS:
                description = self.GetSecondsDescription()
            elif type == DescriptionTypeEnum.DAYOFMONTH:
                description = self.GetDayOfMonthDescription()
            elif type == DescriptionTypeEnum.MONTH:
                description = self.GetMonthDescription()
            elif type == DescriptionTypeEnum.DAYOFWEEK:
                description = self.GetDayOfWeekDescription()
            elif type == DescriptionTypeEnum.YEAR:
                description = self.GetYearDescription()
            else:
                description = self.GetSecondsDescription()

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
            timeSegment = self.GetTimeOfDayDescription()
            dayOfMonthDesc = self.GetDayOfMonthDescription()
            monthDesc = self.GetMonthDescription()
            dayOfWeekDesc = self.GetDayOfWeekDescription()
            yearDesc = self.GetYearDescription()

            description = "{0}{1}{2}{3}".format(
                timeSegment,
                dayOfWeekDesc if self.m_expressionParts[
                    3] == "*" else dayOfMonthDesc,
                monthDesc,
                yearDesc)

            description = self.TransformVerbosity(
                description, self.m_options.Verbose)
            description = self.TransformCase(
                description,
                self.m_options.CasingType)
        except Exception as ex:
            raise
            description = Resources.AnErrorOccuredWhenGeneratingTheExpressionD
            if self.m_options.ThrowExceptionOnParseError:
                raise FormatException(description)

        return description

    """
    Generates a description for only the TIMEOFDAY portion of the expression
    @returns: The TIMEOFDAY description
    """

    def GetTimeOfDayDescription(self):
        secondsExpression = self.m_expressionParts[0]
        minuteExpression = self.m_expressionParts[1]
        hourExpression = self.m_expressionParts[2]

        description = StringBuilder()

        # handle special cases first
        if any(exp in minuteExpression for exp in self.m_specialCharacters) is False and any(exp in hourExpression for exp in self.m_specialCharacters) is False and any(exp in secondsExpression for exp in self.m_specialCharacters) is False:
            # specific time of day (i.e. 10 14)
            description.append(Resources.AtSpace)
            description.append(
                self.FormatTime(
                    hourExpression,
                    minuteExpression,
                    secondsExpression))
        elif "-" in minuteExpression and "," not in minuteExpression and any(exp in hourExpression for exp in self.m_specialCharacters) is False:
            # minute range in single hour (i.e. 0-10 11)
            minuteParts = minuteExpression.split('-')
            description.append(Resources.EveryMinuteBetweenX0AndX1.format(
                self.FormatTime(hourExpression, minuteParts[0]), self.FormatTime(hourExpression, minuteParts[1])))
        elif "," in hourExpression and any(exp in minuteExpression for exp in self.m_specialCharacters) is False:
            # hours list with single minute (o.e. 30 6,14,16)
            hourParts = hourExpression.split(',')
            description.append(Resources.At)
            for i in range(0, len(hourParts)):
                description.append(" ")
                description.append(
                    self.FormatTime(hourParts[i], minuteExpression))

                if i < (len(hourParts) - 2):
                    description.append(",")

                if i == len(hourParts) - 2:
                    description.append(Resources.SpaceAnd)
        else:
            # default time description
            secondsDescription = self.GetSecondsDescription()
            minutesDescription = self.GetMinutesDescription()
            hoursDescription = self.GetHoursDescription()

            description.append(secondsDescription)

            if len(description) > 0:
                description.append(", ")

            description.append(minutesDescription)

            if len(description) > 0:
                description.append(", ")

            description.append(hoursDescription)
        return description.toString()

    """
    Generates a description for only the SECONDS portion of the expression
    @returns: The SECONDS description
    """

    def GetSecondsDescription(self):
        return self.GetSegmentDescription(self.m_expressionParts[0], Resources.EverySecond, lambda s: s.zfill(2), lambda s: Resources.EveryX0Seconds.format(s), lambda s: Resources.SecondsX0ThroughX1PastTheMinute, lambda s: Resources.AtX0SecondsPastTheMinute)

    """
    Generates a description for only the MINUTE portion of the expression
    @returns: The MINUTE description
    """

    def GetMinutesDescription(self):
        return self.GetSegmentDescription(self.m_expressionParts[1], Resources.EveryMinute, lambda s: s.zfill(2), lambda s: Resources.EveryX0Minutes.format(s.zfill(2)), lambda s: Resources.MinutesX0ThroughX1PastTheHour, lambda s: '' if s == "0" else Resources.AtX0MinutesPastTheHour)

    """
    Generates a description for only the HOUR portion of the expression
    @returns: The HOUR description
    """

    def GetHoursDescription(self):
        expression = self.m_expressionParts[2]
        return self.GetSegmentDescription(expression, Resources.EveryHour, lambda s: self.FormatTime(s, "0"), lambda s: Resources.EveryX0Hours.format(s.zfill(2)), lambda s: Resources.BetweenX0AndX1, lambda s: Resources.AtX0)

    """
    Generates a description for only the DAYOFWEEK portion of the expression
    @returns: The DAYOFWEEK description
    """

    def GetDayOfWeekDescription(self):

        def GetDayName(s):
            exp = s
            if "#" in s:
                exp, useless = s.split("#", 2)
            elif "L" in s:
                exp = exp.replace("L", '')
            return NumberToDay(int(exp))

        def GetFormat(s):
            format = None
            if "#" in s:
                dayOfWeekOfMonthNumber = s[s.find("#") + 1:]
                dayOfWeekOfMonthDescription = None
                if dayOfWeekOfMonthNumber == "1":
                    dayOfWeekOfMonthDescription = Resources.First
                elif dayOfWeekOfMonthNumber == "2":
                    dayOfWeekOfMonthDescription = Resources.Second
                elif dayOfWeekOfMonthNumber == "3":
                    dayOfWeekOfMonthDescription = Resources.Third
                elif dayOfWeekOfMonthNumber == "4":
                    dayOfWeekOfMonthDescription = Resources.Forth
                elif dayOfWeekOfMonthNumber == "5":
                    dayOfWeekOfMonthDescription = Resources.Fifth

                format = "{}{}{}".format(Resources.ComaOnThe,
                                         dayOfWeekOfMonthDescription, Resources.SpaceX0OfTheMonth)
            elif "L" in s:
                format = Resources.ComaOnTheLastX0OfTheMonth
            else:
                format = Resources.ComaOnlyOnX0

            return format

        return self.GetSegmentDescription(self.m_expressionParts[5], Resources.ComaEveryDay, lambda s: GetDayName(s), lambda s: Resources.ComaEveryX0DaysOfTheWeek.format(s), lambda s: Resources.ComaX0ThroughX1, lambda s: GetFormat(s))

    """
    Generates a description for only the MONTH portion of the expression
    @returns: The MONTH description
    """

    def GetMonthDescription(self):
        return self.GetSegmentDescription(self.m_expressionParts[4], '',
                                          lambda s: datetime.date(
            datetime.date.today(
            ).year, int(s), 1).strftime("%B"),
            lambda s: Resources.ComaEveryX0Months.format(
            s),
                                     lambda s: Resources.ComaX0ThroughX1,
                                     lambda s: Resources.ComaOnlyInX0)

    """
    Generates a description for only the DAYOFMONTH portion of the expression
    @returns: The DAYOFMONTH description
    """

    def GetDayOfMonthDescription(self):
        description = None
        expression = self.m_expressionParts[3]
        expression = expression.replace("?", "*")

        if expression == "L":
            description = Resources.ComaOnTheLastDayOfTheMonth
        elif expression == "LW" or expression == "WL":
            description = Resources.ComaOnTheLastWeekdayOfTheMonth
        else:
            regex = re.compile("(\\d{1,2}W)|(W\\d{1,2})")
            if regex.match(expression):
                m = regex.match(expression)
                dayNumber = int(m.group().replace("W", ""))

                dayString = Resources.FirstWeekday if dayNumber == 1 else Resources.WeekdayNearestDayX0.format(
                    dayNumber)
                description = Resources.ComaOnTheX0OfTheMonth.format(
                    dayString)
            else:
                description = self.GetSegmentDescription(
                    expression, Resources.ComaEveryDay, lambda s: s, lambda s: Resources.ComaEveryDay if s == "1" else Resources.ComaEveryX0Days,
                                                    lambda s: Resources.ComaBetweenDayX0AndX1OfTheMonth, lambda s: Resources.ComaOnDayX0OfTheMonth)

        return description

    """
    Generates a description for only the YEAR portion of the expression
    @returns: The YEAR description
    """

    def GetYearDescription(self):
        return self.GetSegmentDescription(self.m_expressionParts[6], '',
                                          lambda s: s.zfill(4),
                                          lambda s: Resources.ComaEveryX0Years.format(
            s),
            lambda s: Resources.ComaX0ThroughX1,
                                     lambda s: Resources.ComaOnlyInX0)

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

    def GetSegmentDescription(
        self,
        expression,
     allDescription,
     getSingleItemDescription,
     getIntervalDescriptionFormat,
     getBetweenDescriptionFormat,
     getDescriptionFormat):
        description = None
        if expression is None or expression == '':
            description = ''
        elif expression == "*":
            description = allDescription
        elif any(ext in expression for ext in ['/', '-', ',']) is False:
            description = getDescriptionFormat(expression).format(
                getSingleItemDescription(expression))
        elif "/" in expression:
            segments = expression.split('/')
            description = getIntervalDescriptionFormat(
                segments[1]).format(getSingleItemDescription(segments[1]))

            # interval contains 'between' piece (i.e. 2-59/3 )
            if "-" in segments[0]:
                betweenSegmentOfInterval = segments[0]
                betweenSegements = betweenSegmentOfInterval.split('-')
                betweenSegment1Description = getSingleItemDescription(
                    betweenSegements[0])
                betweenSegment2Description = getSingleItemDescription(
                    betweenSegements[1])
                betweenSegment2Description = betweenSegment2Description.replace(
                    ":00", ":59")
                description += ", " + getBetweenDescriptionFormat(betweenSegmentOfInterval).format(
                    betweenSegment1Description, betweenSegment2Description)
        elif "-" in expression:
            segments = expression.split('-')
            betweenSegment1Description = getSingleItemDescription(segments[0])
            betweenSegment2Description = getSingleItemDescription(segments[1])
            betweenSegment2Description = betweenSegment2Description.replace(
                ":00", ":59")
            description = getBetweenDescriptionFormat(expression).format(
                betweenSegment1Description, betweenSegment2Description)
        elif "," in expression:
            segments = expression.split(',')

            descriptionContent = ''
            for i in range(0, len(segments)):
                if i > 0 and len(segments) > 2:
                    descriptionContent += ","

                    if i < len(segments) - 1:
                        descriptionContent += " "

                if i > 0 and len(segments) > 1 and (i == len(segments) - 1 or len(segments) == 2):
                    descriptionContent += Resources.SpaceAndSpace

                descriptionContent += getSingleItemDescription(segments[i])

            description = getDescriptionFormat(
                expression).format(
                    descriptionContent)

        return description

    """
    Given time parts, will contruct a formatted time description
    @param: hourExpression Hours part
    @param: minuteExpression Minutes part
    @param: secondExpression Seconds part
    @returns: Formatted time description
    """

    def FormatTime(
        self,
        hourExpression,
     minuteExpression,
     secondExpression=''):
        hour = int(hourExpression)

        period = ''
        if self.m_options.Use24HourTimeFormat is False:
            period = " PM" if (hour >= 12) else " AM"
            if hour > 12:
                hour -= 12

        minute = str(int(minuteExpression))  # !FIXME WUT ???
        second = ''
        if secondExpression is not None and len(secondExpression) > 0:
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
            description = description.replace(
                Resources.ComaEveryMinute, '')
            description = description.replace(Resources.ComaEveryHour, '')
            description = description.replace(Resources.ComaEveryDay, '')
        return description

    """
    Transforms the case of the expression description, based on options
    @param: description The description to transform
    @param: caseType The casing type that controls the output casing
    @returns: The transformed description with proper casing
    """

    def TransformCase(self, description, caseType):
        if caseType == CasingTypeEnum.Sentence:
            description = "{}{}".format(
                description[0].upper(),
                description[1:])
        elif caseType == CasingTypeEnum.Title:
            description = description.title()
        else:
            description = description.lower()
        return description

"""
Generates a human readable string for the Cron Expression
@param: expression The cron expression string
@param: options Options to control the output description
@returns: The cron expression description
"""


def GetDescription(expression, options=Options()):
    descripter = ExpressionDescriptor(expression, options)
    return descripter.GetDescription(DescriptionTypeEnum.FULL)
