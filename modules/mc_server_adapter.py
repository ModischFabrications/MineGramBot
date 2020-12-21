import subprocess

import config


def start_server():
    command = config.COMMAND
    if not command:
        raise AttributeError("command missing!")

    # this is not nice form, but easier than creating a dedicated startup script
    # no shell escape! Make sure no garbage is passed!
    process = subprocess.run(config.COMMAND, shell=True, capture_output=True, text=True)
    print(process)
