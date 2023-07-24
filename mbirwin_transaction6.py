# Matthew Irwin - CIS345 - MW @ Noon - PE6

import json
import os
import math
import statistics
from mbirwin_logger import *


class myException(Exception):
    def __float__(self, message):
        self.message = message


user_found = False


# use the open command to open the file
customer_file = open('customers.json')
# read the file and load the data structure in using json.loads()
accounts = json.load(customer_file)
# close the file when done
customer_file.close()

#  Wrapper decorator used in order to create menu in other application.
title1('*')
title2()
title3('Welcome to the Cactus Bank Application ')
title3('Enter 1 to add a new customer')
title3('Enter 2 to delete a customer')
title3('Enter 3 to make bank transactions')
title3('Enter 4 to exit the application')
title1('*')

user_input = input('Make your selection: ')

if user_input == '1':
    username = input('Please enter your username: ')
    if username in accounts:
        print('User is already in program.')
    if username not in accounts:
        accounts[username] = dict()
        user_found = True
        accounts[username]['Pin'] = create_pin()
        with open('customers.json', 'w') as customer_file:
            json.dump(accounts, customer_file)
        print(f"Your pin is {accounts[username]['Pin']}")

    if user_found:
        # store name under name key in the dictionary
        accounts[username]['Name'] = input('Please enter your name: ')
        # print formatted welcome statement
        print(f"Welcome {accounts[username]['Name']}")

        # exception handling if string or negative number is entered in for 'C'
        try:
            # take user input for the number starting in the checking account.
            accounts[username]['C'] = float(input('Enter the amount you will deposit to the checking account: '))
            if int(accounts[username]['C']) < 0:
                raise myException('A negative or invalid number was entered. The current balance will be 0.0')
        except ValueError:
            print('A negative or invalid number was entered. The current balance will be 0.0')
            accounts[username]['C'] = 0.0
        except myException as errorsFor:
            print(errorsFor)
            accounts[username]['C'] = 0.0

        # exception handling if string or negative number is entered in for 'S'
        try:
            # take user input for the number starting in the savings account.
            accounts[username]['S'] = float(input('Enter the amount you will deposit to the savings account: '))
            if int(accounts[username]['S']) < 0:
                raise myException('A negative or invalid number was entered. The current balance will be 0.0')
        except ValueError:
            print('A negative or invalid number was entered. The current balance will be 0.0')
            accounts[username]['S'] = 0.0
        except myException as errorsFor:
            print(errorsFor)
            accounts[username]['S'] = 0.0

        print('Your account has been created.')
        print('Please visit the system again to make transactions')
        input('Press enter to continue')

        print('\n\nSaving data...')
        # TODO: Write accounts data structure to file
        # We can write accounts to our data file here because
        with open('customers.json', 'w') as customer_file:
            json.dump(accounts, customer_file)

        # this is after we exit our application loop when
        # the user typed x to exit.

        print('\nData Saved.\nExiting...')
elif user_input == '2':
    user_entry = input('Please enter your username: ')
    if user_entry in accounts:
        accounts.pop(user_entry)
        print(f'Customer {user_entry} has been deleted.')
        input('Press Enter to exit.')
        with open('customers.json', 'w') as customer_file:
            json.dump(accounts, customer_file)
        exit()
    else:
        print('Username not found in accounts.')
        exit()
elif user_input == '3':

    max_tries = 3
    tries = 1

    username = input('Please enter a username: ')
    print(f'{"Cactus Bank":^30}\n')

    while tries <= max_tries:
        if username in accounts:
            # Print bank title and menu
            selection = input('Enter pin or x to exit application: ').casefold()

            # determine exit, pin not found, or correct pin found
            if selection == 'x':
                break

            # Verify entered pin is a key in accounts
            elif int(selection) != accounts[username]['Pin']:
                os.system('clear')

                print(f'Invalid pin. Attempt {tries} of {max_tries}. Please Try again')
                if tries == max_tries:
                    ans = input("Do you want to create a new pin (Y/N)? ").lower()
                    if ans[0] == 'y':
                        accounts[username]['Pin'] = create_pin()
                        print(f"Your pin is {accounts[username]['Pin']}")
                        print('Please visit the system again to make transactions.')
                        input('Press enter to continue...')
                    if ans[0] == 'n':
                        print('Thank you. Goodbye!')
                        break
                    else:
                        print('Invalid Entry. Exiting the program.')
                        break

                tries += 1
            else:
                # Successful pin entry. reset tries and save pin
                tries = 1
                pin = selection

                os.system('clear')
                # os.system('clear')

                for t in range(1, 5):
                    # Welcome customer
                    print(f"Welcome {accounts[username]['Name']}")
                    print(f'{"Select Account": ^20}')

                    # Prompt for Checking or Savings
                    while True:
                        try:
                            selection = input('Enter C or S for Checking or Savings: ').upper()
                            if selection != 'C' and selection != 'S':
                                raise ValueError('Incorrect selection.  You must enter C or S.')
                        except ValueError as ex:
                            print(ex)
                        else:
                            os.system('clear')
                            print(f'Opening {selection} Account...\n')
                            break
                    # End Prompt Checking or Savings

                    print('Transaction instructions:')
                    print(' - Withdrawal enter a negative dollar amount: -20.00.')
                    print(' - Deposit enter a positive dollar amount: 10.50')

                    # FIXME: Modify the code below to display the selected account's balance with commas for thousands
                    print(f'\nBalance:  ${accounts[username][selection]: ,.2f}')

                    old_bal = accounts[username][selection]

                    amount = 0.00
                    try:
                        amount = float(input(f'Enter transaction amount: '))
                    # FIXME: Catch appropriate exceptions not just Exception
                    # print better error message details using exception object
                    except ValueError as ex:
                        print(ex)
                        amount = 0.00
                    except TypeError as ex:
                        print(ex)
                        amount = 0.00
                    except Exception:
                        print('Bad Amount - No Transaction.')
                        amount = 0.00

                    # Verify enough funds in account
                    if (amount + accounts[username][selection]) >= 0:
                        # FIXME: round() new account balance to 2 decimal places
                        accounts[username][selection] = round((accounts[username][selection] + amount), 2)
                        # Do this step last after running your program.
                        # FIXME: Modify formatting to add commas for thousands
                        print(f'Transaction complete. New balance is {accounts[username][selection]: ,.2f}')

                        logger = [time.ctime(), username, f'${old_bal:,.2f}', f'${amount:,.2f}', f'${accounts[username][selection]:,.2f}']
                        log_transactions(logger)
                    else:
                        print('Insufficient Funds. Transaction Cancelled.')

                    ans = input('Press n to make another transaction or x to exit application: ').casefold()
                    if ans[0] == 'x':
                        tries = max_tries + 1
                        break
        if username not in accounts:
            print('Username not found in accounts. Please try again.')
            input('Press enter to exit...')
            exit()

    # end of application loop

    print('\n\nSaving data...')
    # TODO: Write accounts data structure to file
    # We can write accounts to our data file here because
    with open('customers.json', 'w') as customer_file:
        json.dump(accounts, customer_file)

    # this is after we exit our application loop when
    # the user typed x to exit.

    print('\nData Saved.\nExiting...')

    result = list()
    result2 = list()
    for username in accounts:
        print(f"{username:>20} {accounts[username]['Pin']:>20} {accounts[username]['Name']:>20} {accounts[username]['C']:>20} {accounts[username]['S']:>20}")

    with open('customers.json') as fp:
        customers_data = json.load(fp)

    for username in customers_data:
        result.append(accounts[username]['C'])

    for username in customers_data:
        result2.append(accounts[username]['S'])

    sum1 = math.fsum(result)
    sum2 = math.fsum(result2)
    print()
    print(f"Checking accounts' balance is {sum1} ")
    print(f"Checking accounts' balance is {sum2} ")
    print('Customer whose checking account balance is above the average: ')
    avg = statistics.mean(result)
    above_avg = list(filter(lambda x: x > avg, result))
    for username in accounts:
        if accounts[username]['C'] in above_avg:
            print(f"username is {username} and name is {accounts[username]['Name']}")
    print()

    print('Customer whose savings account balance is above the average: ')
    avg2 = statistics.mean(result2)
    above_avg2 = list(filter(lambda x: x > avg2, result2))
    for username in accounts:
        if accounts[username]['S'] in above_avg2:
            print(f"username is {username} and name is {accounts[username]['Name']}")

elif user_input == '4':
    print('Thank you. Goodbye!')
    exit()
else:
    print('Invalid entry.')
