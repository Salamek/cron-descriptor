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

from cron_descriptor import Options, get_description

"""
Tests formatted cron expressions
"""

def test_every_minute(options: Options) -> None:
    assert get_description("* * * * *", options) == "Every minute"

def test_every1_minute(options: Options) -> None:
    assert get_description("*/1 * * * *", options) == "Every minute"
    assert get_description("0 0/1 * * * ?", options) == "Every minute"

def test_every_hour(options: Options) -> None:
    assert get_description("0 0 * * * ?", options) == "Every hour"
    assert get_description("0 0 0/1 * * ?", options) == "Every hour"

def test_time_of_day_certain_days_of_week(options: Options) -> None:
    assert get_description("0 23 ? * MON-FRI", options) == "At 11:00 PM, Monday through Friday"

def test_every_second(options: Options) -> None:
    assert get_description("* * * * * *", options) == "Every second"

def test_every45_seconds(options: Options) -> None:
    assert get_description("*/45 * * * * *", options) == "Every 45 seconds"

def test_every5_minutes(options: Options) -> None:
    assert get_description("*/5 * * * *", options) == "Every 5 minutes"
    assert get_description("0 0/10 * * * ?", options) == "Every 10 minutes"

def test_every5_minutes_on_the_second(options: Options) -> None:
    assert get_description("0 */5 * * * *", options) == "Every 5 minutes"

def test_weekdays_at_time(options: Options) -> None:
    assert get_description("30 11 * * 1-5", options) == "At 11:30 AM, Monday through Friday"

def test_daily_at_time(options: Options) -> None:
    assert get_description("30 11 * * *", options) == "At 11:30 AM"

def test_minute_span(options: Options) -> None:
    assert get_description("0-10 11 * * *", options) == "Every minute between 11:00 AM and 11:10 AM"

def test_one_month_only(options: Options) -> None:
    assert get_description("* * * 3 *", options) == "Every minute, only in March"

def test_two_months_only(options: Options) -> None:
    assert get_description("* * * 3,6 *", options) == "Every minute, only in March and June"

def test_two_times_each_afternoon(options: Options) -> None:
    assert get_description("30 14,16 * * *", options) == "At 02:30 PM and 04:30 PM"

def test_three_times_daily(options: Options) -> None:
    assert get_description("30 6,14,16 * * *", options) == "At 06:30 AM, 02:30 PM and 04:30 PM"

def test_once_a_week(options: Options) -> None:
    assert get_description("46 9 * * 1", options) == "At 09:46 AM, only on Monday"

def test_day_of_month(options: Options) -> None:
    assert get_description("23 12 15 * *", options) == "At 12:23 PM, on day 15 of the month"

def test_month_name(options: Options) -> None:
    assert get_description("23 12 * JAN *", options) == "At 12:23 PM, only in January"

def test_lowercase_month_name(options: Options) -> None:
    assert get_description("23 12 * jan *", options) == "At 12:23 PM, only in January"

def test_day_of_month_with_question_mark(options: Options) -> None:
    assert get_description("23 12 ? JAN *", options) == "At 12:23 PM, only in January"

def test_month_name_range2(options: Options) -> None:
    assert get_description("23 12 * JAN-FEB *", options) == "At 12:23 PM, January through February"

def test_month_name_range3(options: Options) -> None:
    assert get_description("23 12 * JAN-MAR *", options) == "At 12:23 PM, January through March"

def test_day_of_week_name(options: Options) -> None:
    assert get_description("23 12 * * SUN", options) == "At 12:23 PM, only on Sunday"

def test_day_of_week_name_lowercase(options: Options) -> None:
    assert get_description("23 12 * * sun", options) == "At 12:23 PM, only on Sunday"

def test_day_of_week_range(options: Options) -> None:
    assert get_description("*/5 15 * * MON-FRI", options) == "Every 5 minutes, between 03:00 PM and 03:59 PM, Monday through Friday"

def test_day_of_week_range_lowercase(options: Options) -> None:
    assert get_description("*/5 15 * * MoN-fri", options) == "Every 5 minutes, between 03:00 PM and 03:59 PM, Monday through Friday"

def test_day_of_week_once_in_month(options: Options) -> None:
    assert get_description("* * * * MON#3", options) == "Every minute, on the third Monday of the month"

def test_last_day_of_the_week_of_the_month(options: Options) -> None:
    assert get_description("* * * * 4L", options) == "Every minute, on the last Thursday of the month"

def test_last_day_of_the_month(options: Options) -> None:
    assert get_description(
        "*/5 * L JAN *",
        options,
    ) == "Every 5 minutes, on the last day of the month, only in January"

def test_last_day_offset(options: Options) -> None:
    assert get_description(
        "0 0 0 L-5 * ?",
        options,
    ) == "At 12:00 AM, 5 days before the last day of the month"


def test_last_weekday_of_the_month(options: Options) -> None:
    assert get_description("* * LW * *", options) == "Every minute, on the last weekday of the month"

def test_last_weekday_of_the_month2(options: Options) -> None:
    assert get_description("* * WL * *", options) == "Every minute, on the last weekday of the month"

def test_first_weekday_of_the_month(options: Options) -> None:
    assert get_description("* * 1W * *", options) == "Every minute, on the first weekday of the month"

def test_thirteenth_weekday_of_the_month(options: Options) -> None:
    assert get_description("* * 13W * *", options) == "Every minute, on the weekday nearest day 13 of the month"

def test_first_weekday_of_the_month2(options: Options) -> None:
    assert get_description("* * W1 * *", options) == "Every minute, on the first weekday of the month"

def test_particular_weekday_of_the_month(options: Options) -> None:
    assert get_description("* * 5W * *", options) == "Every minute, on the weekday nearest day 5 of the month"

def test_particular_weekday_of_the_month2(options: Options) -> None:
    assert get_description("* * W5 * *", options) == "Every minute, on the weekday nearest day 5 of the month"

def test_time_of_day_with_seconds(options: Options) -> None:
    assert get_description("30 02 14 * * *", options) == "At 02:02:30 PM"

def test_second_intervals(options: Options) -> None:
    assert get_description("5-10 * * * * *", options) == "Seconds 5 through 10 past the minute"

def test_multi_part_second(options: Options) -> None:
    assert get_description("15,45 * * * * *", options) == "At 15 and 45 seconds past the minute"


def test_second_minutes_hours_intervals(options: Options) -> None:
    assert get_description("5-10 30-35 10-12 * * *", options) == (
        "Seconds 5 through 10 past the minute, "
        "minutes 30 through 35 past the hour, "
        "between 10:00 AM and 12:59 PM")

def test_every5_minutes_at30_seconds(options: Options) -> None:
    assert get_description("30 */5 * * * *", options) == "At 30 seconds past the minute, every 5 minutes"

def test_minutes_past_the_hour_range(options: Options) -> None:
    assert get_description("0 30 10-13 ? * WED,FRI", options) == (
        "At 30 minutes past the hour, "
        "between 10:00 AM and 01:59 PM, "
        "only on Wednesday and Friday")

def test_seconds_past_the_minute_interval(options: Options) -> None:
    assert get_description("10 0/5 * * * ?", options) == "At 10 seconds past the minute, every 5 minutes"


def test_between_with_interval(options: Options) -> None:

    assert get_description("2-59/3 1,9,22 11-26 1-6 ?", options) == ("Every 3 minutes, minutes 2 through 59 past the hour, "
         "at 01:00 AM, 09:00 AM, and 10:00 PM, between day 11 and 26 of the month, "
         "January through June")

def test_recurring_first_of_month(options: Options) -> None:
    assert get_description("0 0 6 1/1 * ?", options) == "At 06:00 AM"

def test_minutes_past_the_hour(options: Options) -> None:
    assert get_description("0 5 0/1 * * ?", options) == "At 5 minutes past the hour"


def test_one_year_only_with_seconds(options: Options) -> None:
    assert get_description("* * * * * * 2013", options) == "Every second, only in 2013"

def test_one_year_only_without_seconds(options: Options) -> None:
    assert get_description("* * * * * 2013", options) == "Every minute, only in 2013"

def test_two_years_only(options: Options) -> None:
    assert get_description("* * * * * 2013,2014", options) == "Every minute, only in 2013 and 2014"

def test_year_range2(options: Options) -> None:
    assert get_description(
        "23 12 * JAN-FEB * 2013-2014",
        options,
    ) == "At 12:23 PM, January through February, 2013 through 2014"


def test_year_range3(options: Options) -> None:
    assert get_description(
        "23 12 * JAN-MAR * 2013-2015",
        options,
    ) == "At 12:23 PM, January through March, 2013 through 2015"


def test_hour_range(options: Options) -> None:
    assert get_description("0 0/30 8-9 5,20 * ?", options) == ("Every 30 minutes, between 08:00 AM and 09:59 AM, "
        "on day 5 and 20 of the month")

def test_day_of_week_modifier(options: Options) -> None:
    assert get_description("23 12 * * SUN#2", options) == "At 12:23 PM, on the second Sunday of the month"

def test_day_of_week_modifier_with_sunday_start_one(options: Options) -> None:

    options.day_of_week_start_index_zero = False
    assert get_description("23 12 * * 1#2", options) == "At 12:23 PM, on the second Sunday of the month"

def test_hour_range_with_every_portion(options: Options) -> None:
    assert get_description("0 25 7-19/8 ? * *", options) == (
        "At 25 minutes past the hour, every 8 hours, "
        "between 07:00 AM and 07:59 PM")

def test_hour_range_with_trailing_zero_with_every_portion(options: Options) -> None:
    assert get_description("0 25 7-20/13 ? * *", options) == (
        "At 25 minutes past the hour, every 13 hours, "
        "between 07:00 AM and 08:59 PM")

def test_every3_day(options: Options) -> None:
    assert get_description("0 0 8 1/3 * ? *", options) == "At 08:00 AM, every 3 days"

def tests_every3_day_of_the_week(options: Options) -> None:
    assert get_description("0 15 10 ? * */3", options) == "At 10:15 AM, every 3 days of the week"

def test_every_7_day_of_the_week(options: Options) -> None:
    assert get_description("0 * * * */7", options) == "Every hour, every 7 days of the week"

def test_every_2_day_of_the_week_in_range(options: Options) -> None:
    assert get_description("* * * ? * 1-5/2", options) == "Every second, every 2 days of the week, Monday through Friday"

def test_every_2_day_of_the_week_in_range_with_sunday_start_one(options: Options) -> None:
    options.day_of_week_start_index_zero = False
    assert get_description("* * * ? * 2-6/2", options) == "Every second, every 2 days of the week, Monday through Friday"

def test_multi_with_day_of_week_start_index_zero_false(options: Options) -> None:
    options.day_of_week_start_index_zero = False

    assert get_description("* * * ? * 1,2,3", options) == "Every second, only on Sunday, Monday, and Tuesday"

def test_every3_month(options: Options) -> None:
    assert get_description("0 5 7 2 1/3 ? *", options) == "At 07:05 AM, on day 2 of the month, every 3 months"

def test_every2_years(options: Options) -> None:
    assert get_description(
        "0 15 6 1 1 ? 1/2",
        options,
    ) == "At 06:15 AM, on day 1 of the month, only in January, every 2 years"


def test_multi_part_range_minutes(options: Options) -> None:
    assert get_description("2,4-5 1 * * *", options) == "At 2 and 4 through 5 minutes past the hour, at 01:00 AM"

def test_multi_part_range_minutes_2(options: Options) -> None:
    assert get_description(
        "2,26-28 18 * * *",
        options,
    ) == "At 2 and 26 through 28 minutes past the hour, at 06:00 PM"


def test_trailing_space_does_not_cause_a_wrong_description(options: Options) -> None:
    assert get_description("0 7 * * * ", options) == "At 07:00 AM"

def test_multi_part_day_of_the_week() -> None:
    assert get_description("0 00 10 ? * MON-THU,SUN *") == "At 10:00 AM, only on Monday through Thursday and Sunday"


def test_day_of_week_with_day_of_month(options: Options) -> None:
    assert get_description("0 0 0 1,2,3 * WED,FRI", options) == "At 12:00 AM, on day 1, 2, and 3 of the month, only on Wednesday and Friday"


def test_seconds_interval_with_step_value(options: Options) -> None:
    assert get_description("5/30 * * * * ?", options) == "Every 30 seconds, starting at 5 seconds past the minute"

def test_minutes_interval_with_step_value(options: Options) -> None:
    assert get_description("0 5/30 * * * ?", options) == "Every 30 minutes, starting at 5 minutes past the hour"

def test_hours_interval_with_step_value(options: Options) -> None:
    assert get_description("* * 5/8 * * ?", options) == "Every second, every 8 hours, starting at 05:00 AM"

def test_day_of_month_interval_with_step_value(options: Options) -> None:
    assert get_description("0 5 7 2/3 * ? *", options) == "At 07:05 AM, every 3 days, starting on day 2 of the month"

def test_month_interval_with_step_value(options: Options) -> None:
    assert get_description("0 5 7 ? 3/2 ? *", options) == "At 07:05 AM, every 2 months, March through December"

def test_day_of_week_interval_with_step_value(options: Options) -> None:
    assert get_description("0 5 7 ? * 2/3 *", options) == "At 07:05 AM, every 3 days of the week, Tuesday through Saturday"

def test_year_interval_with_step_value(options: Options) -> None:
    assert get_description("0 5 7 ? * ? 2016/4", options) == "At 07:05 AM, every 4 years, 2016 through 9999"

def test_minutes_combined_with_multiple_hour_ranges(options: Options) -> None:
    assert get_description("1 1,3-4 * * *", options) == "At 1 minutes past the hour, at 01:00 AM and 03:00 AM through 04:59 AM"


def test_minute_range_conbined_with_second_range(options: Options) -> None:
    assert get_description("12-50 0-10 6 * * * 2022", options) == "Seconds 12 through 50 past the minute, minutes 0 through 10 past the hour, at 06:00 AM, only in 2022"


def test_seconds_expression_combined_with_hours_list_and_single_minute(options: Options) -> None:
    assert get_description("5 30 6,14,16 5 * *", options) == "At 5 seconds past the minute, at 30 minutes past the hour, at 06:00 AM, 02:00 PM, and 04:00 PM, on day 5 of the month"


def test_minute_range_with_interval(options: Options) -> None:
    assert get_description("0-20/3 9 * * *", options) == "Every 3 minutes, minutes 0 through 20 past the hour, between 09:00 AM and 09:59 AM"

def minutes_zero_1(options: Options) -> None:
    assert get_description("* 0 */4 * * *", options) == "Every second, at 0 minutes past the hour, every 4 hours"


def minutes_zero_2(options: Options) -> None:
    assert get_description("*/10 0 * * * *", options) == "Every 10 seconds, at 0 minutes past the hour"

def minutes_zero_3(options: Options) -> None:
    assert get_description("* 0 0 * * *", options) == "Every second, at 0 minutes past the hour, between 12:00 AM and 12:59 AM"


def minutes_zero_4(options: Options) -> None:
    assert get_description("* 0 * * *", options) == "Every minute, between 12:00 AM and 12:59 AM"


def minutes_zero_5(options: Options) -> None:
    assert get_description("* 0 * * * *",options) == "Every second, at 0 minutes past the hour"


def sunday_7(options: Options) -> None:
    assert get_description("0 0 9 ? * 7", options) == "At 09:00 AM, only on Sunday"


def every_year(options: Options) -> None:
    assert get_description("0/10 * ? * MON-FRI *", options) == "Every 10 minutes, Monday through Friday"

