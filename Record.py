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

    name = Config.record + "/" + str(index)

    return name


def create_aspect_ratio_file(item):
    machine_xml = item.get_machine_xml()

    additional_command = None

    if machine_xml is None: # vgmplay
        ratio_string = ""
        additional_command = ["-snapsize", "1280x720"]
    else:
        display = item.get_machine_xml().find("display")

        if display is None: # layout based machine
            ratio_string = ""
            additional_command = ["-snapsize", "1440x1080"]
        else:
            width = float(display.attrib["width"])
            height = float(display.attrib["height"])

            if display.attrib["type"] == "raster":
                # assume raster display is 4/3 ?

                if width > height:  # 4/3
                    ratio_string = "1440:1080"
                else:  # 3/4
                    ratio_string = "810:1080"
            else:
                ratio1 = 1920.0 / width
                ratio2 = 1080.0 / height

                ratio = min(ratio1, ratio2)
                output_width = width * ratio
                output_height = height * ratio

                ratio_string = str(int(output_width)) + ":" + str(int(output_height))

    with open(Config.record + "/" + str(index) + ".aspect", "w") as f:
        f.write(ratio_string)

    return additional_command
