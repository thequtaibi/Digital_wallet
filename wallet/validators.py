from email_validator import validate_email as check_email, EmailNotValidError
from wallet.models import AccountLimits, AccountType
from wallet.repositories import users, transactions


class AccountValidator:

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


class Validations:
    ACCOUNT_LIMITS = AccountLimits.ACCOUNT_LIMITS

    @staticmethod
    def pull_data(user_id):
        """Return the user row as a dict, or None if not found."""
        return users.get_by_id(user_id)

    @staticmethod
    def valid_users(user_id):
        return Validations.pull_data(user_id) is not None

    @staticmethod
    def validate_amount(user_id, amount):
        """True if today's total plus the new amount stays within the daily limit."""
        user = Validations.pull_data(user_id)
        if user is None:
            return False

        try:
            account_type = AccountType(user["account_type"])
        except ValueError: 
            return False

        limit = Validations.ACCOUNT_LIMITS.get(account_type)
        if limit is None:
            return False

        today_total = transactions.total_sent_today(user_id)

        return today_total + amount <= limit

    @staticmethod
    def valid_idempotency_key(idempotency_key):
        return not transactions.idempotency_key_exists(idempotency_key)

    @staticmethod
    def validate_account(user_id, amount):
        user = Validations.pull_data(user_id)
        if user is None:
            return False
        if user["account_status"] == 0:
            return False
        return Validations.validate_amount(user_id, amount)