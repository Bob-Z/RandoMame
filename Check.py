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

    total_machine_qty = 0
    total_parent_qty = 0
    total_clone_qty = 0

    for machine in machine_xml:
        total_machine_qty = total_machine_qty + 1
        if 'cloneof' in machine.attrib:
            total_clone_qty = total_clone_qty + 1
        else:
            total_parent_qty = total_parent_qty + 1

    machine_qty = 0
    parent_qty = 0
    clone_qty = 0

    for machine in machine_xml:
        machine_qty = machine_qty + 1
        if "cloneof" not in machine.attrib:  # Not a clone
            parent_qty = parent_qty + 1
            has_rom = is_machine_need_roms(machine, machine_xml)

            need_file = True
            if "romof" in machine.attrib:  # use BIOS
                need_file = False

                # Get romof machine XML
                romof_machine = None

                romof_name = machine.attrib['romof']
                #                for romof_m in machine_xml:
                #                    if romof_m.attrib['name'] == romof_name:
                #                        romof_machine = romof_m
                #                        break

                command = ".//machine[@name=\"" + romof_name + "\"]"
                romof_machine = machine_xml.find(command)

                # Check if one ROM of current machine is not in romof machine
                for rom_current in machine.findall('rom'):  # for each current machine's ROMs
                    if 'status' not in rom_current.attrib or rom_current.attrib['status'] != 'nodump':  # if it's dumped
                        rom_found = False
                        for romof_rom in romof_machine.findall('rom'):
                            if 'sha1' in romof_rom:
                                if romof_rom.attrib['sha1'] == rom_current.attrib[
                                    'sha1']:  # if ROM exists in romof machine
                                    rom_found = True
                                    break
                            elif 'crc' in romof_rom:
                                if romof_rom.attrib['crc'] == rom_current.attrib[
                                    'crc']:  # if ROM exists in romof machine
                                    rom_found = True
                                    break
                            else:
                                if romof_rom.attrib['name'] == rom_current.attrib[
                                    'name']:  # if ROM exists in romof machine
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
        else:
            clone_qty = clone_qty + 1

        if machine_qty % 10 == 0:
            print(int(machine_qty / total_machine_qty * 100), "% : parent = ", parent_qty, "/", total_parent_qty,
                  ", clone "
                  "= ",
                  clone_qty, "/", total_clone_qty, end='\r')

    return needed_rom_file_list


def is_machine_need_roms(parent_machine, machine_xml):
    parent_name = parent_machine.attrib['name']
    parent_and_clone = [parent_machine]

    for clone_machine in machine_xml:
        if 'cloneof' in clone_machine.attrib and clone_machine.attrib['cloneof'] == parent_name:
            parent_and_clone.append(clone_machine)

    has_rom = False
    for m in parent_and_clone:
        if has_rom is False:
            for r in m.findall("rom"):
                if r.attrib['status'] != 'nodump':
                    has_rom = True
                    break

    return has_rom


def get_existing_rom_file():
    existing_rom_file = []

    path = Path(Config.check)
    for file in path.iterdir():
        if file.is_file():
            existing_rom_file.append(file.stem)

    return existing_rom_file


def print_file_tree():
    print("Parsing MAME input")
    machine_xml, soft_xml = XmlGetter.get()
    print("Parsing MAME input DONE")

    for machine in machine_xml:
        if 'cloneof' in machine.attrib:
            all_disk = machine.findall("disk")

            for disk in all_disk:
                if 'merge' in disk.attrib:
                    continue
                print(machine.attrib["cloneof"] + "/" + disk.attrib["name"] + ".chd")

            continue

        all_disk = machine.findall("disk")
        for disk in all_disk:
            if 'merge' in disk.attrib:
                continue
            print(machine.attrib["name"] + "/" + disk.attrib["name"] + ".chd")

        all_rom = machine.findall("rom")

        new_rom_qty = 0
        for rom in all_rom:
            if rom.attrib['status'] != 'nodump':
                new_rom_qty += 1

        if new_rom_qty == 0:
            continue

        if 'romof' in machine.attrib:
            romof_machine = machine_xml.find('.//machine[@name="' + machine.attrib["romof"] + '"]')
            all_rom = machine.findall("rom")

            all_rom_in_parent = True
            for rom in all_rom:
                if 'status' in rom.attrib:
                    if rom.attrib['status'] == 'nodump':
                        continue
                romof_machine_rom = romof_machine.find('.//rom[@name="' + rom.attrib["name"] + '"]')
                if romof_machine_rom is None:
                    all_rom_in_parent = False
                    break

            if all_rom_in_parent is True:
                continue

        print(machine.attrib["name"] + ".zip")

    for soft_list in soft_xml:
        for soft in soft_list:
            if 'cloneof' in soft.attrib:
                continue

            all_part = soft.findall("part")
            for part in all_part:
                all_dataarea = part.findall("dataarea")
                if len(all_dataarea) > 0:
                    print(soft_list.attrib["name"] + "/" + soft.attrib["name"] + ".zip")
                all_diskarea = part.findall("diskarea")
                for diskarea in all_diskarea:
                    all_disk = diskarea.findall("disk")
                    for disk in all_disk:
                        print(soft_list.attrib["name"] + "/" + soft.attrib["name"] + "/" + disk.attrib["name"] + ".chd")
