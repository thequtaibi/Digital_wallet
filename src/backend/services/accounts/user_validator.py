from email_validator import validate_email as check_email, EmailNotValidError
import sqlite3

class UserValidator:

    @staticmethod
    def validate_email(email):
        try:
            check_email(email, check_deliverability=False)
            return True
        except EmailNotValidError:
            return False

    @staticmethod
    def validate_phone_number(phone_number):
        return len(phone_number) >= 10