import SoundPulseAudio


def init():
    SoundPulseAudio.init()


def get_silence_duration_sec():
    return SoundPulseAudio.get_silence_duration_sec()


def reset():
    SoundPulseAudio.reset()


def kill():
    SoundPulseAudio.kill()


def set_mute(pid, is_mute):
    SoundPulseAudio.set_mute(pid, is_mute)
