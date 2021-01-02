import subprocess

import config


def start_server():
    command = config.COMMAND_START
    if not command:
        raise AttributeError("command missing!")

    # this is not nice form, but easier than creating a dedicated startup script
    # no shell escape! Make sure no garbage is passed!
    subprocess.Popen(config.COMMAND_START, shell=True)


def stop_server():
    command = config.COMMAND_STOP
    if not command:
        raise AttributeError("command missing!")

    # non-blocking, won't check returns either
    subprocess.Popen(config.COMMAND_STOP, shell=True)
