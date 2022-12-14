import os

from mysql import connector


def query(sql: str) -> list[tuple]:
    db_connect = connector.connect(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        host=os.environ["DB_HOST"],
        charset="utf8",
        database=os.environ["DB"],
        connect_timeout=600,
    )
    try:
        cursor = db_connect.cursor(buffered=True)
        cursor.execute(sql)
    except (AttributeError, connector.OperationalError):
        db_connect.ping(True)
        cursor = db_connect.cursor(buffered=True)
        cursor.execute(sql)
    db_connect.commit()
    if sql.lower().startswith("select"):
        result = cursor.fetchall()
    else:
        result = None
    db_connect.close()
    return result
