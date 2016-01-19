import xml.etree.ElementTree as ET
def resx2dict(resx):
    tree = ET.parse(resx)
    root = tree.getroot()
    translationTable = {}
    for first in root.findall('./data'):
            translationTable[first.attrib['name']] = first.find('./value').text

    return translationTable
