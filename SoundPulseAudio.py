import os
import threading
import time
import subprocess
import re

silence_loop = 0
sample_duration_sec = 0.1
timeout_duration_sec = 0.1
silence_duration_sec = 0
tmp_file = '/tmp/randomame.sound'

running = True
monitor_silence_thread = None


def monitor_silence():
    global silence_loop
    silence_loop = 0
    while running is True:
        command = 'rm ' + tmp_file
        os.system(command)
        command = 'XDG_RUNTIME_DIR=/run/user/' + str(os.getuid()) + ' timeout ' + str(
            sample_duration_sec) + 's parec > ' + tmp_file + ' 2>&1'
        os.system(command)

        content = []
        with open(tmp_file, 'rb') as reader:
            content = reader.read(os.stat(tmp_file).st_size)

        is_sound = False
        if len(content) > 0:
            for c in content:
                if c != 0:
                    is_sound = True
                    break

        global silence_duration_sec
        if is_sound is False:
            silence_duration_sec += sample_duration_sec + timeout_duration_sec
            print("Silence duration: ", silence_duration_sec)
        else:
            silence_duration_sec = 0

        time.sleep(timeout_duration_sec)


def init():
    global monitor_silence_thread
    monitor_silence_thread = threading.Thread(target=monitor_silence)
    monitor_silence_thread.start()


def get_silence_duration_sec():
    global silence_duration_sec
    return silence_duration_sec


def reset():
    global silence_duration_sec
    silence_duration_sec = 0


def kill():
    global running
    running = False

    global monitor_silence_thread
    if monitor_silence_thread is not None:
        monitor_silence_thread.join()


def set_process_volume(pid, volume):
    stream_index = get_stream_index(pid)
    if stream_index is not None:
        command = 'pactl set-sink-input-volume ' + str(stream_index) + " " + str(volume) + "%"
        os.system(command)


def set_mute(pid, is_mute):
    stream_index = get_stream_index(pid)
    if stream_index is not None:
        if is_mute is True:
            param = '1'
        else:
            param = '0'
        command = 'pactl set-sink-input-mute ' + str(stream_index) + " " + param
        os.system(command)

        if is_mute is False:
            set_process_volume(pid, 100)


def get_stream_index(input_pid):
    out = subprocess.Popen(['pactl', 'list', 'sink-inputs'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    sout, serr = out.communicate()

    paragraphs = re.split('\n\n', sout.decode("utf-8"))
    for p in paragraphs:
        pid_txt = re.search('application.process.id(.+?)\n', p)
        if pid_txt is not None:
            pid = pid_txt.group(1).split('"')
            if int(pid[1]) == input_pid:
                stream_txt = re.search('Sink Input(.+?)\n', p)
                if stream_txt is not None:
                    stream = stream_txt.group(1).split('#')
                    return int(stream[1])

    return None
