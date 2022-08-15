import threading
from datetime import datetime

import Config

lock = threading.Lock()
index = 0
time_from_first_print = datetime.now()


def get_name():
    global index
    global lock

    lock.acquire()
    index = index + 1
    lock.release()

    name = Config.record + "/" + '{:03d}'.format(index)

    return name


def create_aspect_ratio_file(item):
    machine_xml = item.get_machine_xml()

    additional_command = None

    if machine_xml is None:  # vgmplay
        ratio_string = ""
        additional_command = ["-snapsize", "1024x484"]
    else:
        display = item.get_machine_xml().find("display")

        if display is None:  # layout based machine
            ratio_string = ""
            additional_command = ["-snapsize", "1920x1440"]
        else:
            if "width" not in display.attrib or "height" not in display.attrib:
                ratio_string = ""
                additional_command = ["-snapsize", "1920x1440"]
            else:
                width = float(display.attrib["width"])
                height = float(display.attrib["height"])

                if display.attrib["type"] == "raster":
                    # assume raster display is 4/3 ?

                    if width > height:  # 4/3
                        ratio_string = "1920x1440"
                    else:  # 3/4
                        ratio_string = "1080:1440"
                else:
                    ratio1 = 2560.0 / width
                    ratio2 = 1440.0 / height

                    ratio = min(ratio1, ratio2)
                    output_width = width * ratio
                    output_height = height * ratio

                    ratio_string = str(int(output_width)) + ":" + str(int(output_height))

    with open(Config.record + "/" + '{:03d}'.format(index) + ".aspect", "w") as f:
        f.write(ratio_string)

    return additional_command


def create_time_file():
    if Config.end_duration:
        with open(Config.record + "/" + '{:03d}'.format(index) + ".time", "w") as f:
            f.write(str(Config.end_duration))


def create_srt_file(item):
    machine_xml = item.get_machine_xml()

    if machine_xml is None:  # vgmplay
        with open(Config.record + "/" + '{:03d}'.format(index) + ".srt", "w") as f:
            f.write("1\n00:00:00,000 --> 20:00:00,000\n")
            f.write(item.get_soft_full_description())
            f.write("\n")
            f.write(item.get_part_name())

    else:
        with open(Config.record + "/" + '{:03d}'.format(index) + ".srt", "w") as f:
            f.write("1\n00:00:00,000 --> 00:00:03,000\n")
            if item.get_soft_full_description() != "":
                f.write(item.get_soft_full_description() + " [" + item.get_soft_short_name() + "]\n")
            f.write(item.get_machine_full_description() + " [" + item.get_machine_short_name() + "]")


def create_command_file(command):
    with open(Config.record + "/" + '{:03d}'.format(index) + ".cmd.txt", "w") as f:
        f.write(command)


def log(input_log):
    if Config.record is not None:
        with open(Config.record + "/" + "log.txt", "a") as f:
            f.write(input_log + "\n")


def timed_log(log_str):
    global time_from_first_print

    with open("timed.log", "a") as f:
        delta = datetime.now() - time_from_first_print
        minutes = int(delta.seconds / 60)
        minutes_in_seconds = minutes * 60
        seconds = delta.seconds - minutes_in_seconds
        time_log = '{:}:{:02}'.format(minutes, seconds)
        f.write(time_log + " " + log_str + "\n")


def reset_log_time():
    global time_from_first_print

    time_from_first_print = datetime.now()
