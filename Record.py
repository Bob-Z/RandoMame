import threading

import Config

lock = threading.Lock()
index = 0


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

    if machine_xml is None: # vgmplay
        ratio_string = ""
        additional_command = ["-snapsize", "1024x576"]
    else:
        display = item.get_machine_xml().find("display")

        if display is None: # layout based machine
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
