import string
import random


def generate_random_string(length=12):
    return "".join(random.choices(string.ascii_letters + string.digits, k=12))
