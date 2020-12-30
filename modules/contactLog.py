from typing import Dict

from telebot.types import User


# TODO: should be persistent (local) storage
# sqllite3, redis, ...?

class ContactLog:

    def __init__(self):
        self._chat_partners: Dict[int, User] = {}

    def log(self, user: User):
        self._chat_partners[user.id] = user

    def get(self):
        txt_out = "["
        for uid, user in self._chat_partners.items():
            txt_out += f"{user.first_name} {user.last_name} ({user.username}): {uid}, "
        txt_out += "]"
        return txt_out
