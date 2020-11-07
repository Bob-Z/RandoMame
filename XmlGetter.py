import subprocess
import xml.etree.ElementTree as ElementTree
from XmlFilter import XmlFilter


def load_string():
    print("Reading MAME's XML data")
    out = subprocess.Popen(['/media/4To/emu/mame/mame/mame64', '-listxml'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    return out.communicate()


def get():
    stdout, stderr = load_string()
    print("Parsing MAME's XML data")

    target = XmlFilter()
    parser = ElementTree.XMLParser(target=target)

    return ElementTree.fromstring(stdout, parser=parser)
