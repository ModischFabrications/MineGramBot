import random

import telebot
from telebot import apihelper
from telebot.types import CallbackQuery, Message

import config
from auth import allowed, get_rank, get_user_ranks, Rank
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

def check_allowed(m: Message, rank: Rank):
    if allowed(m.from_user.id, rank):
        return True

    bot.send_message(
        m.chat.id,
        f"Sorry {m.from_user.first_name}, but your rank {get_rank(m.from_user.id).name} is not high enough"
    )
    return False


@bot.middleware_handler(update_types=['message'])
def log_user(bot_instance, m):
    log_contact(m.from_user)


@bot.message_handler(func=lambda query: not allowed(query.from_user.id))
def block_forbidden(m):
    user_id = m.from_user.id
    print(f"Forbidden attempt from {user_id}")
    bot.send_message(
        m.chat.id,
        f"Sorry {m.from_user.first_name}, but you are {get_rank(user_id).name} (ID: {user_id})"
    )


@bot.message_handler(content_types=['new_chat_members', 'group_chat_created'])
def joined_group_command(m):
    if m.content_type == 'group_chat_created' or (
            m.content_type == 'new_chat_members' and m.new_chat_members[0].id == my_id):
        bot.send_message(m.chat.id, 'Thanks for inviting me to this group! Send /start for more')

    show_cmd(m)


@bot.message_handler(commands=['welcome', 'start', 'help', 'h'])
def welcome_command(m):
    if m.chat.type == "private":
        bot.send_message(m.chat.id,
                         f'Greetings {m.from_user.first_name}, your are {get_rank(m.from_user.id).name}!')
    elif m.chat.type in ("group", "supergroup"):
        bot.send_message(m.chat.id, 'Hello again everyone, I am ModischMinecraftBot')
    else:
        bot.send_message(m.chat.id, "Where am I?")

    bot.send_message(
        m.chat.id,
        f'I can start and stop a minecraft server for you.\n' +
        'Send /start to get this message again.\n'
    )
    show_cmd(m)


@bot.message_handler(commands=['cmd', "commands", "c"])
def show_cmd(m):
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


# -- mc server stuff

@bot.callback_query_handler(func=lambda call: call.data == 'status')
@bot.message_handler(commands=['status'])
def status_command(m):
    if type(m) == CallbackQuery:
        m = m.message

    bot.send_message(
        m.chat.id,
        f'Server status is {"unknown"}'
    )


# -- debug commands


@bot.message_handler(commands=['rank'])
def rank_command(m):
    user_id = m.from_user.id
    rank = get_rank(user_id)
    bot.reply_to(m, f'Your id is {user_id}, you are {rank.name}')


@bot.message_handler(commands=['list_ranks'])
def list_user_ranks(m):
    if not check_allowed(m, Rank.ADMIN):
        return

    bot.send_message(m.chat.id, f"Users: {get_user_ranks()}")


@bot.message_handler(commands=['list_contacts'])
def list_contacts(m):
    if not check_allowed(m, Rank.ADMIN):
        return

    bot.send_message(m.chat.id, get_contacts())


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
def fallback_text(m):
    answer = ("sorry?", "pardon?", "what?", "no idea...")
    bot.send_message(m.chat.id, f"{random.choice(answer)} Might want to get /help")


@bot.message_handler()
def fallback(m):
    print(m)


def main():
    print("Starting up...")
    print(f"My API status: {bot.get_me()}")
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
