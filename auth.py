from enum import Enum

import config


# TODO: use persistent storage
# add users at runtime via admin command?
# /allow ID    /forbid ID
# -> would need a persistent store
# -> would make config useless?
# -> Maybe only admin via config and users at runtime
# -> local user database

class Rank(Enum):
    UNKNOWN = 0
    USER = 1
    ADMIN = 2


def allowed(message, admin_only=False) -> bool:
    user_id = message.from_user.id
    collection = config.ADMINS if admin_only else zip(config.ADMINS, config.USERS)
    return user_id in collection


def get_users():
    return config.USERS


def get_admins():
    return config.ADMINS


def get_rank(user_id):
    if user_id in config.ADMINS:
        rank = "Admin"
    elif user_id in config.USERS:
        rank = "User"
    else:
        rank = "unkown"
    return rank
