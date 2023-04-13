import string
import random

def generate_user_credentials():
    username = "u_" + generate_random_string(8)
    password = "pw_" + generate_random_string(10)
    db_name = "db_" + generate_random_string(8)
    return username, password, db_name

def generate_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    