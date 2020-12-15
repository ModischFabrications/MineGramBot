# MineGramBot

## Install
1. Download/checkout
2. cd into directory
3. pipenv install
4. add/change config.py
5. add main.py to your autostart of choice

## Commands
- hello/h/help/start (start is called by telegram on startup)
- rank [ID]
- stop
- status

## Q & A
Q: Why no docker?  
A: Because I can't access executables (minecraft!) from inside a container


## Dev notes

### Roadmap
commands as buttons
https://www.mindk.com/blog/how-to-develop-a-chat-bot/ Step #6

accept inline commands
https://github.com/eternnoir/pyTelegramBotAPI#inline-mode

resolve names to ids: search group for name, return id, group only implicit conversion 

get rank of all users
-> \rank Robin =>\rank 213243

check isUser first and block access if not
https://github.com/eternnoir/pyTelegramBotAPI#middleware-handler

"You are not allowed, ask an admin to add {ID} to users"
-> add at runtime via admin command? 
/allow ID    /forbid ID
-> would need a persistent store 
-> would make config useless? 
-> Maybe only admin via config and users at runtime
-> local user database

differentiate between private chat and group
-> "thanks for inviting me here" vs "hello {user}"
if message.chat.type == "private":
	# private chat message

elif message.chat.type in ("group", "supergroup"):
	# group chat message

check server status (online/offline, n_players, uptime)
-> verbose mode prints joined players
-> would need \hide (me) for privacy minded people


Start/save/stop server/service
-> needs to be able to type commands in screen OR start server here

--> /say group messages in minecraft 


eastereggs (send fortnite dancing steve gif?)

add telegram badge


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


