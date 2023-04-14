import random
import string


def random_str(n):
    alph = string.ascii_letters
    return ''.join(random.choice(alph) for i in range(n))
