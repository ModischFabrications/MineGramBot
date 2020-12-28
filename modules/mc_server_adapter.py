import subprocess

import config


def start_server():
    command = config.COMMAND_START
    if not command:
        raise AttributeError("command missing!")

    # this is not nice form, but easier than creating a dedicated startup script
    # no shell escape! Make sure no garbage is passed!
    process = subprocess.run(config.COMMAND_START, shell=True, check=True)
    # print(process)


def stop_server():
    command = config.COMMAND_STOP
    if not command:
        raise AttributeError("command missing!")

    # this is not nice form, but easier than creating a dedicated startup script
    # no shell escape! Make sure no garbage is passed!
    process = subprocess.run(config.COMMAND_STOP, shell=True, check=True)
    # print(process)
