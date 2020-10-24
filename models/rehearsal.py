from datetime import date
from typing import List

from data import query
from models.member import get_members


class Rehearsal:
    def __init__(self, rehearsal_id: int, rehearsal_date: date, member_name: str, day_of_week: str, passed: bool,
                 price: int):
        self.price = price
        self.passed = passed
        self.day_of_week = day_of_week
        self.member_name = member_name
        self.rehearsal_date = rehearsal_date
        self.rehearsal_id = rehearsal_id

    @staticmethod
    def set_passed_rehearsals():
        today = date.today().strftime('%Y%m%d')
        query(f'UPDATE days SET passed = 1 WHERE date < {today}')

    @staticmethod
    def delete_rehearsal(rehearsal_id: int):
        query(f'DELETE FROM days WHERE id = {rehearsal_id}')

    @staticmethod
    def swap_rehearsal_members(swap_ids: tuple):
        rehearsals = []
        cur = query(f'SELECT id, member_id FROM days WHERE id in ({swap_ids[0]},{swap_ids[1]})')
        for row in cur.fetchall():
            rehearsals.append({'id': row[0], 'member_id': row[1]})
        query(f"UPDATE days SET member_id = {rehearsals[1]['member_id']} WHERE id = {rehearsals[0]['id']};")
        query(f"UPDATE days SET member_id = {rehearsals[0]['member_id']} WHERE id = {rehearsals[1]['id']};")

    @staticmethod
    def delete_not_relevant_days(from_date: date):
        query(f"DELETE FROM days WHERE date >= '{from_date}'")


def write_days_list_into_db(rehearsals: List[Rehearsal]):
    Rehearsal.delete_not_relevant_days(rehearsals[0].rehearsal_date)
    str_query = 'INSERT INTO days VALUES '
    day_data = [f"(0,'{rehearsal.rehearsal_date}','{rehearsal.day_of_week}','{rehearsal.member_name}'" \
                f",{rehearsal.passed}, {rehearsal.price})" for rehearsal in rehearsals]
    str_query += ', '.join(day_data)
    query(str_query)


def get_rehearsals(from_date: date) -> List[Rehearsal]:
    rehearsals = []
    members = get_members()
    cur = query(f'SELECT id, date, member_id, price, day_of_week, passed FROM days '
                f'WHERE date >= {from_date} AND passed = 0')
    for row in cur.fetchall():
        member = [member.name for member in members if member.member_id == row[2]][0]
        rehearsals.append(Rehearsal(rehearsal_id=row[0], rehearsal_date=row[1], member_name=member, price=row[3],
                                    day_of_week=row[4], passed=row[5]))
    return rehearsals
