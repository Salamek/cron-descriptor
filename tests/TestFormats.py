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

import tests.TestCase as TestCase
from cron_descriptor import get_description


class TestFormats(TestCase.TestCase):

    """
    Tests formatted cron expressions
    """

    def test_every_minute(self):

        self.assertEqual("Every minute", get_description("* * * * *", self.options))

    def test_every1_minute(self):

        self.assertEqual("Every minute", get_description("*/1 * * * *", self.options))
        self.assertEqual("Every minute", get_description("0 0/1 * * * ?", self.options))

    def test_every_hour(self):

        self.assertEqual("Every hour", get_description("0 0 * * * ?", self.options))
        self.assertEqual("Every hour", get_description("0 0 0/1 * * ?", self.options))

    def test_time_of_day_certain_days_of_week(self):

        self.assertEqual(
            "At 11:00 PM, Monday through Friday",
            get_description("0 23 ? * MON-FRI", self.options))

    def test_every_second(self):

        self.assertEqual("Every second", get_description("* * * * * *", self.options))

    def test_every45_seconds(self):

        self.assertEqual("Every 45 seconds", get_description("*/45 * * * * *", self.options))

    def test_every5_minutes(self):

        self.assertEqual("Every 5 minutes", get_description("*/5 * * * *", self.options))
        self.assertEqual("Every 10 minutes", get_description("0 0/10 * * * ?", self.options))

    def test_every5_minutes_on_the_second(self):

        self.assertEqual("Every 5 minutes", get_description("0 */5 * * * *", self.options))

    def test_weekdays_at_time(self):

        self.assertEqual(
            "At 11:30 AM, Monday through Friday",
            get_description("30 11 * * 1-5", self.options))

    def test_daily_at_time(self):

        self.assertEqual("At 11:30 AM", get_description("30 11 * * *", self.options))

    def test_minute_span(self):

        self.assertEqual(
            "Every minute between 11:00 AM and 11:10 AM", get_description("0-10 11 * * *", self.options))

    def test_one_month_only(self):

        self.assertEqual(
            "Every minute, only in March",
            get_description("* * * 3 *", self.options))

    def test_two_months_only(self):

        self.assertEqual(
            "Every minute, only in March and June",
            get_description("* * * 3,6 *", self.options))

    def test_two_times_each_afternoon(self):

        self.assertEqual(
            "At 02:30 PM and 04:30 PM",
            get_description("30 14,16 * * *", self.options))

    def test_three_times_daily(self):

        self.assertEqual(
            "At 06:30 AM, 02:30 PM and 04:30 PM",
            get_description("30 6,14,16 * * *", self.options))

    def test_once_a_week(self):

        self.assertEqual(
            "At 09:46 AM, only on Monday",
            get_description("46 9 * * 1", self.options))

    def test_day_of_month(self):

        self.assertEqual(
            "At 12:23 PM, on day 15 of the month",
            get_description("23 12 15 * *", self.options))

    def test_month_name(self):

        self.assertEqual(
            "At 12:23 PM, only in January",
            get_description("23 12 * JAN *", self.options))

    def test_lowercase_month_name(self):

        self.assertEqual(
            "At 12:23 PM, only in January",
            get_description("23 12 * jan *", self.options))

    def test_day_of_month_with_question_mark(self):

        self.assertEqual(
            "At 12:23 PM, only in January",
            get_description("23 12 ? JAN *", self.options))

    def test_month_name_range2(self):

        self.assertEqual(
            "At 12:23 PM, January through February", get_description("23 12 * JAN-FEB *", self.options))

    def test_month_name_range3(self):

        self.assertEqual(
            "At 12:23 PM, January through March",
            get_description("23 12 * JAN-MAR *", self.options))

    def test_day_of_week_name(self):

        self.assertEqual(
            "At 12:23 PM, only on Sunday",
            get_description("23 12 * * SUN", self.options))

    def test_day_of_week_name_lowercase(self):

        self.assertEqual(
            "At 12:23 PM, only on Sunday",
            get_description("23 12 * * sun", self.options))

    def test_day_of_week_range(self):

        self.assertEqual(
            "Every 5 minutes, between 03:00 PM and 03:59 PM, Monday through Friday", get_description("*/5 15 * * MON-FRI", self.options))

    def test_day_of_week_range_lowercase(self):

        self.assertEqual(
            "Every 5 minutes, between 03:00 PM and 03:59 PM, Monday through Friday", get_description("*/5 15 * * MoN-fri", self.options))

    def test_day_of_week_once_in_month(self):

        self.assertEqual(
            "Every minute, on the third Monday of the month", get_description("* * * * MON#3", self.options))

    def test_last_day_of_the_week_of_the_month(self):

        self.assertEqual(
            "Every minute, on the last Thursday of the month", get_description("* * * * 4L", self.options))

    def test_last_day_of_the_month(self):

        self.assertEqual(
            "Every 5 minutes, on the last day of the month, only in January", get_description(
                "*/5 * L JAN *",
                self.options
            )
        )

    def test_last_day_offset(self):

        self.assertEqual(
            "At 12:00 AM, 5 days before the last day of the month", get_description(
                "0 0 0 L-5 * ?",
                self.options
            )
        )

    def test_last_weekday_of_the_month(self):

        self.assertEqual(
            "Every minute, on the last weekday of the month", get_description("* * LW * *", self.options))

    def test_last_weekday_of_the_month2(self):

        self.assertEqual(
            "Every minute, on the last weekday of the month", get_description("* * WL * *", self.options))

    def test_first_weekday_of_the_month(self):

        self.assertEqual(
            "Every minute, on the first weekday of the month", get_description("* * 1W * *", self.options))

    def test_thirteenth_weekday_of_the_month(self):

        self.assertEqual(
            "Every minute, on the weekday nearest day 13 of the month", get_description("* * 13W * *", self.options))

    def test_first_weekday_of_the_month2(self):

        self.assertEqual(
            "Every minute, on the first weekday of the month", get_description("* * W1 * *", self.options))

    def test_particular_weekday_of_the_month(self):

        self.assertEqual(
            "Every minute, on the weekday nearest day 5 of the month", get_description("* * 5W * *", self.options))

    def test_particular_weekday_of_the_month2(self):

        self.assertEqual(
            "Every minute, on the weekday nearest day 5 of the month", get_description("* * W5 * *", self.options))

    def test_time_of_day_with_seconds(self):

        self.assertEqual("At 02:02:30 PM", get_description("30 02 14 * * *", self.options))

    def test_second_intervals(self):

        self.assertEqual(
            "Seconds 5 through 10 past the minute",
            get_description("5-10 * * * * *", self.options))

    def test_multi_part_second(self):
        self.assertEqual(
            "At 15 and 45 seconds past the minute",
            get_description("15,45 * * * * *", self.options)
        )

    def test_second_minutes_hours_intervals(self):

        self.assertEqual((
            "Seconds 5 through 10 past the minute, "
            "minutes 30 through 35 past the hour, "
            "between 10:00 AM and 12:59 PM"), get_description("5-10 30-35 10-12 * * *", self.options))

    def test_every5_minutes_at30_seconds(self):

        self.assertEqual(
            "At 30 seconds past the minute, every 5 minutes", get_description("30 */5 * * * *", self.options))

    def test_minutes_past_the_hour_range(self):

        self.assertEqual((
            "At 30 minutes past the hour, "
            "between 10:00 AM and 01:59 PM, "
            "only on Wednesday and Friday"), get_description("0 30 10-13 ? * WED,FRI", self.options))

    def test_seconds_past_the_minute_interval(self):

        self.assertEqual(
            "At 10 seconds past the minute, every 5 minutes",
            get_description("10 0/5 * * * ?", self.options)
        )

    def test_between_with_interval(self):

        self.assertEqual(
            ("Every 3 minutes, minutes 2 through 59 past the hour, "
             "at 01:00 AM, 09:00 AM, and 10:00 PM, between day 11 and 26 of the month, "
             "January through June"), get_description("2-59/3 1,9,22 11-26 1-6 ?", self.options))

    def test_recurring_first_of_month(self):

        self.assertEqual("At 06:00 AM", get_description("0 0 6 1/1 * ?", self.options))

    def test_minutes_past_the_hour(self):

        self.assertEqual(
            "At 5 minutes past the hour",
            get_description("0 5 0/1 * * ?", self.options)
        )

    def test_one_year_only_with_seconds(self):

        self.assertEqual(
            "Every second, only in 2013",
            get_description("* * * * * * 2013", self.options))

    def test_one_year_only_without_seconds(self):

        self.assertEqual(
            "Every minute, only in 2013",
            get_description("* * * * * 2013", self.options))

    def test_two_years_only(self):

        self.assertEqual(
            "Every minute, only in 2013 and 2014", get_description("* * * * * 2013,2014", self.options))

    def test_year_range2(self):

        self.assertEqual(
            "At 12:23 PM, January through February, 2013 through 2014", get_description(
                "23 12 * JAN-FEB * 2013-2014",
                self.options
            )
        )

    def test_year_range3(self):

        self.assertEqual(
            "At 12:23 PM, January through March, 2013 through 2015", get_description(
                "23 12 * JAN-MAR * 2013-2015",
                self.options
            )
        )

    def test_hour_range(self):

        self.assertEqual((
            "Every 30 minutes, between 08:00 AM and 09:59 AM, "
            "on day 5 and 20 of the month"), get_description("0 0/30 8-9 5,20 * ?", self.options))

    def test_day_of_week_modifier(self):

        self.assertEqual(
            "At 12:23 PM, on the second Sunday of the month", get_description("23 12 * * SUN#2", self.options))

    def test_day_of_week_modifier_with_sunday_start_one(self):

        self.options.day_of_week_start_index_zero = False

        self.assertEqual(
            "At 12:23 PM, on the second Sunday of the month", get_description("23 12 * * 1#2", self.options))

    def test_hour_range_with_every_portion(self):

        self.assertEqual((
            "At 25 minutes past the hour, every 8 hours, "
            "between 07:00 AM and 07:59 PM"), get_description("0 25 7-19/8 ? * *", self.options))

    def test_hour_range_with_trailing_zero_with_every_portion(self):

        self.assertEqual((
            "At 25 minutes past the hour, every 13 hours, "
            "between 07:00 AM and 08:59 PM"), get_description("0 25 7-20/13 ? * *", self.options))

    def test_every3_day(self):

        self.assertEqual(
            "At 08:00 AM, every 3 days",
            get_description("0 0 8 1/3 * ? *", self.options))

    def tests_every3_day_of_the_week(self):

        self.assertEqual(
            "At 10:15 AM, every 3 days of the week",
            get_description("0 15 10 ? * */3", self.options))

    def test_every_2_day_of_the_week_in_range(self):
        self.assertEqual(
            "Every second, every 2 days of the week, Monday through Friday",
            get_description("* * * ? * 1-5/2", self.options))

    def test_every_2_day_of_the_week_in_range_with_sunday_start_one(self):
        self.options.day_of_week_start_index_zero = False

        self.assertEqual(
            "Every second, every 2 days of the week, Monday through Friday",
            get_description("* * * ? * 2-6/2", self.options))

    def test_multi_with_day_of_week_start_index_zero_false(self):
        self.options.day_of_week_start_index_zero = False

        self.assertEqual(
            "Every second, only on Sunday, Monday, and Tuesday",
            get_description("* * * ? * 1,2,3", self.options)
        )

    def test_every3_month(self):

        self.assertEqual(
            "At 07:05 AM, on day 2 of the month, every 3 months", get_description("0 5 7 2 1/3 ? *", self.options))

    def test_every2_years(self):

        self.assertEqual(
            "At 06:15 AM, on day 1 of the month, only in January, every 2 years", get_description(
                "0 15 6 1 1 ? 1/2",
                self.options
            )
        )

    def test_multi_part_range_minutes(self):
        self.assertEqual(
            "At 2 and 4 through 5 minutes past the hour, at 01:00 AM", get_description("2,4-5 1 * * *", self.options))

    def test_multi_part_range_minutes_2(self):
        self.assertEqual(
            "At 2 and 26 through 28 minutes past the hour, at 06:00 PM", get_description(
                "2,26-28 18 * * *",
                self.options
            )
        )

    def test_trailing_space_does_not_cause_a_wrong_description(self):
        self.assertEqual(
            "At 07:00 AM", get_description("0 7 * * * ", self.options))

    def test_multi_part_day_of_the_week(self):
        self.assertEqual(
            "At 10:00 AM, only on Monday through Thursday and Sunday",
            get_description("0 00 10 ? * MON-THU,SUN *")
        )

    def test_day_of_week_with_day_of_month(self):
        self.assertEqual(
            "At 12:00 AM, on day 1, 2, and 3 of the month, only on Wednesday and Friday",
            get_description("0 0 0 1,2,3 * WED,FRI", self.options)
        )

    def test_seconds_interval_with_step_value(self):
        self.assertEqual(
            "Every 30 seconds, starting at 5 seconds past the minute",
            get_description("5/30 * * * * ?", self.options))

    def test_minutes_interval_with_step_value(self):
        self.assertEqual(
            "Every 30 minutes, starting at 5 minutes past the hour",
            get_description("0 5/30 * * * ?", self.options))

    def test_hours_interval_with_step_value(self):
        self.assertEqual(
            "Every second, every 8 hours, starting at 05:00 AM",
            get_description("* * 5/8 * * ?", self.options))

    def test_day_of_month_interval_with_step_value(self):
        self.assertEqual(
            "At 07:05 AM, every 3 days, starting on day 2 of the month",
            get_description("0 5 7 2/3 * ? *", self.options))

    def test_month_interval_with_step_value(self):
        self.assertEqual(
            "At 07:05 AM, every 2 months, March through December",
            get_description("0 5 7 ? 3/2 ? *", self.options))

    def test_day_of_week_interval_with_step_value(self):
        self.assertEqual(
            "At 07:05 AM, every 3 days of the week, Tuesday through Saturday",
            get_description("0 5 7 ? * 2/3 *", self.options))

    def test_year_interval_with_step_value(self):
        self.assertEqual(
            "At 07:05 AM, every 4 years, 2016 through 9999",
            get_description("0 5 7 ? * ? 2016/4", self.options))

    def test_minutes_combined_with_multiple_hour_ranges(self):
        self.assertEqual(
            "At 1 minutes past the hour, at 01:00 AM and 03:00 AM through 04:59 AM",
            get_description("1 1,3-4 * * *", self.options))


    def test_minute_range_conbined_with_second_range(self):
        self.assertEqual(
            "Seconds 12 through 50 past the minute, minutes 0 through 10 past the hour, at 06:00 AM, only in 2022",
            get_description("12-50 0-10 6 * * * 2022", self.options)
        )


    def test_seconds_expression_combined_with_hours_list_and_single_minute(self):
        self.assertEqual(
            "At 5 seconds past the minute, at 30 minutes past the hour, at 06:00 AM, 02:00 PM, and 04:00 PM, on day 5 of the month",
            get_description("5 30 6,14,16 5 * *", self.options)
        )


    def test_minute_range_with_interval(self):
        self.assertEqual(
            "Every 3 minutes, minutes 0 through 20 past the hour, between 09:00 AM and 09:59 AM",
            get_description("0-20/3 9 * * *", self.options)
        )

    def minutes_zero_1(self):
        self.assertEqual(
            "Every second, at 0 minutes past the hour, every 4 hours",
            get_description("* 0 */4 * * *", self.options)
        )

    def minutes_zero_2(self):
        self.assertEqual(
            "Every 10 seconds, at 0 minutes past the hour",
            get_description("*/10 0 * * * *", self.options)
        )

    def minutes_zero_3(self):
        self.assertEqual(
            "Every second, at 0 minutes past the hour, between 12:00 AM and 12:59 AM",
            get_description("* 0 0 * * *", self.options)
        )

    def minutes_zero_4(self):
        self.assertEqual(
            "Every minute, between 12:00 AM and 12:59 AM",
            get_description("* 0 * * *", self.options)
        )

    def minutes_zero_5(self):
        self.assertEqual(
            "Every second, at 0 minutes past the hour",
            get_description("* 0 * * * *", self.options)
        )

    def sunday_7(self):
        self.assertEqual(
            "At 09:00 AM, only on Sunday",
            get_description("0 0 9 ? * 7", self.options)
        )

    def every_year(self):
        self.assertEqual(
            "Every 10 minutes, Monday through Friday",
            get_description("0/10 * ? * MON-FRI *", self.options)
        )
