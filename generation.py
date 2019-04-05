from datetime import date, timedelta

from data import write_days_list_into_db, get_members, get_rehearsals, delete_rehearsal


def get_list_of_days(start_from=None):
    if start_from is None:
        start_from = date.today()
    index = 0
    days = []
    weekdays = {1: 'Tuesday', 3: 'Thursday'}
    while len(days) < 30:
        day = start_from + timedelta(index)
        if day.weekday() in [1, 3]:
            if day < date.today():
                passed = True
            else:
                passed = False
            days.append({'date': day, 'weekday': weekdays[day.weekday()], 'member': '', 'passed': passed})
        index += 1
    return days


def set_members(days, member_id=None, half=False):
    members = get_members()
    member_index = members.index([_ for _ in members if _['id'] == member_id][0])
    if member_id is None:
        member_index = 0
    for day in days:
        day_index = days.index(day)
        # individual logic for 2 first days
        if day_index == 0:
            day['member'] = members[member_index]['id']
            continue
        elif day_index == 1:
            if not half:
                day['member'] = members[member_index]['id']
                continue
            else:
                member_index += 1
                if member_index > 3:
                    member_index = 0
                day['member'] = members[member_index]['id']
        # regular logic for the rest of days
        previous_pay = days[day_index - 1]['member']
        past_previous_pay = days[day_index - 2]['member']
        if previous_pay == past_previous_pay:
            member_index += 1
            if member_index > 3:
                member_index = 0
        day['member'] = members[member_index]['id']
    return days


def generate_list(from_date, from_member, half=False):
    days = get_list_of_days(from_date)
    set_members(days, from_member, half)
    write_days_list_into_db(days)
    return days


def get_future_rehearsals():
    return get_rehearsals(date.today())


def cancel_rehearsal(rehearsal_id):
    rehearsals = get_rehearsals(date.today())
    member = [_['member'] for _ in rehearsals if _['id'] == rehearsal_id][0]
    date_from = [_['date'] for _ in rehearsals if _['id'] == rehearsal_id][0] + timedelta(1)
    ind = rehearsals.index([_ for _ in rehearsals if _['id'] == rehearsal_id][0])
    half = False
    member_id = [_['id'] for _ in get_members() if _['name'] == member][0]
    if rehearsals[ind + 1]['member'] != member:
        half = True
    delete_rehearsal(rehearsal_id)
    generate_list(date_from, member_id, half)
