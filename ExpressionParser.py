
class ExpressionParser(object):
    m_expression = ''
    m_options = None #Options Class
    m_en_culture = None #CultureInfo Class

    """
    Initializes a new instance of the <see cref="ExpressionParser"/> class
    @param: expression The cron expression string
    @param: options Parsing options
    """
    def __init__(self, expression, options):
        self.m_expression = expression
        self.m_options = options
        self.m_en_culture = CultureInfo("en-US") #Default to English

    """
    Parses the cron expression string
    @returns: A 7 part string array, one part for each component of the cron expression (seconds, minutes, etc.)
    """
    def Parse(self):
        # Initialize all elements of parsed array to empty strings
        parsed = ['', '', '', '', '', '']

        if self.m_expression not in parsed:
            #raise MissingFieldException("ExpressionDescriptor", "expression") #FIXME
            raise Exception("ExpressionDescriptor")
        else:
            expressionPartsTemp = self.m_expression.split(' ')
            expressionPartsTempLength = len(expressionPartsTemp)
            if expressionPartsTempLength < 5:
                #throw new FormatException(string.Format("Error: Expression only has {0} parts.  At least 5 part are required.", expressionPartsTemp.Length));
                raise Exception("Error: Expression only has {0} parts.  At least 5 part are required.".format(expressionPartsTempLength))
            elif expressionPartsTempLength == 5:
                #5 part cron so shift array past seconds element
                parsed.insert(0, expressionPartsTemp)
            elif expressionPartsTempLength == 6:
                #If last element ends with 4 digits, a year element has been supplied and no seconds element
                yearRegex = re.compile("\\d{4}$")
                if prog.match(expressionPartsTemp[5]):
                    parsed.insert(1, expressionPartsTemp)
                else:
                    parsed.insert(0, expressionPartsTemp)
            elif expressionPartsTemp == 7:
                parsed = expressionPartsTemp
            else:
                #throw new FormatException(string.Format("Error: Expression has too many parts ({0}).  Expression must not have more than 7 parts.", expressionPartsTemp.Length));
                raise Exception("Error: Expression has too many parts ({0}).  Expression must not have more than 7 parts.".format(expressionPartsTemp.Length))

        self.NormalizeExpression(parsed);

        return parsed;

    """
    Converts cron expression components into consistent, predictable formats.
    @param: expressionParts A 7 part string array, one part for each component of the cron expression
    """

    def NormalizeExpression(self, expressionParts):
        #convert ? to * only for DOM and DOW
        expressionParts[3] = expressionParts[3].replace("?", "*")
        expressionParts[5] = expressionParts[5].replace("?", "*")

        #convert 0/, 1/ to */
        if expressionParts[0].startswith("0/"):
            expressionParts[0] = expressionParts[0].replace("0/", "*/") #seconds

        if expressionParts[1].startswith("0/"):
            expressionParts[1] = expressionParts[1].replace("0/", "*/") #minutes

        if expressionParts[2].startswith("0/"):
            expressionParts[2] = expressionParts[2].replace("0/", "*/") #hours

        if expressionParts[3].startswith("1/"):
            expressionParts[3] = expressionParts[3].replace("1/", "*/") #DOM

        if expressionParts[4].startswith("1/"):
            expressionParts[4] = expressionParts[4].replace("1/", "*/") #Month

        if expressionParts[5].startswith("1/"):
            expressionParts[5] = expressionParts[5].replace("1/", "*/") #DOW

        #convert */1 to *
        length = len(expressionParts)
        for i in range(0, length):
            if expressionParts[i] == "*/1":
                expressionParts[i] = "*"

        #handle DayOfWeekStartIndexZero option where SUN=1 rather than SUN=0
        if self.m_options.DayOfWeekStartIndexZero is False:
            length = len(expressionParts[5])
            for i in range(0, length):
                if i == 0 or dowChars[i - 1] != '#':
                    try:
                        charNumeric = int(string)
                        expressionParts[5][i] = str(charNumeric - 1)[0]
                    except ValueError:
                        pass

        #convert SUN-SAT format to 0-6 format
        for i in range(0, 6):
            expressionParts[5] = expressionParts[5].replace(NumberToDay(i), str(i))

        #convert JAN-DEC format to 1-12 format
        for i in range(0, 12):
            expressionParts[4] = expressionParts[4].replace(NumberToMonth(i), str(i))

        #convert 0 second to (empty)
        if expressionParts[0] == "0":
            expressionParts[0] = ''
