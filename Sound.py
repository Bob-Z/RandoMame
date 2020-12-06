import SoundPulseAudio


def init():
    SoundPulseAudio.init()


def is_silence_detected():
    return SoundPulseAudio.is_silence_detected()


def reset():
    SoundPulseAudio.reset()


def kill():
    SoundPulseAudio.kill()
