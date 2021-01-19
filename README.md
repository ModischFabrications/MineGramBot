# MineGramBot

A Telegram bot to start, stop and monitor minecraft servers via chat. It is able to answer direct messages or commands
from a group chat. It implements basic user identification to prevent unauthorized use. It won't store or share any
details about chats, groups or anything (why should it?), so it should be fully GDPR conform!

Based on [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
and [McStatus](https://github.com/Dinnerbone/mcstatus), this bot wouldn't exist without them.

## Install

Use Python 3.6 or higher!

1. Download/checkout
2. `cd` into directory
3. add and customize config.py from *.template
4. `pipenv install` or `pipenv update`
5. add this program to your autostart of choice (see `start.sh`)
6. contact your bot instance on telegram or invite it into a group

Don't try to start two bot instances with the same token at the same time and don't share your token with anyone else!
Request a new token from Godfather if you are unsure if your token has been used somewhere else.

## Commands

Commands are displayed as a custom keyboard whenever you send /help to the bot, the following list is a summary:

- /start
- /commands
- /status
- /players
- /start_server
- /stop_server

## Q & A

Q: Why are you not using docker like all the (other) cool kids?  
A: I can't access host executables (minecraft) from inside a container

Q: Why are you not starting the .jar directly?  
A: Many minecraft versions use custom launchers, don't want to break that

Q Why are you not allowing /say commands or bridge messages?  
A: I can't pass commands to or read output from the running server instance because it's hidden behind the custom call.

## References

- https://core.telegram.org/bots
- https://www.mindk.com/blog/how-to-develop-a-chat-bot/
- https://github.com/vendra/MinecraftTelegram (nice!)
- https://github.com/mate-amargo/telegram-mc-bot

### Telegram API lib comparison

- https://python-telegram-bot.org/ -> oldest, feels clunky
- https://github.com/aiogram/aiogram -> fast and async, but few tutorials
- **https://github.com/eternnoir/pyTelegramBotAPI** -> nice midway and works
  flawlessly <sub><sup><sub><sup>[after bug hunting](https://github.com/eternnoir/pyTelegramBotAPI/issues/1058)
  . </sup></sub></sup></sub> 


