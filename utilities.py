from cryptography.fernet import Fernet as F
from dotenv import load_dotenv
import os
import random as R
import string as S

load_dotenv()

key = os.getenv("FERNET_KEY").encode()
cipher = F(key)


def menuInterface():
    choice_dict = {1: 'Add Account', 2: 'View Accounts', 3: 'Delete Account', 4: 'Exit'}

    while True:
        print('\n--- Password Manager ---\n\n\n')
        print('1. Add Account\n2. View Accounts\n3. Delete Account\n4. Exit')
        userChoice = int(input('Select Option here (type number): ').strip())
        if userChoice not in (1,2,3,4):
            print('Invalid Select!')
            continue
        return choice_dict[userChoice]

def addAccount(vault,account):
    print('\n--- Add Account ---\n')
    print('Type [q] to exit function')
    user_input = input('Click enter to continue')

    if user_input == 'q':
        return False
    
    application = input('Application Name: ').strip().lower()
    username = input('Username: ').strip()
    user_input = input('[G]enerate Password or "enter" to type your own password: ').strip().lower()
    if user_input == 'g':
        while True:
            password = generatePassword()
            print(f'Generate password: {password}')
            user_input2 = input('"Enter" to continue, [G]enerate new password: ').strip().lower()
            if user_input2 == 'g':
                continue
            break
    else:
        password = input('Password: ').strip()

    encrypted_password = cipher.encrypt(password.encode()).decode()
    vault[account][application] = {'username': username, 'password': encrypted_password}
    return vault

def viewAccounts(vault, account, calledbyfunc=False):
    print('\n--- Accounts ---\n')
    if calledbyfunc == True:
        for application in vault[account]:
            print(application.capitalize())
        return None

    for application in vault[account]:
        print(application.capitalize())

    while True:
        print('Type [q] to exit function')
        viewInfo = input('Click enter to select account: ').strip().lower()
        if viewInfo == 'q':
            return None
        
        if viewInfo != '':
            print('Invalid Selection!')
            continue

        viewApplicationInformation(vault, account)
    
def deleteApplication(vault, account):
    print('\n--- Delete Account ---\n')
    print('Enter [q] anytime to exit function\n')
    while True:
        choice = input('Would you like to display your accounts [y]es or [n]o: ').strip().lower()
        if choice not in ('n','y','q'):
            print('Not a valid choice')
            continue

        if choice == 'n':
            break

        if choice == 'q':
            return vault  

        print()
        viewAccounts(vault, account, True)

        break
    
    while True:
        try:
            choosen_application = input('\nPlease Enter Account to Delete: ').strip().lower()
            if choosen_application == 'q':
                return None
            del vault[account][choosen_application]
            print('\n', choosen_application.capitalize(), 'has been removed from vault.')
            break
        except KeyError:
            print('No account found!')

    return vault

def viewApplicationInformation(vault, account):
    application = input('Enter Account: ').strip().lower()


    if application not in vault[account]:
        print('Account Doesn\'t Exists')


    username = vault[account][application]['username']
    password = cipher.decrypt(vault[account][application]['password'].encode()).decode()
    print(f"{application.capitalize()}\n    Username: {username}\n    Password: {password}")

def generatePassword():
    characters = S.ascii_letters + S.digits + '!$*/#'
    lis = []
    for _ in range(12):
        character = R.choice(characters)
        lis.append(character)
    return ''.join(lis)




