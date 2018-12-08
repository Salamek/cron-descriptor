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

from resx2dict import resx2dict
import os


class Shit2gettext(object):
    def __init__(self, resx, pyfile, pyfileo, resclasspath):
        if os.path.isfile(resx) is False:
            raise Exception("Resx file not found")

        if os.path.isfile(pyfile) is False:
            raise Exception("Pyfile not found")

        table = resx2dict(resx)

        f = open(pyfile,'r')
        filedata = f.read()
        f.close()

        for key in sorted(table, key=len, reverse=True):
            filedata = filedata.replace("{}.{}".format('.'.join(resclasspath), key), '_("{}")'.format(table[key]))

        f = open(pyfileo + '.new' if pyfileo == pyfile else pyfileo,'w')
        f.write(filedata)
        f.close()


Shit2gettext('Resources.resx', '../cron_descriptor/ExpressionDescriptor.py.resx','../cron_descriptor/ExpressionDescriptor.py', ['Resources'])
