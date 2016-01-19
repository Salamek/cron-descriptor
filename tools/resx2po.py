from resx2dict import resx2dict
import os
import polib
import shutil

class resx2po(object):
    def __init__(self, resxen2name, resxlocale, potemplate, out):
        if os.path.isfile(resxen2name) is False:
            raise Exception("Resx bound not found")

        if os.path.isfile(resxlocale) is False:
            raise Exception("Resx trans not found")

        if os.path.isfile(potemplate) is False:
            raise Exception("PO template not found")

        bound = resx2dict(resxen2name)
        trans = resx2dict(resxlocale)

        motable = {}
        for boundk in sorted(bound, key=len, reverse=True):
            if boundk in trans:
                motable[bound[boundk]] = trans[boundk]
            else:
                print("WARNING: {} not found in {}, wont be added into motable".format(boundk, resxen2name))

        po = polib.pofile(potemplate)
        for entry in po:
            if entry.msgid in motable:
                entry.msgstr = motable[entry.msgid]
            else:
                print("WARNING: {} not found in {}".format(entry.msgid, 'motable'))

        po.save()
        shutil.copy2(potemplate, out)


directory = '../locale'
resx2po('Resources.resx', 'Resources.de.resx', 'messages.po', os.path.join(directory, 'de_DE.po'))
resx2po('Resources.resx', 'Resources.es.resx', 'messages.po', os.path.join(directory, 'es_ES.po'))
resx2po('Resources.resx', 'Resources.fr.resx', 'messages.po', os.path.join(directory, 'fr_FR.po'))
resx2po('Resources.resx', 'Resources.it.resx', 'messages.po', os.path.join(directory, 'it_IT.po'))
resx2po('Resources.resx', 'Resources.nl.resx', 'messages.po', os.path.join(directory, 'nl_NL.po'))
resx2po('Resources.resx', 'Resources.no.resx', 'messages.po', os.path.join(directory, 'nb_NO.po'))
resx2po('Resources.resx', 'Resources.pt.resx', 'messages.po', os.path.join(directory, 'pt_PT.po'))
resx2po('Resources.resx', 'Resources.ru.resx', 'messages.po', os.path.join(directory, 'ru_RU.po'))
resx2po('Resources.resx', 'Resources.tr.resx', 'messages.po', os.path.join(directory, 'tr_TR.po'))
resx2po('Resources.resx', 'Resources.uk.resx', 'messages.po', os.path.join(directory, 'uk_UA.po'))
resx2po('Resources.resx', 'Resources.zh-CHS.resx', 'messages.po', os.path.join(directory, 'zh_CN.po'))
