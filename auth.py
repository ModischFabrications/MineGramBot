import config


# TODO: use persistent storage


def allowed(message) -> bool:
    user_id = message.from_user.id
    return user_id in zip(config.ADMINS, config.USERS)
