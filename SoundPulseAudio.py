import os
import threading
import time

silence_detected = False
silence_loop = 0
sample_duration_sec = 0.1
timeout_duration_sec = 0.1
silence_detection_sec = 5
silence_loop_detected = int(silence_detection_sec / (sample_duration_sec + timeout_duration_sec))
tmp_file = '/tmp/randomame.sound'

running = True
monitor_silence_thread = None


def monitor_silence():
    global silence_loop
    silence_loop = 0
    while running is True:
        # This is hacky, let me know if you find something cleaner.
        command = 'XDG_RUNTIME_DIR=/run/user/' + str(os.getuid()) + ' timeout ' + str(
            sample_duration_sec) + 's parec > ' + tmp_file + ' 2>&1'
        os.system(command)

        with open(tmp_file, 'rb') as reader:
            content = reader.read(os.stat(tmp_file).st_size)

        is_sound = False
        for c in content:
            if c != 0:
                is_sound = True
                break

        global silence_detected
        if is_sound is False:
            silence_loop = silence_loop + 1
            if silence_loop >= silence_loop_detected:
                silence_detected = True
        else:
            silence_loop = 0
            silence_detected = False

        time.sleep(timeout_duration_sec)


def init():
    global monitor_silence_thread
    monitor_silence_thread = threading.Thread(target=monitor_silence)
    monitor_silence_thread.start()


def is_silence_detected():
    global silence_detected
    return silence_detected


def reset():
    global silence_detected
    silence_detected = False
    global silence_loop
    silence_loop = 0


def kill():
    global running
    running = False

    global monitor_silence_thread
    if monitor_silence_thread is not None:
        monitor_silence_thread.join()
