from typing import List

from data import query


class Member:
    def __init__(self, member_id: int, name: str):
        self.name = name
        self.member_id = member_id


def get_members() -> List[Member]:
    members = []
    result = query("SELECT * FROM members")
    for row in result:
        members.append(Member(member_id=row[0], name=row[1]))
    return members
