import subprocess
import os

import Config
import Sound


def run(command):
    if command is None:
        return

    args = [Config.mame_binary]
    for c in command.split(' '):
        args.append(c)
    args += ['-nomouse', '-nohttp', '-window',
             '-ui_active', '-skip_gameinfo', '-resolution', '1x1']

    if Config.mode != 'music':
        args.append('-artwork_crop')

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
