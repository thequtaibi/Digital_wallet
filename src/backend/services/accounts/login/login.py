import sqlite3
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
ph = PasswordHasher()


class LoginVerification:
    def __init__(self, username, password):
        self.username = username
        self.password = password


    def _search_db(self):
        with sqlite3.connect("src/backend/database/wallet.db") as conn:
            result = conn.execute("""
                    SELECT 
                    username,
                    password
                    FROM users
                    WHERE username = ?
                    """,
                    (self.username,))
            user = result.fetchall()

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



        
test = LoginVerification("khlk4004", "khlk4004")
print(test.verification())