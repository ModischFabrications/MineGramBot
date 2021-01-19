#!/usr/bin/env python3

import platform

# pipenv decided to forbid specification of min versions, so we need to check manually to prevent weird errors
py_version = platform.python_version_tuple()
if int(py_version[0]) < 3 or int(py_version[1]) < 6:
    raise OSError("Python versions older than 3.6 are not supported")

from modules import bot_commands


def main():
    print("Starting up...")
    print(f"My API status: {bot_commands.my_state}")

    print("Press CTRL+C to stop server")
    # this version will still escape on keyboard interrupt but ignores user errors
    bot_commands.bot.infinity_polling()


if __name__ == '__main__':
    main()
