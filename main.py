#!/usr/bin/env python3

import logging
import platform
import random
import signal
import time

# pipenv decided to forbid specification of min versions
py_version = platform.python_version_tuple()
if int(py_version[0]) < 3 or int(py_version[1]) < 6:
    raise OSError("Python versions older than 3.6 are not supported")

keep_running = True


def exit(sig, frame):
    global keep_running
    keep_running = False


signal.signal(signal.SIGINT, exit)

import telebot
from requests.exceptions import ConnectionError
from telebot import apihelper
from telebot.types import Message

import config
from modules.auth import Rank, Auth
from modules.contactLog import ContactLog
from modules.mc_server_adapter import start_server, stop_server
from modules.mc_server_observer import State, MCServerObserver
from modules.observer_scheduler import MCServerObserverScheduler

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console.

apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(config.TOKEN)

my_id = bot.get_me().id

auth = Auth(config.USERS)
observer = MCServerObserver(config.LOCAL_ADDRESS)
userLog = ContactLog()


def forbidden_access(m: Message, rank: Rank):
    if auth.allowed(m.from_user.id, rank):
        return False

    bot.reply_to(
        m,
        f"Sorry {m.from_user.first_name}, but your rank {auth.get_rank(m.from_user.id).name} is not high enough"
    )
    return True


@bot.middleware_handler(update_types=['message'])
def log_user(bot_instance, m):
    userLog.log(m.from_user)


@bot.message_handler(func=lambda query: not auth.allowed(query.from_user.id))
def block_forbidden(m):
    user_id = m.from_user.id
    print(f"Forbidden attempt from {user_id}")
    bot.reply_to(m, f"Sorry {m.from_user.first_name}, but you are {auth.get_rank(user_id).name} (ID: {user_id})")


@bot.message_handler(func=lambda query: (time.time() - query.date > 60))
def ignore_old(m):
    user_id = m.from_user.id
    print(f"Old attempt from {user_id}")
    bot.reply_to(m, f"Sorry {m.from_user.first_name}, but I was not running. Send again if it's still relevant")


@bot.message_handler(content_types=['new_chat_members', 'group_chat_created'])
def joined_group_command(m):
    if m.content_type == 'group_chat_created' or (
            m.content_type == 'new_chat_members' and m.new_chat_members[0].id == my_id):
        bot.send_message(m.chat.id, 'Thanks for inviting me to this group! Send /start for more')

    show_cmd(m)


@bot.message_handler(commands=['welcome', 'start', 'help', 'h'])
def welcome_command(m):
    urank = auth.get_rank(m.from_user.id)

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
        telebot.types.KeyboardButton("/status"),
        telebot.types.KeyboardButton("/players"),
        telebot.types.KeyboardButton("/stop_server")
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
        telebot.types.KeyboardButton("/status"),
        telebot.types.KeyboardButton("/players"),
        telebot.types.KeyboardButton("/stop_server")
    )
    keyboard.row(
        telebot.types.KeyboardButton("/list_contacts"),
        telebot.types.KeyboardButton("/list_ranks"),
        telebot.types.KeyboardButton("/help")
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
        f'Server status is [querying]..'
    )

    bot.edit_message_text(f'Server is {observer.get_state_str()}', chat_id=msg_send.chat.id,
                          message_id=msg_send.message_id)


@bot.message_handler(commands=['players', 'list_players'])
def players_command(m):
    msg_send = bot.send_message(
        m.chat.id,
        f'Player list is [querying]..'
    )

    bot.edit_message_text(f'Players: {observer.get_players()}', chat_id=msg_send.chat.id,
                          message_id=msg_send.message_id)


@bot.message_handler(commands=['start_server'])
def start_server_command(m):
    if forbidden_access(m, Rank.OP):
        return

    state = observer.get_state()[0]
    if state != State.OFFLINE:
        bot.reply_to(m, f"Server is already {observer.get_state_str()}")
        return

    start_server()

    msg_send = bot.send_message(
        m.chat.id,
        f"Server is starting up, wait a few minutes..."
    )
    on_success = lambda: bot.edit_message_text(f'Server is {observer.get_state_str()}', chat_id=msg_send.chat.id,
                                               message_id=msg_send.message_id)

    on_error = lambda: bot.edit_message_text(f'Server is unresponsive, state is unknown', chat_id=msg_send.chat.id,
                                             message_id=msg_send.message_id)

    MCServerObserverScheduler(observer).call_when_online(on_success, on_error)


@bot.message_handler(commands=['stop_server'])
def stop_server_command(m):
    if forbidden_access(m, Rank.OP):
        return

    stop_server()

    bot.send_message(
        m.chat.id,
        f"Server is terminating"
    )


# -- debug commands


@bot.message_handler(commands=['rank'])
def rank_command(m):
    user_id = m.from_user.id
    rank = auth.get_rank(user_id)
    bot.reply_to(m, f'Your id is {user_id}, you are {rank.name}')


@bot.message_handler(commands=['list_ranks'])
def list_user_ranks(m):
    if forbidden_access(m, Rank.ADMIN):
        return

    bot.send_message(m.chat.id, f"Users: {auth.get_user_ranks()}")


@bot.message_handler(commands=['list_contacts'])
def list_contacts(m):
    if forbidden_access(m, Rank.ADMIN):
        return

    bot.send_message(m.chat.id, userLog.get())


# --- fallback handlers

# last one by design!
@bot.message_handler(content_types=['text'])
def fallback_text(m):
    answer = ("sorry?", "pardon?", "what?", "no idea...")
    bot.reply_to(m, f"{random.choice(answer)} Might want to get /help")


@bot.message_handler()
def fallback(m):
    print(m)


def main():
    print("Starting up...")
    print(f"My API status: {bot.get_me()}")

    # bot.infinity_polling()
    # this version will still escape with CTRL + S and user errors
    while keep_running:
        try:
            bot.polling(none_stop=True)
        except ConnectionError as e:
            print(f"TeleBot crashed with {e}! Restarting in 5 seconds...")
            time.sleep(5)


if __name__ == '__main__':
    main()
