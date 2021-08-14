from random import choice
from string import ascii_letters, digits

RANDOM_CAND = ascii_letters + digits


def generate_random_string(size=12):
    # `size=12` from medium slug random string
    return "".join(choice(RANDOM_CAND) for _ in range(size))
