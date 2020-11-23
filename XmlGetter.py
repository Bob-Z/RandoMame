import subprocess
import xml.etree.ElementTree as ElementTree
import datetime

import Config


# from XmlMachineFilter import XmlMachineFilter


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
    # target = XmlMachineFilter()
    # parser = ElementTree.XMLParser(target=target)
    # return ElementTree.fromstring(stdout, parser=parser)
    return ElementTree.fromstring(stdout)


def parse_soft_list(stdout):
    print("Parsing MAME's softwares lists")
    return ElementTree.fromstring(stdout)


def get_soft_list():
    a = datetime.datetime.now()
    stdout, stderr = load_soft_list()
    b = datetime.datetime.now()
    print(b - a)
    a = datetime.datetime.now()
    soft_list = parse_soft_list(stdout)
    b = datetime.datetime.now()
    print(b - a)

    return soft_list


def get():
    machine_list = None
    if Config.mode != 'music':
        a = datetime.datetime.now()
        stdout, stderr = load_machine_list()
        b = datetime.datetime.now()
        print(b - a)
        a = datetime.datetime.now()
        machine_list = parse_machine_list(stdout)
        b = datetime.datetime.now()
        print(b - a)

    soft_list = None
    if Config.need_softlist:
        soft_list = get_soft_list()

    return machine_list, soft_list
