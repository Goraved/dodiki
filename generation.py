from datetime import date, timedelta
from typing import List

from models.member import get_members
from models.rehearsal import Rehearsal, get_rehearsals, write_days_list_into_db


def get_list_of_rehearsals(start_from: date = None) -> List[Rehearsal]:
    if start_from is None:
        start_from = date.today()
    index = 0
    rehearsals = []
    weekdays = {6: 'Sunday'}
    while len(rehearsals) < 12:
        day = start_from + timedelta(index)
        if day.weekday() in weekdays.keys():
            if day < date.today():
                passed = True
            else:
                passed = False
            rehearsals.append(
                Rehearsal(rehearsal_date=day, day_of_week=weekdays[day.weekday()], member_name='', passed=passed,
                          price=800, rehearsal_id=0))
        index += 1
    return rehearsals


def set_members(rehearsals: List[Rehearsal], member_id: int = 0, half: bool = False) -> List[Rehearsal]:
    # get all member ids
    members = [member.member_id for member in get_members()]
    # get index of requested member to start schedule
    # fall back to the first member if requested id is unknown
    member_index = members.index(member_id) if member_id in members else 0

    for rehearsal in rehearsals:
        rehearsal_index = rehearsals.index(rehearsal)

        # individual logic for 2 first days
        if rehearsal_index == 0:
            rehearsal.member_name = members[member_index]
            continue
        # TODO disable until 2 rehearsals per week
        # elif rehearsal_index == 1:
        #     if not half:
        #         rehearsal.member_name = members[member_index].member_id
        #         continue
        # else:
        #     member_index += 1
        #     if member_index > 3:
        #         member_index = 0
        #     rehearsal.member_name = members[member_index].member_id
        # regular logic for the rest of days

        previous_pay = members.index(rehearsals[rehearsal_index - 1].member_name)
        # TODO disable until 2 rehearsals per week
        # past_previous_pay = rehearsals[rehearsal_index - 2].member_name
        # if previous_pay == past_previous_pay:

        member_index = previous_pay + 1
        # Max count of member index
        if member_index >= len(members):
            member_index = 0

        rehearsal.member_name = members[member_index]

    return rehearsals


def generate_list(from_date: date, from_member: int = 1, half: bool = False) -> List[Rehearsal]:
    rehearsals = get_list_of_rehearsals(from_date)
    set_members(rehearsals, from_member, half)
    write_days_list_into_db(rehearsals)
    return rehearsals


def get_future_rehearsals() -> List[Rehearsal]:
    return get_rehearsals(date.today())


def cancel_rehearsal(rehearsal_id: int):
    rehearsals = get_rehearsals(date.today())
    target = next((r for r in rehearsals if r.rehearsal_id == rehearsal_id), None)
    if target is None:
        raise ValueError(f"No such rehearsal - {rehearsal_id}")
    date_from = target.rehearsal_date + timedelta(1)
    member_id = next((m.member_id for m in get_members() if m.name == target.member_name), 0)
    Rehearsal.delete_rehearsal(rehearsal_id)
    generate_list(date_from, member_id, False)
