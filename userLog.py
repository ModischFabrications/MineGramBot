from typing import Dict

from telebot.types import User

# TODO: should be persistent (local) storage
# sqllite3, redis, ...?

chat_partners: Dict[int, User] = {}


def log_contact(user: User):
    chat_partners[user.id] = user


def get_contacts():
    txt_out = "["
    for uid, user in chat_partners.items():
        txt_out += f"{user.first_name} {user.last_name} ({user.username}): {uid}, "
    txt_out += "]"
    return txt_out
