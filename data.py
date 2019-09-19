import os
from datetime import date

import MySQLdb


def query(sql):
    # ATTENTION i dont now how actual must set environ
    db_to_prod_connection()
    db = MySQLdb.connect(user=os.environ['DB_USER'], password=os.environ['DB_PASS'],
                         host=os.environ['DB_HOST'], charset='utf8',
                         database=os.environ['DB'], connect_timeout=600)
    try:
        cursor = db.cursor()
        cursor.execute("""SET NAMES 'utf8';
    SET CHARACTER SET 'utf8';
    SET SESSION collation_connection = 'utf8_general_ci';""")
    except:
        pass
    try:
        cursor = db.cursor()
        cursor.execute(sql)
    except (AttributeError, MySQLdb.OperationalError):
        db.ping(True)
        cursor = db.cursor()
        cursor.execute(sql)
    db.commit()
    db.close()
    return cursor


def get_members():
    members = []
    cur = query('Select * from members')
    for row in cur.fetchall():
        members.append({'id': row[0], 'name': row[1]})
    return members


def delete_not_relevant_days(from_date):
    cur = query(f"delete from days where date >= {from_date}")


def write_days_list_into_db(days):
    delete_not_relevant_days(days[0]['date'])
    str_query = 'Insert into days values '
    day_data = [f"(0,'{day['date']}','{day['weekday']}','{day['member']}',{day['passed']}, 330)" for day in days]
    str_query += ', '.join(day_data)
    query(str_query)


def get_rehearsals(from_date):
    rehearsals = []
    members = get_members()
    cur = query(f'Select id, date, member_id, price, day_of_week from days where date >= {from_date} and passed = 0')
    for row in cur.fetchall():
        member = [_["name"] for _ in members if _["id"] == row[2]][0]
        rehearsals.append({"id": row[0], "date": row[1], "member": member, "price": row[3], "weekday": row[4]})
    return rehearsals


def set_passed_rehearsals():
    today = date.today().strftime('%Y%m%d')
    cur = query(f'Update days set passed = 1 where date < {today}')


def delete_rehearsal(rehearsal_id):
    cur = query(f'Delete from days where id = {rehearsal_id}')


def swap_rehearsal_members(swap_ids):
    rehearsals = []
    cur = query(f'Select id, member_id from days where id in ({swap_ids[0]},{swap_ids[1]})')
    for row in cur.fetchall():
        rehearsals.append({'id': row[0], 'member_id': row[1]})
    cur = query(f"Update days set member_id = {rehearsals[1]['member_id']} where id = {rehearsals[0]['id']};")
    cur = query(f"Update days set member_id = {rehearsals[0]['member_id']} where id = {rehearsals[1]['id']};")


def db_connection_for_noob():
    os.environ['DB_USER'] = 'pahlava'
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB'] = 'dodiki_db'
    os.environ['DB_PASS'] = '12345678'


def db_to_prod_connection():
    os.environ['DB_USER'] = 'dodiki'
    os.environ['DB_HOST'] = 'den1.mysql3.gear.host'
    os.environ['DB'] = 'dodiki'
    os.environ['DB_PASS'] = 'Qb0kC17-uBr!'

    # ser = os.environ['DB_USER'], password = os.environ['DB_PASS'],
    # host = os.environ['DB_HOST'], charset = 'utf8',
    # database = os.environ['DB']
