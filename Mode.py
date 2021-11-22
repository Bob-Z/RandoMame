import threading

import Config
import ModeAll
import ModeArcade
import ModeMusic
import ModeSelectedSoftList
import ModeSoftList

my_machine_list = []
my_soft_list = []
gen_lock = threading.Lock()


def init(machine_list, soft_list):
    global my_machine_list
    my_machine_list = machine_list
    global my_soft_list
    my_soft_list = soft_list


def get():
    global my_machine_list
    global my_soft_list
    global gen_lock
    with gen_lock:
        if Config.mode == "arcade":
            return ModeArcade.get(my_machine_list)
        elif Config.mode == "standalone":
            # Standalone is the same as Arcade mode with different machine filter
            return ModeArcade.get(my_machine_list)
        elif Config.mode == "slotmachine":
            # Slotmachine is the same as Arcade mode with different machine filter
            return ModeArcade.get(my_machine_list)
        elif Config.mode == "softlist":
            return ModeSoftList.get(my_machine_list, my_soft_list)
        elif Config.mode == "all":
            return ModeAll.get(my_machine_list, my_soft_list)
        elif Config.mode == "selected softlist":
            return ModeSelectedSoftList.get(my_machine_list, my_soft_list, Config.selected_softlist)
        elif Config.mode == "music":
            return ModeMusic.get(my_soft_list)
