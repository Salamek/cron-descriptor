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

import tests.TestCase as TestCase
from cron_descriptor.Options import Options
from cron_descriptor.CasingTypeEnum import CasingTypeEnum
from cron_descriptor.DescriptionTypeEnum import DescriptionTypeEnum
from cron_descriptor.ExpressionDescriptor import ExpressionDescriptor, GetDescription
from cron_descriptor.Exception import MissingFieldException, FormatException


class TestFormats(TestCase.TestCase):

    def testEveryMinute(self):

        self.assertEqual("Every minute", GetDescription("* * * * *"))

    def testEvery1Minute(self):

        self.assertEqual("Every minute", GetDescription("*/1 * * * *"))
        self.assertEqual("Every minute", GetDescription("0 0/1 * * * ?"))

    def testEveryHour(self):

        self.assertEqual("Every hour", GetDescription("0 0 * * * ?"))
        self.assertEqual("Every hour", GetDescription("0 0 0/1 * * ?"))

    def testTimeOfDayCertainDaysOfWeek(self):

        self.assertEqual(
            "At 11:00 PM, Monday through Friday",
            GetDescription("0 23 ? * MON-FRI"))

    def testEverySecond(self):

        self.assertEqual("Every second", GetDescription("* * * * * *"))

    def testEvery45Seconds(self):

        self.assertEqual("Every 45 seconds", GetDescription("*/45 * * * * *"))

    def testEvery5Minutes(self):

        self.assertEqual("Every 05 minutes", GetDescription("*/5 * * * *"))
        self.assertEqual("Every 10 minutes", GetDescription("0 0/10 * * * ?"))

    def testEvery5MinutesOnTheSecond(self):

        self.assertEqual("Every 05 minutes", GetDescription("0 */5 * * * *"))

    def testWeekdaysAtTime(self):

        self.assertEqual(
            "At 11:30 AM, Monday through Friday",
            GetDescription("30 11 * * 1-5"))

    def testDailyAtTime(self):

        self.assertEqual("At 11:30 AM", GetDescription("30 11 * * *"))

    def testMinuteSpan(self):

        self.assertEqual(
            "Every minute between 11:00 AM and 11:10 AM", GetDescription("0-10 11 * * *"))

    def testOneMonthOnly(self):

        self.assertEqual(
            "Every minute, only in March",
            GetDescription("* * * 3 *"))

    def testTwoMonthsOnly(self):

        self.assertEqual(
            "Every minute, only in March and June",
            GetDescription("* * * 3,6 *"))

    def testTwoTimesEachAfternoon(self):

        self.assertEqual(
            "At 02:30 PM and 04:30 PM",
            GetDescription("30 14,16 * * *"))

    def testThreeTimesDaily(self):

        self.assertEqual(
            "At 06:30 AM, 02:30 PM and 04:30 PM",
            GetDescription("30 6,14,16 * * *"))

    def testOnceAWeek(self):

        self.assertEqual(
            "At 09:46 AM, only on Monday",
            GetDescription("46 9 * * 1"))

    def testDayOfMonth(self):

        self.assertEqual(
            "At 12:23 PM, on day 15 of the month",
            GetDescription("23 12 15 * *"))

    def testMonthName(self):

        self.assertEqual(
            "At 12:23 PM, only in January",
            GetDescription("23 12 * JAN *"))

    def testDayOfMonthWithQuestionMark(self):

        self.assertEqual(
            "At 12:23 PM, only in January",
            GetDescription("23 12 ? JAN *"))

    def testMonthNameRange2(self):

        self.assertEqual(
            "At 12:23 PM, January through February", GetDescription("23 12 * JAN-FEB *"))

    def testMonthNameRange3(self):

        self.assertEqual(
            "At 12:23 PM, January through March",
            GetDescription("23 12 * JAN-MAR *"))

    def testDayOfWeekName(self):

        self.assertEqual(
            "At 12:23 PM, only on Sunday",
            GetDescription("23 12 * * SUN"))

    def testDayOfWeekRange(self):

        self.assertEqual(
            "Every 05 minutes, at 03:00 PM, Monday through Friday", GetDescription("*/5 15 * * MON-FRI"))

    def testDayOfWeekOnceInMonth(self):

        self.assertEqual(
            "Every minute, on the third Monday of the month", GetDescription("* * * * MON#3"))

    def testLastDayOfTheWeekOfTheMonth(self):

        self.assertEqual(
            "Every minute, on the last Thursday of the month", GetDescription("* * * * 4L"))

    def testLastDayOfTheMonth(self):

        self.assertEqual(
            "Every 05 minutes, on the last day of the month, only in January", GetDescription("*/5 * L JAN *"))

    def testLastWeekdayOfTheMonth(self):

        self.assertEqual(
            "Every minute, on the last weekday of the month", GetDescription("* * LW * *"))

    def testLastWeekdayOfTheMonth2(self):

        self.assertEqual(
            "Every minute, on the last weekday of the month", GetDescription("* * WL * *"))

    def testFirstWeekdayOfTheMonth(self):

        self.assertEqual(
            "Every minute, on the first weekday of the month", GetDescription("* * 1W * *"))

    def testThirteenthWeekdayOfTheMonth(self):

        self.assertEqual(
            "Every minute, on the weekday nearest day 13 of the month", GetDescription("* * 13W * *"))

    def testFirstWeekdayOfTheMonth2(self):

        self.assertEqual(
            "Every minute, on the first weekday of the month", GetDescription("* * W1 * *"))

    def testParticularWeekdayOfTheMonth(self):

        self.assertEqual(
            "Every minute, on the weekday nearest day 5 of the month", GetDescription("* * 5W * *"))

    def testParticularWeekdayOfTheMonth2(self):

        self.assertEqual(
            "Every minute, on the weekday nearest day 5 of the month", GetDescription("* * W5 * *"))

    def testTimeOfDayWithSeconds(self):

        self.assertEqual("At 02:02:30 PM", GetDescription("30 02 14 * * *"))

    def testSecondInternvals(self):

        self.assertEqual(
            "Seconds 05 through 10 past the minute",
            GetDescription("5-10 * * * * *"))

    def testSecondMinutesHoursIntervals(self):

        self.assertEqual(
            "Seconds 05 through 10 past the minute, minutes 30 through 35 past the hour, between 10:00 AM and 12:59 PM", GetDescription("5-10 30-35 10-12 * * *"))

    def testEvery5MinutesAt30Seconds(self):

        self.assertEqual(
            "At 30 seconds past the minute, every 05 minutes", GetDescription("30 */5 * * * *"))

    def testMinutesPastTheHourRange(self):

        self.assertEqual(
            "At 30 minutes past the hour, between 10:00 AM and 01:59 PM, only on Wednesday and Friday", GetDescription("0 30 10-13 ? * WED,FRI"))

    def testSecondsPastTheMinuteInterval(self):

        self.assertEqual(
            "At 10 seconds past the minute, every 05 minutes", GetDescription("10 0/5 * * * ?"))

    def testBetweenWithInterval(self):

        self.assertEqual(
            "Every 03 minutes, minutes 02 through 59 past the hour, at 01:00 AM, 09:00 AM, and 10:00 PM, between day 11 and 26 of the month, January through June",
                         GetDescription("2-59/3 1,9,22 11-26 1-6 ?"))

    def testRecurringFirstOfMonth(self):

        self.assertEqual("At 06:00 AM", GetDescription("0 0 6 1/1 * ?"))

    def testMinutesPastTheHour(self):

        self.assertEqual(
            "At 05 minutes past the hour",
            GetDescription("0 5 0/1 * * ?"))

    def testOneYearOnlyWithSeconds(self):

        self.assertEqual(
            "Every second, only in 2013",
            GetDescription("* * * * * * 2013"))

    def testOneYearOnlyWithoutSeconds(self):

        self.assertEqual(
            "Every minute, only in 2013",
            GetDescription("* * * * * 2013"))

    def testTwoYearsOnly(self):

        self.assertEqual(
            "Every minute, only in 2013 and 2014", GetDescription("* * * * * 2013,2014"))

    def testYearRange2(self):

        self.assertEqual(
            "At 12:23 PM, January through February, 2013 through 2014",
                         GetDescription("23 12 * JAN-FEB * 2013-2014"))

    def testYearRange3(self):

        self.assertEqual(
            "At 12:23 PM, January through March, 2013 through 2015",
                         GetDescription("23 12 * JAN-MAR * 2013-2015"))

    def testHourRange(self):

        self.assertEqual(
            "Every 30 minutes, between 08:00 AM and 09:59 AM, on day 5 and 20 of the month", GetDescription("0 0/30 8-9 5,20 * ?"))

    def testDayOfWeekModifier(self):

        self.assertEqual(
            "At 12:23 PM, on the second Sunday of the month", GetDescription("23 12 * * SUN#2"))

    def testDayOfWeekModifierWithSundayStartOne(self):

        options = Options()
        options.DayOfWeekStartIndexZero = False

        self.assertEqual(
            "At 12:23 PM, on the second Sunday of the month", GetDescription("23 12 * * 1#2", options))

    def testHourRangeWithEveryPortion(self):

        self.assertEqual(
            "At 25 minutes past the hour, every 13 hours, between 07:00 AM and 07:59 PM", GetDescription("0 25 7-19/13 ? * *"))

    def testHourRangeWithTrailingZeroWithEveryPortion(self):

        self.assertEqual(
            "At 25 minutes past the hour, every 13 hours, between 07:00 AM and 08:59 PM", GetDescription("0 25 7-20/13 ? * *"))

    def testEvery3Day(self):

        self.assertEqual(
            "At 08:00 AM, every 3 days",
            GetDescription("0 0 8 1/3 * ? *"))

    def testsEvery3DayOfTheWeek(self):

        self.assertEqual(
            "At 10:15 AM, every 3 days of the week",
            GetDescription("0 15 10 ? * */3"))

    def testEvery3Month(self):

        self.assertEqual(
            "At 07:05 AM, on day 2 of the month, every 3 months", GetDescription("0 5 7 2 1/3 ? *"))

    def testEvery2Years(self):

        self.assertEqual(
            "At 06:15 AM, on day 1 of the month, only in January, every 2 years", GetDescription("0 15 6 1 1 ? 1/2"))

    def testMutiPartRangeSeconds(self):

        self.assertEqual(
            "Minutes 2,4 through 05 past the hour, at 01:00 AM", GetDescription("2,4-5 1 * * *"))

    def testMutiPartRangeSeconds2(self):

        self.assertEqual(
            "Minutes 2,26 through 28 past the hour, at 06:00 PM", GetDescription("2,26-28 18 * * *"))
