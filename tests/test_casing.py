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

from cron_descriptor import CasingTypeEnum, DescriptionTypeEnum, ExpressionDescriptor, Options

"""
Tests casing transformation
"""

def test_sentence_casing(options: Options) -> None:
    options.casing_type = CasingTypeEnum.Sentence
    ceh = ExpressionDescriptor("* * * * *", options)
    assert ceh.get_description(DescriptionTypeEnum.FULL) == "Every minute"

def test_title_casing(options: Options) -> None:
    options.casing_type = CasingTypeEnum.Title
    ceh = ExpressionDescriptor("* * * * *", options)
    assert ceh.get_description(DescriptionTypeEnum.FULL) == "Every Minute"

def test_lower_casing(options: Options) -> None:
    options.casing_type = CasingTypeEnum.LowerCase
    ceh = ExpressionDescriptor("* * * * *", options)
    assert ceh.get_description(DescriptionTypeEnum.FULL) == "every minute"
