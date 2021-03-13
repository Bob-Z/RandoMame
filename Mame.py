import subprocess
import os

import Config
import Sound
import Record


def run(item):
    if item is None:
        return

    args = [Config.mame_binary]
    command = item.get_command_line()
    for c in command.split(' '):
        args.append(c)
    args += ['-nomouse', '-nohttp', '-window',
             '-ui_active', '-skip_gameinfo', '-resolution', '1x1']

    if Config.mode != 'music':
        args.append('-artwork_crop')

    if Config.record is not None:
        filename = Record.get_name() + ".avi"
        args.append('-aviwrite')
        args.append(filename)

        additional_command = Record.create_aspect_ratio_file(item)
        if additional_command is not None:
            args.extend(additional_command)

    if Config.extra is not None:
        args.append(Config.extra)

    full_command = ""
    for a in args:
        full_command += a + " "
    print("Running full command: " + full_command)

    # Linux PulseAudio specific
    my_env = os.environ.copy()
    my_env["XDG_RUNTIME_DIR"] = "/run/user/" + str(os.getuid())

    out = subprocess.Popen(args,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           env=my_env)

    Sound.reset()

    return out
