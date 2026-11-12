import uuid

print(uuid.uuid7().int)

class User:
    def __init__(self, first_name, last_name, email, phone_number, password, ):
        self.user_id = uuid.uuid1
        