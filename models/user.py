from data import query


class User:
    def __init__(self, username: str, password: str):
        self.password = password
        self.username = username


def get_user(username) -> User:
    users = []
    cur = query(f"SELECT username, password FROM aqa WHERE username LIKE '{username}'")
    for row in cur.fetchall():
        users.append(User(username=row[0], password=row[1]))
    if not users:
        raise ValueError(f'No such user - {username}')
    return users[0]
