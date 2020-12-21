import subprocess

import config


def start_server():
    command = config.COMMAND
    if not command:
        raise AttributeError("command missing!")

    process = subprocess.run(config.COMMAND, shell=True, capture_output=True, text=True)
    print(process)
