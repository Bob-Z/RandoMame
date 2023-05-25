import threading

import Config
import ModeAll
import ModeArcade
import ModeMusic
import ModeSelectedSoftList
import ModeSoftList

all_machine_xml = []
my_soft_list = []
gen_lock = threading.Lock()


def init(machine_list, soft_list):
    global all_machine_xml
    all_machine_xml = machine_list
    global my_soft_list
    my_soft_list = soft_list


def get():
    global all_machine_xml
    global my_soft_list
    global gen_lock
    with gen_lock:
        if Config.mode == "arcade":
            return ModeArcade.get(all_machine_xml)
        elif Config.mode == "standalone":
            # Standalone is the same as Arcade mode with different machine filter
            return ModeArcade.get(all_machine_xml)
        elif Config.mode == "slotmachine":
            # Slotmachine is the same as Arcade mode with different machine filter
            return ModeArcade.get(all_machine_xml)
        elif Config.mode == "softlist":
            return ModeSoftList.get(all_machine_xml, my_soft_list)
        elif Config.mode == "all":
            return ModeAll.get(all_machine_xml, my_soft_list)
        elif Config.mode == "selected softlist":
            return ModeSelectedSoftList.get(all_machine_xml, my_soft_list, Config.selected_softlist)
        elif Config.mode == "music":
            return ModeMusic.get(all_machine_xml, my_soft_list)
