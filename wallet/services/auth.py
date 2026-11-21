from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
ph = PasswordHasher()
from wallet.repositories import users


class LoginVerification:
    def __init__(self, username, password):
        self.username = username
        self.password = password


    def _search_db(self):
        user = users.find_login(self.username)

        if user is not None:
            user = dict(user)
            return user

        return False


    def _verify_password(self, password, hashed_password):
        try:
            if ph.verify(hashed_password, password):
                return True

            return False

        except VerifyMismatchError:
            return False

        except VerificationError:
            return False

    def verification(self):
        user = self._search_db()

        if not user:
            return False

        return self._verify_password(self.password, user[self.username])

