from enum import Enum

import config


# TODO: use persistent storage
# add users at runtime via admin command?
# /set_rank ID RANK
# -> would need a persistent store
# -> would make config useless?
# -> Maybe only admin via config and users at runtime
# -> local user database

class Rank(Enum):
    BLOCKED = -1
    UNKOWN = 0
    USER = 1
    ADMIN = 2


def allowed(message, min_rank=1) -> bool:
    user_id = message.from_user.id
    return user_id in config.USERS.keys() and config.USERS[user_id] >= min_rank


def get_ranks():
    return config.USERS


def get_rank(user_id):
    return Rank(config.USERS.get(user_id, Rank.UNKOWN))
