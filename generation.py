from datetime import date, timedelta
from typing import List

from models.member import get_members
from models.rehearsal import Rehearsal, get_rehearsals, write_days_list_into_db


def get_list_of_rehearsals(start_from: date = None) -> List[Rehearsal]:
    if start_from is None:
        start_from = date.today()
    index = 0
    rehearsals = []
    weekdays = {3: 'Thursday', 6: 'Sunday'}
    while len(rehearsals) < 30:
        day = start_from + timedelta(index)
        if day.weekday() in (3, 6):
            if day < date.today():
                passed = True
            else:
                passed = False
            rehearsals.append(
                Rehearsal(rehearsal_date=day, day_of_week=weekdays[day.weekday()], member_name='', passed=passed,
                          price=440, rehearsal_id=0))
        index += 1
    return rehearsals


def set_members(rehearsals: List[Rehearsal], member_id: int = None, half: bool = False) -> List[Rehearsal]:
    members = get_members()
    member_index = members.index([member for member in members if member.member_id == member_id][0])
    if member_id is None:
        member_index = 0
    for rehearsal in rehearsals:
        rehearsal_index = rehearsals.index(rehearsal)
        # individual logic for 2 first days
        if rehearsal_index == 0:
            rehearsal.member_name = members[member_index].member_id
            continue
        elif rehearsal_index == 1:
            if not half:
                rehearsal.member_name = members[member_index].member_id
                continue
            else:
                member_index += 1
                if member_index > 3:
                    member_index = 0
                rehearsal.member_name = members[member_index].member_id
        # regular logic for the rest of days
        previous_pay = rehearsals[rehearsal_index - 1].member_name
        past_previous_pay = rehearsals[rehearsal_index - 2].member_name
        if previous_pay == past_previous_pay:
            member_index += 1
            if member_index > 3:
                member_index = 0
        rehearsal.member_name = members[member_index].member_id
    return rehearsals


def generate_list(from_date, from_member, half=False) -> List[Rehearsal]:
    rehearsals = get_list_of_rehearsals(from_date)
    set_members(rehearsals, from_member, half)
    write_days_list_into_db(rehearsals)
    return rehearsals


def get_future_rehearsals() -> List[Rehearsal]:
    return get_rehearsals(date.today())


def cancel_rehearsal(rehearsal_id: id):
    rehearsals = get_rehearsals(date.today())
    member_name = [rehearsal.member_name for rehearsal in rehearsals if rehearsal.rehearsal_id == rehearsal_id][0]
    date_from = [rehearsal.rehearsal_date for rehearsal in rehearsals if rehearsal.rehearsal_id == rehearsal_id][
                    0] + timedelta(1)
    ind = rehearsals.index([rehearsal for rehearsal in rehearsals if rehearsal.rehearsal_id == rehearsal_id][0])
    half = False
    member_id = [member.member_id for member in get_members() if member.name == member_name][0]
    if rehearsals[ind + 1].member_name != member_name:
        half = True
    Rehearsal.delete_rehearsal(rehearsal_id)
    generate_list(date_from, member_id, half)
