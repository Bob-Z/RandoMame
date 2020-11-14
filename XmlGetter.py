import subprocess
import xml.etree.ElementTree as ElementTree
from multiprocessing import Process

import Config
from XmlMachineFilter import XmlMachineFilter


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


class XmlGetter:
    my_machine_list = None
    my_soft_list = None

    def parse_machine_list(self, stdout):
        print("Parsing MAME's machines list start")
        target = XmlMachineFilter()
        parser = ElementTree.XMLParser(target=target)
        self.my_machine_list = ElementTree.fromstring(stdout, parser=parser)
        print("Parsing MAME's machines list finished")

    def parse_soft_list(self, stdout):
        print("Parsing MAME's softwares lists start")
        self.my_soft_list = ElementTree.fromstring(stdout)
        print("Parsing MAME's softwares lists finished")

    def get(self):
        stdout, stderr = load_machine_list()
        #parse_machine_process = Process(target=self.parse_machine_list, args=(stdout,))
        #parse_machine_process.start()
        self.parse_machine_list(stdout)

        if Config.mode == 'softlist':
            stdout, stderr = load_soft_list()
            #parse_soft_process = Process(target=self.parse_soft_list, args=(stdout,))
            #parse_soft_process.start()
            self.parse_soft_list(stdout)

        #parse_machine_process.join()
        #parse_soft_process.join()

        return self.my_machine_list, self.my_soft_list
