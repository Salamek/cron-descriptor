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

import gettext
import os
import logging


logger = logging.getLogger(__name__)


class GetText(object):

    """
    Handles language translations and Initializes global _() function
    """

    def __init__(self, locale_code):
        """
        Initialize GetText
        :param locale_code selected locale
        """
        try:
            filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'locale', '{}.mo'.format(locale_code))
            trans = gettext.GNUTranslations(open(filename, "rb"))
            logger.debug('{} Loaded'.format(filename))
        except IOError:
            logger.debug('Failed to found locale {}'.format(locale_code))
            trans = gettext.NullTranslations()

        trans.install()
