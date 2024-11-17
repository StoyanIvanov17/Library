import random
import string


def generate_isbn():
    isbn_base = ''.join(random.choices(string.digits, k=12))

    check_digit = calculate_isbn_check_digit(isbn_base)
    return isbn_base + str(check_digit)


def calculate_isbn_check_digit(isbn_base):
    total = 0
    for i, digit in enumerate(isbn_base):
        if i % 2 == 0:
            total += int(digit)
        else:
            total += int(digit) * 3
    check_digit = (10 - (total % 10)) % 10
    return check_digit
