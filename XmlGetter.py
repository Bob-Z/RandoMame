import datetime
import subprocess
import threading
import Display
import xml.etree.ElementTree as ElementTree
import os.path

import Config
import Mame

soft_list = None
temp_dir = "/tmp/"


def get_listxml_file_name():
    mame_version = Mame.get_version()
    return temp_dir + "listxml_" + mame_version + ".txt"


def get_softlist_file_name():
    mame_version = Mame.get_version()
    return temp_dir + "softlist_" + mame_version + ".txt"


def load_machine_list():
    Display.print_text("Reading machines list")

    file_name = get_listxml_file_name()

    if os.path.isfile(file_name) is False:
        print("Creating", file_name)
        fd = open(file_name, "w")
        subprocess.run([Config.mame_binary, '-listxml'],
                       stdout=fd)
    else:
        print(file_name, "already exists")


def load_soft_list():
    Display.print_text("Reading software list")

    file_name = get_softlist_file_name()

    if os.path.isfile(file_name) is False:
        print("Creating", file_name)
        fd = open(file_name, "w")
        subprocess.run([Config.mame_binary, '-getsoftlist'],
                       stdout=fd)
    else:
        print(file_name, "already exists")


def parse_machine_list():
    Display.print_text("Parsing machines list")
    tree = ElementTree.parse(get_listxml_file_name())
    return tree.getroot()


def parse_soft_list():
    Display.print_text("Parsing softwares lists")
    tree = ElementTree.parse(get_softlist_file_name())
    return tree.getroot()


def get_soft_list():
    a = datetime.datetime.now()
    load_soft_list()
    b = datetime.datetime.now()
    print(b - a)
    a = datetime.datetime.now()
    global soft_list
    soft_list = parse_soft_list()
    b = datetime.datetime.now()
    print(b - a)


def get():
    total_start = datetime.datetime.now()
    get_soft_list_thread = None

    if Config.need_softlist:
        get_soft_list_thread = threading.Thread(target=get_soft_list)
        get_soft_list_thread.start()

    machine_list = None
    if Config.need_machine is True:
        a = datetime.datetime.now()
        load_machine_list()
        b = datetime.datetime.now()
        print(b - a)
        a = datetime.datetime.now()
        machine_list = parse_machine_list()
        b = datetime.datetime.now()
        print(b - a)

    if get_soft_list_thread is not None:
        get_soft_list_thread.join()

    total_end = datetime.datetime.now()
    print("Total XML data loading:", total_end - total_start)

    return machine_list, soft_list
