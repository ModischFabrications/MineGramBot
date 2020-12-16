import random

import telebot
from telebot import apihelper
from telebot.types import CallbackQuery

import config
from auth import allowed
from userLog import add_user, print_users

apihelper.ENABLE_MIDDLEWARE = True
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


@bot.middleware_handler(update_types=['message'])
def log_user(bot_instance, message):
    add_user(message.from_user)
    print_users()


@bot.message_handler(func=lambda query: allowed(query))
def block_forbidden(message):
    print(f"Forbidden attempt from {message.from_user.id}")
    bot.send_message(
        message.chat.id,
        f"Sorry {message.from_user.first_name}, but you are not a registered user (ID: {message.from_user.id})"
    )


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
    cmd_command(message)


@bot.message_handler(commands=['cmd', "commands", "c"])
def cmd_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton("help", callback_data='help'),
        telebot.types.InlineKeyboardButton("status", callback_data='status'),
        telebot.types.InlineKeyboardButton("rank", callback_data='rank')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton("start_server", callback_data='start_server'),
        telebot.types.InlineKeyboardButton("stop_server", callback_data='stop_server')
    )

    bot.send_message(
        message.chat.id,
        f'Commands:',
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data == 'status')
@bot.message_handler(commands=['status'])
def status_command(message):
    if type(message) == CallbackQuery:
        message = message.message

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


# --- fallback handlers

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    print(f"Callback: {call}")
    bot.send_message(
        call.message.chat.id,
        f"{call.data} is not implemented yet..."
    )


# last one by design!
@bot.message_handler(content_types=['text'])
def fallback(message):
    answer = ("sorry?", "pardon?", "what?", "no idea...")
    bot.send_message(message.chat.id, f"{random.choice(answer)} Might want to get /help")


def main():
    print("Starting up...")
    print(f"My API status: {bot.get_me()}")
    print(f"Admins: {config.ADMINS}")
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
