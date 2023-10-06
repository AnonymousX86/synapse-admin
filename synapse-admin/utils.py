# -*- coding: utf-8 -*-
from random import choice
from re import match


LETTERS = 'qwertyuiopasdfghjklzxcvbnm'
NUMBERS = '1234567890'


def check_username(username: str) -> bool:
    return bool(match('^[a-z_]*$', username))

def temp_password() -> str:
    password = ''
    for _ in range(3):
        password += choice(LETTERS)
    for _ in range(5):
        password += choice(NUMBERS)
    return password.capitalize()
