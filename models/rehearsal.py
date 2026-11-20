from datetime import date
from typing import List

from data import query
from models.member import get_members


class Rehearsal:
    def __init__(
        self,
        rehearsal_id: int,
        rehearsal_date: date,
        member_name: str,
        day_of_week: str,
        passed: bool,
        price: int,
    ):
        self.price = price
        self.passed = passed
        self.day_of_week = day_of_week
        self.member_name = member_name
        self.rehearsal_date = rehearsal_date
        self.rehearsal_id = rehearsal_id

    @staticmethod
    def set_passed_rehearsals():
        query("UPDATE days SET passed = 1 WHERE date < %s", (date.today(),))

    @staticmethod
    def delete_rehearsal(rehearsal_id: int):
        query("DELETE FROM days WHERE id = %s", (int(rehearsal_id),))

    @staticmethod
    def swap_rehearsal_members(swap_ids: tuple):
        first, second = int(swap_ids[0]), int(swap_ids[1])
        if first == second:
            raise ValueError("Cannot swap a rehearsal with itself")
        result = query(
            "SELECT id, member_id FROM days WHERE id IN (%s, %s)", (first, second)
        )
        members = {row[0]: row[1] for row in result}
        if len(members) != 2:
            raise ValueError("Rehearsal not found")
        # single statement => atomic swap
        query(
            "UPDATE days SET member_id = CASE id WHEN %s THEN %s WHEN %s THEN %s END "
            "WHERE id IN (%s, %s)",
            (first, members[second], second, members[first], first, second),
        )

    @staticmethod
    def delete_not_relevant_days(from_date: date):
        query("DELETE FROM days WHERE date >= %s", (from_date,))


def write_days_list_into_db(rehearsals: List[Rehearsal]):
    Rehearsal.delete_not_relevant_days(rehearsals[0].rehearsal_date)
    if not rehearsals:
        return
    placeholders = ", ".join(["(0, %s, %s, %s, %s, %s)"] * len(rehearsals))
    params = []
    for rehearsal in rehearsals:
        params += [
            rehearsal.rehearsal_date,
            rehearsal.day_of_week,
            rehearsal.member_name,
            int(rehearsal.passed),
            rehearsal.price,
        ]
    query("INSERT INTO days VALUES " + placeholders, tuple(params))


def get_rehearsals(from_date: date) -> List[Rehearsal]:
    rehearsals = []
    members = get_members()
    result = query(
        "SELECT id, date, member_id, price, day_of_week, passed FROM days "
        "WHERE date >= %s AND passed = 0",
        (from_date,),
    )
    for row in result:
        member = next((m.name for m in members if m.member_id == row[2]), "")
        rehearsals.append(
            Rehearsal(
                rehearsal_id=row[0],
                rehearsal_date=row[1],
                member_name=member,
                price=row[3],
                day_of_week=row[4],
                passed=row[5],
            )
        )
    return rehearsals
