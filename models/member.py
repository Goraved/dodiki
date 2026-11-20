import time
from typing import List

from data import query


class Member:
    def __init__(self, member_id: int, name: str):
        self.name = name
        self.member_id = member_id


_CACHE_TTL = 60  # seconds; members change rarely
_cache = {"at": 0.0, "members": []}


def get_members() -> List[Member]:
    now = time.monotonic()
    if _cache["members"] and now - _cache["at"] < _CACHE_TTL:
        return list(_cache["members"])
    result = query("SELECT * FROM members") or []
    members = [Member(member_id=row[0], name=row[1]) for row in result]
    _cache.update(at=now, members=members)
    return list(members)
