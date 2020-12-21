import math
import random
import time

import telebot
from telebot import apihelper
from telebot.types import Message

import config
from modules.auth import allowed, get_rank, get_user_ranks, Rank
from modules.mc_server_adapter import start_server
from modules.mc_server_observer import get_status
from modules.userLog import log_contact, get_contacts

apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(config.TOKEN)

my_id = bot.get_me().id

last_start = -math.inf


def forbidden_access(m: Message, rank: Rank):
    if allowed(m.from_user.id, rank):
        return False

    bot.reply_to(
        m,
        f"Sorry {m.from_user.first_name}, but your rank {get_rank(m.from_user.id).name} is not high enough"
    )
    return True


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
    urank = get_rank(m.from_user.id)

    if m.chat.type == "private":
        bot.send_message(m.chat.id,
                         f'Greetings {m.from_user.first_name}, your are {urank.name.lower()}!')
    elif m.chat.type in ("group", "supergroup"):
        bot.send_message(m.chat.id, 'Hello again everyone, I am ModischMinecraftBot')
    else:
        bot.send_message(m.chat.id, "Where am I?")

    bot.send_message(
        m.chat.id,
        f'I can start and stop a minecraft server for you.\n' +
        'Send /start to get this message again.\n'
    )

    if urank == Rank.OP: show_cmd(m)
    if urank == Rank.ADMIN: show_ex_cmd(m)


@bot.message_handler(commands=['cmd', "commands", "c"])
def show_cmd(m):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row(
        telebot.types.KeyboardButton("/start_server"),
        telebot.types.InlineKeyboardButton("/status"),
        telebot.types.InlineKeyboardButton("/stop_server")
    )

    bot.send_message(
        m.chat.id,
        f'What do you want me to do?',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['ex_cmd', "extended_commands", "xc"])
def show_ex_cmd(m):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row(
        telebot.types.KeyboardButton("/start_server"),
        telebot.types.InlineKeyboardButton("/status"),
        telebot.types.InlineKeyboardButton("/stop_server")
    )
    keyboard.row(
        telebot.types.KeyboardButton("/list_contacts"),
        telebot.types.InlineKeyboardButton("/list_ranks"),
        telebot.types.InlineKeyboardButton("/help")
    )

    bot.send_message(
        m.chat.id,
        f'What do you want me to do?',
        reply_markup=keyboard
    )


# -- mc server stuff

@bot.message_handler(commands=['status'])
def status_command(m):
    msg_send = bot.send_message(
        m.chat.id,
        f'Server status is [querying]'
    )

    bot.edit_message_text(f'Server status is {get_status()}', chat_id=msg_send.chat.id, message_id=msg_send.message_id)


@bot.message_handler(commands=['start_server'])
def start_server_command(m):
    if forbidden_access(m, Rank.OP):
        return

    global last_start
    now = time.perf_counter()
    if now - last_start < config.CMD_COOLDOWN_S:
        bot.reply_to(m, "Can't do, server is still starting...")
        return
    last_start = now

    start_server()

    bot.send_message(
        m.chat.id,
        f"server is starting..."
    )
    # TODO: check status after delay and update message?


@bot.message_handler(commands=['stop_server'])
def stop_server_command(m):
    if forbidden_access(m, Rank.OP):
        return

    bot.send_message(
        m.chat.id,
        f"start_server isn't done yet, sorry"
    )


# -- debug commands


@bot.message_handler(commands=['rank'])
def rank_command(m):
    user_id = m.from_user.id
    rank = get_rank(user_id)
    bot.reply_to(m, f'Your id is {user_id}, you are {rank.name}')


@bot.message_handler(commands=['list_ranks'])
def list_user_ranks(m):
    if forbidden_access(m, Rank.ADMIN):
        return

    bot.send_message(m.chat.id, f"Users: {get_user_ranks()}")


@bot.message_handler(commands=['list_contacts'])
def list_contacts(m):
    if forbidden_access(m, Rank.ADMIN):
        return

    bot.send_message(m.chat.id, get_contacts())


# --- fallback handlers

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
