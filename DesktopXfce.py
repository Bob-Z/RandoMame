import os
import subprocess


class DesktopXfce:
    decoration_size = None

    def get_desktop_size(self):
        command = "xdpyinfo | awk '/dimensions:/ { print $2; exit }'"
        out = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        sout, serr = out.communicate()

        txt = sout.decode("utf-8").rstrip()
        split1 = txt.split("x")

        return [0, 0, int(split1[0]), int(split1[1])]  # TODO pos_x and pos_y are hard coded to 0

    def set_position(self, pid, pos_x, pos_y, width, height):
        if self.decoration_size is None:
            self.find_decoration_size(pid)

        if self.decoration_size is not None:
            # Guess that 0 and 1 are right, left and 2 and 3 are top, bottom. To be validated
            width = width - int(self.decoration_size[0]) - int(self.decoration_size[1])
            height = height - int(self.decoration_size[2]) - int(self.decoration_size[3])

        size_str = str(int(width)) + " " + str(int(height))

        move_str = str(int(pos_x)) + " " + str(int(pos_y))

        command = "xdotool search --all --pid " + str(
            pid) + " --class mame windowmove " + move_str + " windowsize " + size_str + " > /dev/null 2>&1"
        
        os.system(command)
        # Sometimes the first call does not honor requested position (slightly too right when trying coordinates 0,0)
        return_value = os.system(command)

        if return_value == 0 and self.decoration_size is not None:
            return True
        else:
            return False

    def find_decoration_size(self, pid):
        search_str = 'xdotool search --all --pid ' + str(pid)
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

    def send_keyboard(self, pid):
        command = "xdotool search --all --pid " + str(pid) + " --class mame key super > /dev/null 2>&1"
        return_value = os.system(command)

        if return_value == 0:
            return True
        else:
            return False

    def set_title(self, pid, title):
        command = "xdotool search --all --pid " + str(
            pid) + " --class mame set_window --name \"" + title + "\" > /dev/null 2>&1"
        return_value = os.system(command)

        if return_value == 0:
            return True
        else:
            return False
