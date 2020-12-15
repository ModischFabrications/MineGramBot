import telebot

import config

bot = telebot.TeleBot(config.TOKEN)


# if verbose: send updates on change
# send on /status
# from mcstatus import MinecraftServer
# server = MinecraftServer.lookup("127.0.0.1:25565")
# server = MinecraftServer(MINECRAFT_SERVER_IP, MINECRAFT_SERVER_PORT)

# query = server.query()
# query.players.names

# status = server.status()
# status.players.online


def is_user(message) -> bool:
    user_id = message.from_user.id
    return user_id in zip(config.ADMINS, config.USERS)


@bot.message_handler(commands=['start', 'hello', 'help', 'h'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        f'Greetings {message.from_user.first_name}! \n'
        f'I can start and stop a minecraft server for you.\n' +
        'To start send /start.\n' +
        'To stop send /stop.\n' +
        'To get help press /help.'
    )


@bot.message_handler(commands=['status'])
def status_command(message):
    bot.send_message(
        message.chat.id,
        f'I am still alive.\n Server status is {"NOT IMPLEMENTED"}'
    )


@bot.message_handler(commands=['rank'])
def rank_command(message):
    user_id = message.from_user.id

    if user_id in config.ADMINS:
        rank = "ADMIN"
    elif user_id in config.USERS:
        rank = "USER"
    else:
        rank = "Noone"

    bot.reply_to(message, f'Your id is {user_id}, you are {rank}')


@bot.message_handler(commands=['echo'])
def echo_command(message):
    bot.reply_to(message, f'You said {message.text}')


@bot.message_handler(commands=['test'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            "Message the developer", url='telegram.me/RobinMod'
        )
    )
    bot.send_message(
        message.chat.id,
        '1) To receive a list of available currencies press /exchange.\n' +
        '2) Click on the currency you are interested in.\n' +
        '3) You will receive a message containing information regarding the source and the target currencies, ' +
        'buying rates and selling rates.\n' +
        '4) Click “Update” to receive the current information regarding the request. ' +
        'The bot will also show the difference between the previous and the current exchange rates.\n' +
        '5) The bot supports inline. Type @<botusername> in any chat and the first letters of a currency.',
        reply_markup=keyboard
    )


def main():
    print("Starting up...")
    print(f"My API status: {bot.get_me()}")
    print(f"Admins: {config.ADMINS}")
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
