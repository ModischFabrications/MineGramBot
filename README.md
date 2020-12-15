# MineGramBot

## Install
1. Download/checkout
2. cd into directory
3. pipenv install
4. add/change config.py
5. add main.py to your autostart of choice



## Dev notes

### Roadmap
"You are not allowed, ask an admin to add {ID} to users"

add at runtime via admin command? 
/allow ID    /forbid ID
-> would need a persistent store 
-> would make config useless? 
-> Maybe only admin via config and users at runtime


Start/save/stop server/service
-> needs to be able to type commands in screen OR start server here

--> /say group messages in minecraft 




### References
https://core.telegram.org/bots
https://www.mindk.com/blog/how-to-develop-a-chat-bot/

Very good similar implementation: 
https://github.com/vendra/MinecraftTelegram

https://github.com/mate-amargo/telegram-mc-bot

#### API libs
https://python-telegram-bot.org/ -> oldest, feels clunky
https://github.com/eternnoir/pyTelegramBotAPI -> nice midway, easy to use
https://github.com/aiogram/aiogram -> might be cool later for higher performance





