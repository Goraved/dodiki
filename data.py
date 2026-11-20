import os
import threading

from mysql import connector

_lock = threading.Lock()
_connection = None


def _get_connection():
    """Reuse one connection per process (saves a TCP+auth handshake per query)."""
    global _connection
    if _connection is None:
        _connection = connector.connect(
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            host=os.environ["DB_HOST"],
            charset="utf8",
            database=os.environ["DB"],
            connect_timeout=10,
        )
    return _connection


def _reset_connection():
    global _connection
    try:
        if _connection is not None:
            _connection.close()
    except connector.Error:
        pass
    _connection = None


def _run(sql: str, params):
    connection = _get_connection()
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(sql, params)
        if sql.lstrip().lower().startswith("select"):
            return cursor.fetchall()
        connection.commit()
        return None
    finally:
        cursor.close()


def query(sql: str, params: tuple = None) -> list[tuple]:
    """Run a query. Always pass user-supplied values via `params` (never format them into `sql`)."""
    with _lock:
        try:
            return _run(sql, params)
        except (connector.OperationalError, connector.InterfaceError):
            # connection was probably dropped while idle: reconnect and retry once
            _reset_connection()
            return _run(sql, params)
        except connector.Error:
            _reset_connection()
            raise
