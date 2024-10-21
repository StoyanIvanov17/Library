import random
import string


def generate_library_card_number():
    prefix = "LIB"
    number_length = 8
    number = ''.join(random.choices(string.digits, k=number_length))
    return f"{prefix}{number}"
