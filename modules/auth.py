from enum import IntEnum
from typing import Dict


# matrix of permissions might be even cooler
class Rank(IntEnum):
    BLOCKED = -1
    UNKNOWN = 0
    USER = 1
    OP = 2
    ADMIN = 3


# could use persistent storage to add users at runtime via admin command
# /set_rank ID RANK
# -> would need a persistent store
# -> would make config useless?
# -> Maybe only admin via config and users at runtime
# -> local user database

class Auth:
    def __init__(self, users: Dict[int, int]):
        self._users: Dict[int, Rank] = {uid: Rank(rank) for (uid, rank) in users.items()}

    def allowed(self, user_id, min_rank=Rank.USER) -> bool:
        return user_id in self._users.keys() and self._users[user_id] >= min_rank

    def get_user_ranks(self):
        return {uid: rank.name for (uid, rank) in self._users.items()}

    def get_rank(self, user_id) -> Rank:
        return Rank(self._users.get(user_id, Rank.UNKNOWN))
