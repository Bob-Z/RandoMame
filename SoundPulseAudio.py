import os
import re
import struct
import subprocess
import threading
import time
import pyaudio

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

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    while running is True:
        stream.start_stream()
        byte_array = stream.read(CHUNK)
        stream.stop_stream()

        count = int(len(byte_array) / 2)

        if count >= 1024:
            integers = struct.unpack('h' * count, byte_array)

            is_sound = False
            if len(integers) > 63:
                first = integers[64]
                first_max = first * 1.1
                first_min = first * 0.9
                integers_max = max(first_min, first_max)
                integers_min = min(first_min, first_max)
                for i in range(65, len(integers)):
                    if integers[i] > integers_max or integers[i] < integers_min:
                        is_sound = True
                        break

            global silence_duration_sec
            if is_sound is False:
                silence_duration_sec += sample_duration_sec + timeout_duration_sec
            else:
                silence_duration_sec = 0

        time.sleep(timeout_duration_sec)


def init():
    print('Warning ! For smart sound to work,  make sure that your default (or fallback) "Input device" in PulseAudio\'s configuration is your output device\'s "monitor"')
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
