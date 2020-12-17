# MineGramBot

## Install
1. Download/checkout
2. cd into directory
3. pipenv install
4. add/change config.py
5. add main.py to your autostart of choice

## Commands
- hello/h/help/start (start is called by telegram on startup)
- c/cmd/commands
- rank [ID]
- start_server
- stop_server
- status

## Q & A
Q: Why no docker?  
A: Because I can't access executables (minecraft!) from inside a container


## Dev notes

### Roadmap

check server status (online/offline, n_players, uptime)
-> verbose mode prints joined players -> would need \hide (me) for privacy minded people

Start/save/stop server/service -> needs to be able to type commands in screen OR start server here

--> /say group messages in minecraft

resolve names to ids: search group for name, return id, group only implicit conversion -> message entity type "mention"

get rank of all users -> \rank Robin =>\rank 213243

eastereggs (send fortnite dancing steve gif?)

add telegram badge

accept inline commands
https://github.com/eternnoir/pyTelegramBotAPI#inline-mode

### References

- https://core.telegram.org/bots
- https://core.telegram.org/bots/api#message

- https://www.mindk.com/blog/how-to-develop-a-chat-bot/

similar implementations:

- https://github.com/vendra/MinecraftTelegram (nice!)
- https://github.com/mate-amargo/telegram-mc-bot

#### API libs
- https://python-telegram-bot.org/ -> oldest, feels clunky
- https://github.com/aiogram/aiogram -> best, but least tutorials
- **https://github.com/eternnoir/pyTelegramBotAPI** -> nice midway, easy to use and used


