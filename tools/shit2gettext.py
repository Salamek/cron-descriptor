from resx2dict import resx2dict
import os

class shit2gettext(object):
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

shit2gettext('Resources.resx', '../cron_descriptor/ExpressionDescriptor.py.resx','../cron_descriptor/ExpressionDescriptor.py', ['Resources'])
