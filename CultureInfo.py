class CultureInfo(object):
    def __init__(self, code = "en-US"):
        pass

    def getCode(self):
        code, encoding = locale.getdefaultlocale()
        return code
