from dbController import *
from main import *

if __name__ == "__main__":
    user1 = User()
    user1.id = 1
    user1.first_name = "John"
    user1.last_name = "Doe"
    user1.email = "johndoe@gmail.com"
    add_user(user1)