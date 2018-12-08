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


class TestImport(TestCase.TestCase):

    """
    Tests that inline and separated imports are working
    """

    def test_inline_import(self):
        from cron_descriptor import Options, DescriptionTypeEnum, ExpressionDescriptor
        options = Options()
        options.use_24hour_time_format = True
        options.locale_code = self.options.locale_code
        ceh = ExpressionDescriptor("* * * * *", options)
        self.assertEqual(
            "Every minute",
            ceh.get_description(DescriptionTypeEnum.FULL))

    def test_full_import(self):
        from cron_descriptor.Options import Options
        from cron_descriptor.DescriptionTypeEnum import DescriptionTypeEnum
        from cron_descriptor.ExpressionDescriptor import ExpressionDescriptor

        options = Options()
        options.use_24hour_time_format = True
        options.locale_code = self.options.locale_code
        ceh = ExpressionDescriptor("* * * * *", options)
        self.assertEqual(
            'Every minute',
            ceh.get_description(DescriptionTypeEnum.FULL))
