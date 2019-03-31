import os
from datetime import date

import MySQLdb


def query(sql):
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
    cur.close()
    return members


def delete_not_relevant_days(from_date):
    cur = query(f"delete from days where date >= {from_date}")
    cur.close()


def write_days_list_into_db(days):
    delete_not_relevant_days(days[0]['date'])
    str_query = 'Insert into days values '
    day_data = [f"(0,'{day['date']}','{day['weekday']}','{day['member']}',{day['passed']}, 330)" for day in days]
    str_query += ', '.join(day_data)
    query(str_query)
