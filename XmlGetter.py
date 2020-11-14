import subprocess
import xml.etree.ElementTree as ElementTree
from multiprocessing import Process, Queue

import Config
from XmlMachineFilter import XmlMachineFilter


def load_machine_list():
    print("Reading MAME's machines list")
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


def parse_machine_list(stdout):
    print("Parsing MAME's machines list")
    target = XmlMachineFilter()
    parser = ElementTree.XMLParser(target=target)
    return ElementTree.fromstring(stdout, parser=parser)


def parse_soft_list(stdout):
    print("Parsing MAME's softwares lists")
    return ElementTree.fromstring(stdout)


def get():
    stdout, stderr = load_machine_list()
    machine_list = parse_machine_list(stdout)

    if Config.mode == 'softlist':
        stdout, stderr = load_soft_list()
        soft_list = parse_soft_list(stdout)

    return machine_list, soft_list
