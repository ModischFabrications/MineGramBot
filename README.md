# MineGramBot

A Telegram bot to start minecraft servers from chat messages. Able to communicate by direct message or from a group
chat. Implements basic user identification to prevent unauthorized use. Won't store or share any details about chats,
groups or anything, should be fully GDPR conform!

Based on [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
and [McStatus](https://github.com/Dinnerbone/mcstatus), this bot wouldn't exist without them.

## Install

Use Python 3.6 or higher!

1. Download/checkout
2. `cd` into directory
3. add and customize config.py from *.template
4. `pipenv install`
5. add this program to your autostart of choice (see `start.sh`)
6. contact your bot instance on telegram or invite it into a group

Don't try to start two bot instances with the same token at the same time!

## Commands

- /start (start is called by telegram on first contact)
- c/cmd/commands
- rank [ID]
- start_server
- stop_server
- status

## Q & A

Q: Why no docker?  
A: I can't access host executables (minecraft) from inside a container

Q: Why not start the jar directly?  
A: Many minecraft launchers use custom launchers, don't want to break that

Q Why no /say commands or message bridge?  
A: I can't pass commands to or read output from the running server instance

## References

- https://core.telegram.org/bots
- https://www.mindk.com/blog/how-to-develop-a-chat-bot/

similar implementations:

- https://github.com/vendra/MinecraftTelegram (nice!)
- https://github.com/mate-amargo/telegram-mc-bot

### Telegram API lib comparison

- https://python-telegram-bot.org/ -> oldest, feels clunky
- https://github.com/aiogram/aiogram -> best, but least tutorials
- **https://github.com/eternnoir/pyTelegramBotAPI** -> nice midway


