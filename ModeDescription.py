import random
import re

import MachineFilter
import ModeSelectedSoftList

found = []


def prepare(machine_list, softlist_list, description):
    print("Searching for description:", description)
    compiled_re = re.compile(description)

    for m in machine_list:
        machine_description = m.find('description')
        result = compiled_re.match(machine_description.text)
        if result is not None:
            machine_filtered, title_filtered = MachineFilter.get(m)
            if machine_filtered is not None:
                found.append([machine_filtered.attrib['name'], title_filtered])
                print("Found", title_filtered)

    for softlist in softlist_list:
        for soft in softlist:
            soft_description = soft.find('description')
            result = compiled_re.match(soft_description.text)
            if result is not None:
                machine_name, machine_description = ModeSelectedSoftList.find_machine(machine_list, softlist.attrib['name'])
                if machine_name is not None:
                    command = machine_name + " " + soft.attrib['name']
                    title = soft_description.text + " (" + soft.find('year').text + ")" + " / " + machine_description
                    found.append([command, title])
                    print("Found", title)


def get(machine_list, softlist_list, description):
    if len(found) == 0:
        prepare(machine_list, softlist_list, description)

    rand = random.randrange(len(found))
    return found[rand]
