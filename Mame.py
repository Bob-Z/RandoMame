import subprocess
import os

import Config
import Sound
import Record


def run(item):
    if item is None:
        return

    args = [Config.mame_binary]
    command, my_env = item.get_command_line()
    for c in command.split(' '):
        args.append(c)
    args += ['-nohttp',
             '-ui_active', '-skip_gameinfo', ]

    if Config.mode == 'music':  # Disable joystick and lightgun detection. This speeds-up start-up and helps for noise detection.
        args.append('-joystickprovider')
        args.append('none')
        args.append('-lightgunprovider')
        args.append('none')

    if Config.windows_quantity != 1:
        args.append('-nomouse')
        args.append('-window')
        args.append('-resolution')
        args.append('1x1')

    if Config.record is not None:
        filename = Record.get_name() + ".avi"
        args.append('-aviwrite')
        args.append(filename)

        additional_command = Record.create_aspect_ratio_file(item)
        if additional_command is not None:
            args.extend(additional_command)

        Record.create_srt_file(item)

    if Config.emulation_time is True:
        args.append('-str')
        args.append(str(Config.timeout))

    if Config.extra is not None:
        for e in Config.extra.split(' '):
            args.append(e)

    if item.get_machine_xml() is not None:
        display = item.get_machine_xml().find("display")
        if display is not None and display.attrib["type"] == "raster":
            args.append('-artwork_crop')

    full_command = ""
    for a in args:
        full_command += a + " "
    print("Running full command: " + full_command)

    if Config.record is not None:
        Record.create_command_file(full_command)

    if Config.dry_run is False:
        # Linux PulseAudio specific
        my_env["XDG_RUNTIME_DIR"] = "/run/user/" + str(os.getuid())

        out = subprocess.Popen(args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               env=my_env)

        Sound.reset()

        return out


def get_version():
    args = [Config.mame_binary]
    args += ['-version']

    out = subprocess.run(args, capture_output=True)
    return out.stdout.decode('utf-8')
