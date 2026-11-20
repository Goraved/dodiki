from data import query


class User:
    def __init__(self, username: str, password: str):
        self.password = password
        self.username = username


def get_user(username) -> User:
    users = []
    result = query(
        "SELECT username, password FROM aqa WHERE username = %s", (username,)
    )
    for row in result:
        users.append(User(username=row[0], password=row[1]))
    return users[0] if users else None
