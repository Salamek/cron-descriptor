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
from cron_descriptor.ExpressionDescriptor import ExpressionDescriptor
from cron_descriptor.Exception import MissingFieldException, FormatException


class TestExceptions(TestCase.TestCase):
    def testNullCronExpressionException(self):
        options = Options()
        options.ThrowExceptionOnParseError = True
        ceh = ExpressionDescriptor(None, options)
        self.assertRaises(MissingFieldException, ceh.GetDescription, DescriptionTypeEnum.FULL)

    def testEmptyCronExpressionException(self):
        options = Options()
        options.ThrowExceptionOnParseError = True
        ceh = ExpressionDescriptor('', options)
        self.assertRaises(MissingFieldException, ceh.GetDescription, DescriptionTypeEnum.FULL)

    def testNullCronExpressionError(self):
        options = Options()
        options.ThrowExceptionOnParseError = False
        ceh = ExpressionDescriptor(None, options)
        self.assertEqual("Field 'ExpressionDescriptor.expression' not found.", ceh.GetDescription(DescriptionTypeEnum.FULL))

    def testInvalidCronExpressionException(self):
        options = Options()
        options.ThrowExceptionOnParseError = True
        ceh = ExpressionDescriptor("INVALID", options)
        self.assertRaises(FormatException, ceh.GetDescription, DescriptionTypeEnum.FULL)


    def testInvalidCronExpressionError(self):
        options = Options()
        options.ThrowExceptionOnParseError = False
        ceh = ExpressionDescriptor("INVALID CRON", options)
        self.assertEqual("Error: Expression only has 2 parts.  At least 5 part are required.", ceh.GetDescription(DescriptionTypeEnum.FULL))

    def TestInvalidSyntaxException(self):
        options = Options()
        options.ThrowExceptionOnParseError = True
        ceh = ExpressionDescriptor("* $ * * *", options)
        self.assertRaises(FormatException, ceh.GetDescription, DescriptionTypeEnum.FULL)
