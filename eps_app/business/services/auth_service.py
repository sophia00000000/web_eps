from data.daos.user_dao import UserDAO


class AuthService:
    def __init__(self):
        self.user_dao = UserDAO()

    def login(self, username: str, password: str):
        user = self.user_dao.find_by_username(username)
        if user and user.password == password:
            return user
        return None