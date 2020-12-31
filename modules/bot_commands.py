import logging
import random
import time

import telebot
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

my_state = bot.get_me()

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


# -- commands
# reply_to to direct commands, send_message for generic updates meant for everybody

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
            m.content_type == 'new_chat_members' and m.new_chat_members[0].id == my_state.id):
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

    show_cmd(m)


def add_c_row_users(keyboard):
    keyboard.row(
        telebot.types.KeyboardButton("/status"),
        telebot.types.KeyboardButton("/players")
    )


def add_c_row_op(keyboard):
    keyboard.row(
        telebot.types.KeyboardButton("/start_server"),
        telebot.types.KeyboardButton("/stop_server")
    )


def add_c_row_admin(keyboard):
    keyboard.row(
        telebot.types.KeyboardButton("/list_contacts"),
        telebot.types.KeyboardButton("/list_ranks")
    )


@bot.message_handler(commands=['cmd', "commands", "c"])
def show_cmd(m):
    urank = auth.get_rank(m.from_user.id)

    keyboard = telebot.types.ReplyKeyboardMarkup()

    if urank >= Rank.USER: add_c_row_users(keyboard)
    if urank >= Rank.OP: add_c_row_op(keyboard)
    if urank >= Rank.ADMIN: add_c_row_admin(keyboard)

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
    observer.assume_starting(config.MAX_TIME_TO_START__S)

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
    logger.wa(f"Received unexpected message: {m}")
