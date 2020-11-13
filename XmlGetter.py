import subprocess
import xml.etree.ElementTree as ElementTree

import Config
from XmlDriverFilter import XmlDriverFilter


def load_driver_list():
    print("Reading MAME's drivers list")
    out = subprocess.Popen([Config.mame_binary, '-listxml'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    return out.communicate()


def load_soft_list():
    print("Reading MAME's softwares list")
    out = subprocess.Popen([Config.mame_binary, '-getsoftlist'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    return out.communicate()


def get():
    stdout, stderr = load_driver_list()

    print("Parsing MAME's drivers list")
    target = XmlDriverFilter()
    parser = ElementTree.XMLParser(target=target)
    driver_list = ElementTree.fromstring(stdout, parser=parser)

    soft_list = None
    if Config.arcade_mode is False:
        stdout, stderr = load_soft_list()
        print("Parsing MAME's softwares list")
        soft_list = ElementTree.fromstring(stdout)

    return driver_list, soft_list
