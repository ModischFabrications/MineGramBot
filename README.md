# MineGramBot

## Install
1. Download/checkout
2. cd into directory
3. pipenv install
4. add/change config.py
5. add main.py to your autostart of choice



## Dev notes

### Roadmap
commands as buttons
https://www.mindk.com/blog/how-to-develop-a-chat-bot/ Step #6

resolve names to ids: search group for name, return id, group only implicit conversion 

get rank of all users
-> \rank Robin =>\rank 213243


"You are not allowed, ask an admin to add {ID} to users"
-> add at runtime via admin command? 
/allow ID    /forbid ID
-> would need a persistent store 
-> would make config useless? 
-> Maybe only admin via config and users at runtime

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




### References
https://core.telegram.org/bots
https://core.telegram.org/bots/api#message

https://www.mindk.com/blog/how-to-develop-a-chat-bot/

Very good similar implementation: 
https://github.com/vendra/MinecraftTelegram

https://github.com/mate-amargo/telegram-mc-bot

#### API libs
https://python-telegram-bot.org/ -> oldest, feels clunky
https://github.com/eternnoir/pyTelegramBotAPI -> nice midway, easy to use
https://github.com/aiogram/aiogram -> might be cool later for higher performance





