import os

import MySQLdb
from MySQLdb.cursors import Cursor


def query(sql: str) -> Cursor:
    db_connect = MySQLdb.connect(user=os.environ['DB_USER'], password=os.environ['DB_PASS'],
                                 host=os.environ['DB_HOST'], charset='utf8',
                                 database=os.environ['DB'], connect_timeout=600)
    try:
        cursor = db_connect.cursor()
        cursor.execute("SET NAMES 'utf8'; "
                       "SET CHARACTER SET 'utf8'; "
                       "SET SESSION collation_connection = 'utf8_general_ci';")
    except:
        pass
    try:
        cursor = db_connect.cursor()
        cursor.execute(sql)
    except (AttributeError, MySQLdb.OperationalError):
        db_connect.ping(True)
        cursor = db_connect.cursor()
        cursor.execute(sql)
    db_connect.commit()
    db_connect.close()
    return cursor
