# Matthew Irwin - CIS345 - MW @ Noon - PE6

import csv
import json
import random
import statistics
import time
from os import path
from functools import wraps


def log_transactions(logger):
    """
    Write all transactions to the csv file.
    :param logger:
    :return:
    """
    if not path.isfile('transactions.csv'):
        with open('transactions.csv', 'w') as fp:
            data = csv.writer(fp)
            data.writerow(['DateTime', 'Username', 'Old Balance', 'Transaction Amount', 'New Balance'])

    with open('transactions.csv', 'a') as fp:
        data = csv.writer(fp)
        data.writerow(logger)


def create_pin():
    pin_tries = 1
    max_tries = 3
    user_pin = ''

    user_entry = int(input('Enter 1 to create a pin yourself or 2 and the system will create a pin for you: '))

    while pin_tries <= max_tries:
        if user_entry == 1:
            try:
                user_pin = int(input('Select a number between 1 and 9999 as your pin: '))
            except ValueError:
                print(f'Invalid pin entered. Attempt {pin_tries} of {max_tries}')
                pin_tries += 1
            else:
                if 0 < user_pin <= 9999:
                    user_pin = user_pin
                    break
                print(f'Invalid pin entered. Attempt {pin_tries} of {max_tries}')
                pin_tries += 1
            if pin_tries > max_tries:
                user_pin = random.randint(1, 9999)
                break

        elif user_entry == 2:
            user_pin = random.randint(1, 9999)
            break

        else:
            print('Invalid entry please type either 1 or 2.')

    return user_pin


def line(func):
    """Add a line to the user interface"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function"""
        title = func(*args, **kwargs)
        print(f'|{title:<60}|')
    return wrapper

@line
def title1(border):
    """border"""
    return f'{border:*^60}'

@line
def title2():
    """Welcome Message"""
    return '  Welcome!'

@line
def title3(option):
    """"Application function options"""
    return f'  {option}'