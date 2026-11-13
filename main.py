from src.accounts.user import User, UserService



def create_account():
    # gov_identification = input('entier your id')
    # first_name = input('entier first name ')
    # last_name = input('entier last name')
    # email = input('entier your email')
    # phone_number = input('entier your number')
    # password = input('entier password')
    
    gov_identification = "2154833948"
    first_name = "ahmed"
    last_name = "ali"
    email = "ahmed@gmail.com"
    phone_number = "0559182878"
    password = "ahmed1998"

    user = User(
        gov_identification=gov_identification, 
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        phone_number=phone_number, 
        password=password
            )

    UserService(user).add_account()

create_account()