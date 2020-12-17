import random

import telebot
from telebot import apihelper
from telebot.types import CallbackQuery

import config
from auth import allowed, get_rank, get_admins, get_users
from userLog import log_contact, get_contacts

apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(config.TOKEN)

my_id = bot.get_me().id


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
def log_user(bot_instance, m):
    log_contact(m.from_user)


@bot.message_handler(func=lambda query: allowed(query))
def block_forbidden(m):
    print(f"Forbidden attempt from {m.from_user.id}")
    bot.send_message(
        m.chat.id,
        f"Sorry {m.from_user.first_name}, but you are not a registered user (ID: {m.from_user.id})"
    )


@bot.message_handler(content_types=['new_chat_members', 'group_chat_created'])
def joined_group_command(m):
    if m.content_type == 'group_chat_created' or (
            m.content_type == 'new_chat_members' and m.new_chat_members[0].id == my_id):
        bot.send_message(m.chat.id, 'Thanks for inviting me to this group!')

    cmd_command(m)


@bot.message_handler(commands=['welcome', 'start', 'hello', 'help', 'h'])
def welcome_command(m):
    if m.chat.type == "private":
        bot.send_message(m.chat.id,
                         f'Greetings {m.from_user.first_name}, your are {get_rank(m.from_user.id)}!')
    elif m.chat.type in ("group", "supergroup"):
        bot.send_message(m.chat.id, 'Hello there everyone')
    else:
        bot.send_message(m.chat.id, "Where am I?")

    bot.send_message(
        m.chat.id,
        f'I can start and stop a minecraft server for you.\n' +
        'To get this message again send /start.\n'
    )
    cmd_command(m)


@bot.message_handler(commands=['cmd', "commands", "c"])
def cmd_command(m):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton("/start_server", callback_data='start_server'),
        telebot.types.InlineKeyboardButton("/status", callback_data='status'),
        telebot.types.InlineKeyboardButton("/stop_server", callback_data='stop_server')
    )

    bot.send_message(
        m.chat.id,
        f'Commands:',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['list_contacts'])
def list_contacts(m):
    bot.send_message(m.chat.id, get_contacts())


@bot.message_handler(commands=['list_ranks'])
def list_ranks(m):
    bot.send_message(m.chat.id, f"Users: {get_users()}\nAdmins: {get_admins()}")


@bot.callback_query_handler(func=lambda call: call.data == 'status')
@bot.message_handler(commands=['status'])
def status_command(m):
    if type(m) == CallbackQuery:
        m = m.m

    bot.send_message(
        m.chat.id,
        f'Server status is {"unknown"}'
    )


@bot.message_handler(commands=['rank'])
def rank_command(m):
    user_id = m.from_user.id
    rank = get_rank(user_id)
    bot.reply_to(m, f'Your id is {user_id}, you are {rank}')


# --- fallback handlers

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    print(f"Callback: {call}")
    bot.send_message(
        call.m.chat.id,
        f"{call.data} is not implemented yet..."
    )


# last one by design!
@bot.message_handler(content_types=['text'])
def fallback_text(m):
    answer = ("sorry?", "pardon?", "what?", "no idea...")
    bot.send_message(m.chat.id, f"{random.choice(answer)} Might want to get /help")


@bot.message_handler()
def fallback(m):
    print(m)


def main():
    print("Starting up...")
    print(f"My API status: {bot.get_me()}")
    print(f"Admins: {config.ADMINS}")
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
