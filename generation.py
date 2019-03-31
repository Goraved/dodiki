from datetime import date, timedelta

from data import write_days_list_into_db, get_members


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


def set_members(days, member_index=None):
    members = get_members()
    if member_index is None:
        member_index = 0
    for day in days:
        day_index = days.index(day)
        if day_index in [0, 1]:
            day['member'] = members[member_index]['id']
            continue
        previous_pay = days[day_index - 1]['member']
        past_previous_pay = days[day_index - 2]['member']
        if previous_pay == past_previous_pay:
            member_index += 1
            if member_index > 3:
                member_index = 0
        day['member'] = members[member_index]['id']
    return days


def generate_list(from_date, from_member):
    days = get_list_of_days(from_date)
    set_members(days, from_member)
    write_days_list_into_db(days)
    return days
