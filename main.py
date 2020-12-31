#!/usr/bin/env python3

import platform
import time

# pipenv decided to forbid specification of min versions
py_version = platform.python_version_tuple()
if int(py_version[0]) < 3 or int(py_version[1]) < 6:
    raise OSError("Python versions older than 3.6 are not supported")

from modules.exit_handler import keep_running
from modules import bot_commands

from requests.exceptions import ConnectionError


def main():
    print("Starting up...")
    print(f"My API status: {bot_commands.my_state}")

    # bot.infinity_polling()
    # this version will still escape with CTRL + S and user errors
    while keep_running:
        try:
            bot_commands.bot.polling(none_stop=True)
        except ConnectionError as e:
            print(f"TeleBot crashed with {e}! Restarting in 5 seconds...")
            time.sleep(5)


if __name__ == '__main__':
    main()
