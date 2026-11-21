from wallet.validators import AccountValidator
from wallet.repositories import users


class AccountService:
    def __init__(self, user):
        self.user = user


    def save_to_db(self):
        try:
            users.insert_user(self.user)
            return f"Done adding {self.user.gov_identification}"

        except BufferError:
            return f'error {BufferError}'


    def check_for_existing_account(self):
        return users.gov_id_exists(self.user.gov_identification)

    def add_account(self):

        if self.check_for_existing_account():
            return "you have already account"

        elif not AccountValidator().validate_email(self.user.email):
            return "invild email"

        elif not AccountValidator().validate_phone_number(self.user.phone_number):
            return 'invild phone'
        else:
            save_to_db = self.save_to_db()
            return save_to_db


    def delete_account(self):
        pass

    def edit_account(self):
        pass
