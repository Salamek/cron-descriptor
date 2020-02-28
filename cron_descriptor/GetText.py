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

import gettext
import os
import logging


logger = logging.getLogger(__name__)


class GetText(object):

    """
    Handles language translations and Initializes global _() function
    """

    def __init__(self, locale_code, install=True):
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
            logger.debug('Failed to find locale {}'.format(locale_code))
            trans = gettext.NullTranslations()

        if install:
            trans.install()
        self.trans = trans
