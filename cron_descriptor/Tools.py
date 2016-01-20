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

from .Exception import WrongArgumentException


def number_to_day(day_number):
    """Returns day name by its number

    Args:
        day_number: Number of a day
    Returns:
        Day corresponding to day_number
    Raises:
        IndexError: When day_numer is not found
    """
    return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][day_number]


def number_to_month(month_number):
    """Returns month name by its number

    Args:
        month_number: Number of a month
    Returns:
        Month corresponding to day_number
    Raises:
        IndexError: When month_number is not found
        WrongArgumentException: When month number is 0
    """

    if month_number == 0:
        raise WrongArgumentException('There is no month 0')

    return ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][month_number]
