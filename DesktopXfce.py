import os
import subprocess


class DesktopXfce:
    decoration_size = None

    def set_position(self, machine_name, pos_x, pos_y, width, height):
        if self.decoration_size is None:
            self.find_decoration_size(machine_name)

        if self.decoration_size is not None:
            # Guess that 0 and 1 are right, left and 2 and 3 are top, bottom. To be validated
            width = width - int(self.decoration_size[0]) - int(self.decoration_size[1])
            height = height - int(self.decoration_size[2]) - int(self.decoration_size[3])

        size_str = str(int(width)) + " " + str(int(height))

        move_str = str(int(pos_x)) + " " + str(int(pos_y))
        search_str = "\"MAME.*" + machine_name + "\""

        command = "xdotool search --name " + search_str + " windowmove " + move_str + " windowsize " + size_str
        os.system(command)

    def find_decoration_size(self, machine_name):
        search_str = 'xdotool search --name "MAME.*"' + machine_name
        out = subprocess.Popen(
            search_str,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        sout, serr = out.communicate()

        if out.returncode != 0:
            return

        if len(sout) == 0:
            return

        window_id = int(sout)

        cmd = 'xwininfo -id ' + str(window_id) + ' -wm | grep "Frame extents"'
        out = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        sout, serr = out.communicate()

        if out.returncode != 0:
            return

        txt = sout.decode("utf-8").rstrip()
        split1 = txt.split(": ")
        self.decoration_size = split1[1].split(", ")

    def send_keyboard(self, machine_name):
        search_str = "\"MAME.*" + machine_name + "\""
        command = "xdotool search --name " + search_str + " key super"
        os.system(command)
