import Config
import XmlGetter
from pathlib import Path


def start():
    print("Parsing MAME input")
    machine_list, soft_list = XmlGetter.get()
    print("Parsing MAME input DONE")

    print("File type:", "merged")
    needed_rom_file_list = get_needed_rom_file("merged", machine_list)
    existing_rom_file = get_existing_rom_file()

    print("")
    print("Missing ROMS file:")
    print("==================")
    print("")
    for needed in needed_rom_file_list:
        if needed not in existing_rom_file:
            print(needed)

    print("")
    print("Useless ROMS file:")
    print("==================")
    print("")
    for existing in existing_rom_file:
        if existing not in needed_rom_file_list:
            print(existing)

    # needed_directory_list = get_dir("merged")

    # for soft_list_dir in needed_directory_list:
    #    needed_soft_file_list = get_soft_file("merged", soft_list_dir)


def get_needed_rom_file(rom_type, machine_xml):
    needed_rom_file_list = []
    for machine in machine_xml:
        has_rom = False
        for r in machine.findall("rom"):
            if r.attrib['status'] != 'nodump':
                has_rom = True
                break

        need_file = True
        if "romof" in machine.attrib:  # use BIOS
            need_file = False

            # Get romof machine XML
            romof_machine = None

            romof_name = machine.attrib['romof']
            for romof_m in machine_xml:
                if romof_m.attrib['name'] == romof_name:
                    romof_machine = romof_m
                    break

            # Check if one ROM of current machine is not in romof machine
            for rom_current in machine.findall('rom'):  # for each current machine's ROMs
                if 'status' not in rom_current.attrib or rom_current.attrib['status'] != 'nodump':  # if it's dumped
                    rom_found = False
                    for romof_rom in romof_machine.findall('rom'):
                        if romof_rom.attrib['name'] == rom_current.attrib['name']:  # if ROM exists in romof machine
                            rom_found = True
                            break

                    if rom_found is False:
                        need_file = True
                        break

        if has_rom is True and need_file is True:
            if rom_type == "merged":
                if "cloneof" not in machine.attrib:  # Not a clone
                    needed_rom_file_list.append(machine.attrib['name'])
            else:
                needed_rom_file_list.append(machine.attrib['name'])

    return needed_rom_file_list


def get_existing_rom_file():
    existing_rom_file = []

    path = Path(Config.check)
    for file in path.iterdir():
        if file.is_file():
            existing_rom_file.append(file.stem)

    return existing_rom_file
