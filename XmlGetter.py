import datetime
import subprocess
import threading
import Display
import xml.etree.ElementTree as ElementTree

import Config

soft_list = None


# from XmlMachineFilter import XmlMachineFilter


def load_machine_list():
    print("Reading MAME's machines list")
    Display.print_text("Reading MAME's machines list", None)
    out = subprocess.Popen([Config.mame_binary, '-listxml'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    return out.communicate()


def load_soft_list():
    print("Reading MAME's softwares list")
    Display.print_text("Reading MAME's softwares list", None)
    out = subprocess.Popen([Config.mame_binary, '-getsoftlist'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    return out.communicate()


def parse_machine_list(stdout):
    print("Parsing MAME's machines list")
    Display.print_text("Parsing MAME's machines list", None)
    # target = XmlMachineFilter()
    # parser = ElementTree.XMLParser(target=target)
    # return ElementTree.fromstring(stdout, parser=parser)
    return ElementTree.fromstring(stdout)


def parse_soft_list(stdout):
    print("Parsing MAME's softwares lists")
    Display.print_text("Parsing MAME's softwares lists", None)
    return ElementTree.fromstring(stdout)


def get_soft_list():
    a = datetime.datetime.now()
    stdout, stderr = load_soft_list()
    b = datetime.datetime.now()
    print(b - a)
    a = datetime.datetime.now()
    global soft_list
    soft_list = parse_soft_list(stdout)
    b = datetime.datetime.now()
    print(b - a)


def get():
    total_start = datetime.datetime.now()
    get_soft_list_thread = None

    if Config.need_softlist:
        get_soft_list_thread = threading.Thread(target=get_soft_list)
        get_soft_list_thread.start()

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

    if get_soft_list_thread is not None:
        get_soft_list_thread.join()

    total_end = datetime.datetime.now()
    print("Total XML data loading:", total_end - total_start)

    return machine_list, soft_list
