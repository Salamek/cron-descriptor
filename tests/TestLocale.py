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
from cron_descriptor import Options, ExpressionDescriptor
from unittest.mock import patch
import tempfile
import shutil
import os
import logging


class TestLocale(TestCase.TestCase):

    def test_locale_de(self):
        options = Options()
        options.locale_code = 'de_DE'
        options.use_24hour_time_format = True
        self.assertEqual(
            "Jede Minute",
            ExpressionDescriptor("* * * * *", options).get_description())

    def test_locale_de_custom_location(self):
        logger = logging.getLogger('cron_descriptor.GetText')
        with patch.object(logger, "debug") as mock_logger:
            # Copy existing .mo file to temp directory:
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, 'de_DE.mo')
            shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../cron_descriptor/locale/', 'de_DE.mo'), temp_path)

            options = Options()
            options.locale_location = temp_dir
            options.locale_code = 'de_DE'
            options.use_24hour_time_format = True

            self.assertEqual("Jede Minute", ExpressionDescriptor("* * * * *", options).get_description())
            mock_logger.assert_called_once_with("{temp_path} Loaded".format(**{"temp_path":temp_path}))
