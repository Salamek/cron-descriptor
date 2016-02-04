#!/usr/bin/env python3

from resx2dict import resx2dict
import os
import polib
import shutil

class resx2po(object):
    """
    Converts resx to po and mo, it is using template.po file to keep file.py:line_number info
    """
    def __init__(self, resxen2name, resxlocale, potemplate, out_path, code):
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

        po.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'adam.schubert@sg1-game.net',
            'POT-Creation-Date': '2016-01-19 02:00+0100',
            'PO-Revision-Date': '2016-01-19 02:00+0100',
            'Last-Translator': 'Adam Schubert <adam.schubert@sg1-game.net>',
            'Language-Team': '',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
            'Language': code
        }
        for entry in po:
            if entry.msgid in motable:
                entry.msgstr = motable[entry.msgid]
            else:
                print("WARNING: {} not found in {}".format(entry.msgid, 'motable'))

        po.save()
        po.save_as_mofile(os.path.join(out_path, '{}.mo'.format(code)))
        shutil.copy2(potemplate, os.path.join(out_path, '{}.po'.format(code)))


directory = '../locale'
resx2po('Resources.resx', 'Resources.de.resx', 'messages.po', directory, 'de_DE')
resx2po('Resources.resx', 'Resources.es.resx', 'messages.po', directory, 'es_ES')
resx2po('Resources.resx', 'Resources.fr.resx', 'messages.po', directory, 'fr_FR')
resx2po('Resources.resx', 'Resources.it.resx', 'messages.po', directory, 'it_IT')
resx2po('Resources.resx', 'Resources.nl.resx', 'messages.po', directory, 'nl_NL')
resx2po('Resources.resx', 'Resources.no.resx', 'messages.po', directory, 'nb_NO')
resx2po('Resources.resx', 'Resources.pt.resx', 'messages.po', directory, 'pt_PT')
resx2po('Resources.resx', 'Resources.ru.resx', 'messages.po', directory, 'ru_RU')
resx2po('Resources.resx', 'Resources.tr.resx', 'messages.po', directory, 'tr_TR')
resx2po('Resources.resx', 'Resources.uk.resx', 'messages.po', directory, 'uk_UA')
resx2po('Resources.resx', 'Resources.zh-CHS.resx', 'messages.po', directory, 'zh_CN')
