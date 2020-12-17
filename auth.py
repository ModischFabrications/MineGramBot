from enum import IntEnum
from typing import Dict

import config


# only class to know about authentication (config.USERS)
# knows nothing about telebot and messages!


class Rank(IntEnum):
    BLOCKED = -1
    UNKOWN = 0
    USER = 1
    ADMIN = 2


# TODO: use persistent storage
# add users at runtime via admin command?
# /set_rank ID RANK
# -> would need a persistent store
# -> would make config useless?
# -> Maybe only admin via config and users at runtime
# -> local user database

users: Dict[int, Rank] = {uid: Rank(rank) for (uid, rank) in config.USERS.items()}


def allowed(user_id, min_rank=Rank.USER) -> bool:
    return user_id in users.keys() and users[user_id] >= min_rank


def get_user_ranks():
    return {uid: rank.name for (uid, rank) in users.items()}


def get_rank(user_id):
    return Rank(users.get(user_id, Rank.UNKOWN))
