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
import datetime

import xml.etree.ElementTree as ET
from pathlib import Path
import polib


class Resx2Po:
    def __init__(self, en_resx: Path, translation_resx: Path, code: str, output_po: Path):
        if not en_resx.is_file():
            raise Exception("EN Resx {} not found".format(en_resx.absolute()))

        if not translation_resx.is_file():
            raise Exception("Translation {} {} Resx bound not found".format(code, translation_resx.absolute()))

        self.en_resx = self.resx2dict(en_resx)
        self.translation_resx = self.resx2dict(translation_resx)
        self.code = code
        self.output_po = output_po

        self.generate()

    def resx2dict(self, resx):
        tree = ET.parse(resx)
        root = tree.getroot()
        translation_table = {}
        for first in root.findall('./data'):
            translation_table[first.attrib['name']] = first.find('./value').text

        return translation_table

    def generate(self):
        po = polib.POFile()
        now = datetime.datetime.now(datetime.timezone.utc)
        po.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'adam.schubert@sg1-game.net',
            'POT-Creation-Date': now.strftime("%Y-%m-%d %H:%M%z"),
            'PO-Revision-Date': now.strftime("%Y-%m-%d %H:%M%z"),
            'Last-Translator': 'Adam Schubert <adam.schubert@sg1-game.net>',
            'Language-Team': '',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
            'Language': self.code
        }

        for message_en_id, message_en in self.en_resx.items():
            if message_en_id in self.translation_resx:
                entry = polib.POEntry(
                    msgid=message_en,
                    msgstr=self.translation_resx[message_en_id],
                    comment=message_en_id
                )
                po.append(entry)
            else:
                print('WARNING: {} not found in {} resx'.format(message_en_id, self.code))

        po.save(str(self.output_po.absolute()))


code_list = {
    'da': 'da_DK',

    # 'de': 'de_DE',
    # 'es': 'es_ES',
    # 'es-MX': 'es_MX',
    # 'fa': 'fa_IR',
    # 'fi': 'fi_FI',
    # 'fr': 'fr_FR',
    # 'it': 'it_IT',
    # 'ja': 'ja_IP',
    # 'ko': 'ko_KR',
    # 'nb': 'nb_NO',
    # 'nl': 'nl_NL',
    # 'pl': 'pl_PL',
    # 'pt': 'pt_PT',
    # 'ro': 'ro_RO',
    # 'ru': 'ru_RU',
    # 'sl': 'sl_SI',
    # 'sv': 'sv_SE',
    # 'tr': 'tr_TR',
    # 'uk': 'uk_UA',
    # 'zh-Hans': 'zh_Hans_CN',
    # 'zh-Hant': 'zh_Hant',
}

output_dir = Path('../locale')

for from_code, to_code in code_list.items():
    output_file = output_dir.joinpath('{}.po'.format(to_code))
    Resx2Po(
        Path('Resources.resx'),
        Path('Resources.{}.resx'.format(from_code)),
        to_code,
        output_file
    )
