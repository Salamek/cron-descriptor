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

import pytest

from cron_descriptor import DescriptionTypeEnum, ExpressionDescriptor, FormatException, MissingFieldException, Options

"""
Tests that Exceptions are/not properly raised
"""

def test_empty_cron_expression_exception(options: Options) -> None:
    with pytest.raises(MissingFieldException):
        ExpressionDescriptor("", options)

def test_invalid_cron_expression_exception(options: Options) -> None:
    with pytest.raises(FormatException):
        ExpressionDescriptor("INVALID", options)

def test_invalid_syntax_exception(options: Options) -> None:
    ceh = ExpressionDescriptor("* $ * * *", options)
    with pytest.raises(FormatException):
        ceh.get_description(DescriptionTypeEnum.FULL)

