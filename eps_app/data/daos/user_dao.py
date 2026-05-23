from data.database import get_connection
from data.models.user import User


class UserDAO:
    def find_by_username(self, username: str):
        connection = get_connection()
        row = connection.execute(
            "SELECT * FROM usuarios WHERE username = ? AND activo = 1", (username,)
        ).fetchone()
        if not row:
            return None
        return User(row["id"], row["username"], row["password"], row["rol"], row["activo"])