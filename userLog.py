from typing import Dict

from telebot.types import User

# TODO: should be persistent (local) storage
# sqllite3, redis, ...?

chat_partners: Dict[int, User] = {}


def add_user(user: User):
    chat_partners[user.id] = user


def print_users():
    txt_out = "["
    for uid, user in chat_partners.items():
        txt_out += f"{user.first_name} {user.last_name} ({user.username}): {uid}, "
    txt_out += "]"
    print(txt_out)
