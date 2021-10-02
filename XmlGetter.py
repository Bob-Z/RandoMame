import datetime
import subprocess
import Display
import xml.etree.ElementTree as ElementTree
import os.path
import Config
import Mame

temp_dir = "/tmp/"


def get_listxml_file_name():
    mame_version = Mame.get_version()
    return temp_dir + "listxml_" + mame_version + ".txt"


def get_softlist_file_name():
    mame_version = Mame.get_version()
    return temp_dir + "softlist_" + mame_version + ".txt"


def load_machine_list():
    Display.print_text("Get machines XML")

    file_name = get_listxml_file_name()

    if os.path.isfile(file_name) is False:
        print("Creating", file_name)
        fd = open(file_name, "w")
        subprocess.run([Config.mame_binary, '-listxml'],
                       stdout=fd)
    else:
        print(file_name, "already exists")


def load_soft_list():
    Display.print_text("Get software list XML")

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
    Display.print_text("Parsing software list XML")
    tree = ElementTree.parse(get_softlist_file_name())
    return tree.getroot()


def get():
    machine_list = None
    soft_list = None

    total_start = datetime.datetime.now()

    if Config.need_softlist is True:
        load_soft_list()
        soft_list = parse_soft_list()

    soft_list_end = datetime.datetime.now()
    print("Soft list parsing:", soft_list_end - total_start)

    if Config.need_machine is True:
        load_machine_list()
        machine_list = parse_machine_list()

    print("Machine parsing:", datetime.datetime.now() - soft_list_end)
    total_end = datetime.datetime.now()
    print("Total XML parsing:", total_end - total_start)

    return machine_list, soft_list
