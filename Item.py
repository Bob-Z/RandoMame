import AutoBoot
import Config
import os


class Item:
    def __init__(self, all_machine_xml):
        self.all_machine_xml = all_machine_xml
        self.machine_xml = None
        self.soft_xml = None
        self.softlist_name = None
        self.part_xml = None  # For vgmplay

    def set_machine_xml(self, machine_xml):
        self.machine_xml = machine_xml

    def get_machine_xml(self):
        return self.machine_xml

    def set_soft_xml(self, soft_xml):
        self.soft_xml = soft_xml

    def get_soft_xml(self):
        return self.soft_xml

    def set_softlist_name(self, softlist_name):
        self.softlist_name = softlist_name

    def get_softlist_name(self):
        return self.softlist_name

    def set_part_xml(self, part_xml):
        self.part_xml = part_xml

    def get_machine_short_name(self):
        if self.machine_xml is not None:
            return self.machine_xml.attrib['name']
        else:
            return None

    def get_cloneof_short_name(self):
        if 'cloneof' in self.machine_xml.attrib:
            return self.machine_xml.attrib['cloneof']
        else:
            return None

    def get_machine_description(self):
        if self.machine_xml is not None:
            return self.machine_xml.find("description").text

        return ""

    def get_machine_year(self):
        if self.machine_xml is not None:
            return self.machine_xml.find("year").text

        return ""

    def get_machine_full_description(self):
        return self.get_machine_description() + " (" + self.get_machine_year() + ")"

    def get_soft_short_name(self):
        return self.soft_xml.attrib['name']

    def get_soft_interface(self):
        part = self.soft_xml.findall("part")
        return part[0].attrib["interface"]

    def get_soft_description(self):
        if self.soft_xml is None:
            return ""
        return self.soft_xml.find('description').text

    def get_soft_year(self):
        if self.soft_xml is not None:
            return self.soft_xml.find('year').text
        return None

    def get_soft_full_description(self):
        if self.get_soft_description() is not None and self.get_soft_year() is not None:
            return self.get_soft_description() + " (" + self.get_soft_year() + ")"
        if self.get_soft_description() is not None:
            return self.get_soft_description()
        return None

    def get_sort_criteria(self):
        criteria = ""
        if self.get_soft_description() is not None and self.get_soft_description() != "":
            if Config.sort_by_year is True:
                if self.get_soft_year() is not None:
                    criteria = self.get_soft_year() + " " + self.get_soft_description() + " " + self.get_machine_description()
                else:
                    criteria = "0000 " + self.get_soft_description() + " " + self.get_machine_description()
            if Config.sort_by_name is True:
                if self.get_soft_year() is not None:
                    criteria = self.get_soft_description() + " " + self.get_soft_year() + " " + self.get_machine_description()
                else:
                    criteria = self.get_soft_description() + " " + self.get_machine_description()
        else:
            if Config.sort_by_name is True:
                criteria = self.get_machine_full_description()

            if Config.sort_by_year is True:
                criteria = self.get_machine_year() + " " + self.get_machine_description()

        return criteria

    def get_command_line(self):
        my_env = os.environ.copy()

        if self.soft_xml is None:
            command = self.get_machine_short_name() + AutoBoot.get_autoboot_command("",
                                                                                    self.get_machine_short_name())
            return command, my_env
        else:
            info_usage = self.get_soft_info_named("usage")

            if info_usage is not None:
                my_env["RANDOMAME_INFO_USAGE"] = info_usage
            else:
                my_env["RANDOMAME_INFO_USAGE"] = ""

            if self.part_xml is None:
                interface_command_line = self.get_interface_command_line()
                command = self.get_machine_short_name() + " " + interface_command_line + " " + self.soft_xml.attrib[
                    'name']

                command = command + AutoBoot.get_autoboot_command(self.softlist_name,
                                                                  self.get_machine_short_name())

                return command, my_env
            else:
                return "vgmplay -quik " + self.get_soft_short_name() + ":" + self.part_xml.attrib['name'], my_env

    # Return a command line to add a device supporting the given soft_interface on the given machine_xml
    def find_interface_name(self, soft_interface, machine_xml):
        device = machine_xml.findall("device")
        for d in device:
            if 'interface' in d.attrib:
                all_interface = d.attrib['interface'].split(',')
                for i in all_interface:
                    if i == soft_interface:
                        instance = d.find("instance")
                        if instance is not None:
                            if 'briefname' in instance.attrib:
                                interface_name = instance.attrib["briefname"]
                                command_line = "-" + interface_name
                                return command_line

        return None

    def get_interface_command_line(self):
        part = self.soft_xml.findall("part")
        soft_interface = part[0].attrib["interface"]
        print("Searching suitable software interface", soft_interface, "for", self.machine_xml.attrib['name'])

        # Search if a built-in device has a suitable software interface
        command_line = self.find_interface_name(soft_interface, self.machine_xml)

        if command_line is not None:
            return command_line

        if Config.skip_slot is True:
            return ""

        # Search if a slotted device has a suitable software interface
        slot = self.machine_xml.findall("slot")

        # FIXME horrible hack: I don't understand why there is no 'interface' property in floppy drives, hard disk and cd-rom devices...
        if soft_interface == 'floppy_5_25' or soft_interface == 'floppy_3_5' or soft_interface == 'ide_hdd' or soft_interface == 'scsi_hdd' or soft_interface == 'cdrom':
            return ""

        for s in slot:
            slotoption = s.findall("slotoption")
            for so in slotoption:
                for machine_xml in self.all_machine_xml:
                    if machine_xml.attrib['name'] == so.attrib['devname']:
                        command_line = self.find_interface_name(soft_interface, machine_xml)
                        if command_line is not None:
                            # Add slotted device command line
                            command_line = "-" + s.attrib['name'] + " " + so.attrib['name'] + " " + command_line
                            return command_line
        return ""

    def get_part_name(self):
        if self.part_xml is not None:
            feature = self.part_xml.find('feature')
            return feature.attrib['value']

        return None

    def get_title(self):
        if self.soft_xml is None:
            return self.get_machine_full_description()
        else:
            if self.part_xml is None:
                return self.get_soft_full_description() + " // " + self.get_machine_full_description()
            else:
                return self.get_part_name() + " // " + self.get_soft_description()

    def get_soft_info(self):
        if self.soft_xml is None:
            return ""

        info_string = ""
        all_info = self.soft_xml.findall('info')
        if all_info is not None:

            for info in all_info:
                name = info.attrib['name']
                value = info.attrib['value']
                info_string = info_string + " ,info - " + name + ": " + value

        return info_string

    def get_soft_info_named(self, name):
        if self.soft_xml is None:
            return ""

        info_string = ""
        all_info = self.soft_xml.findall('info')
        if all_info is not None:

            for info in all_info:
                if info.attrib['name'] == name:
                    value = info.attrib['value']
                    return value

        return None
