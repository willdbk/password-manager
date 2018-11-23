import pyperclip
import random


def get_random_password():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 8
    p =  "".join(random.sample(s,passlen))
    return p



# flowwwww
print("\nWelcome to the Password Farm where we work from dawn to dusk to protect your passwords!")
print("usage note: at any point type exit to quit out of the program")

'''
# check to see if database file exists already
try:
    fh = open('password_manager.sqlite', 'r')
    fh.close()
except FileNotFoundError:
    #insert code for initializing DB for first time startup
'''

profile_name = input("Enter your profile name: ")
# profile = profile.Profile(username)

#if(not user.exists()):
if(random.random() < 0.5):
    print("A Profile with given username does not exist.")
    answer = input("Would you like to create a password management profile? (y or n)\n")
    if('y' in answer):
        password = input("Enter the MASTER password for this profile: ")
        # account.create_profile(password)
        password = get_random_bytes(len(password))
    else:
        sys.exit(2)
else:
    password = input("Enter your master password:")
    # authenticated = user.authenticate(password)
    password = get_random_bytes(len(password))
    if(not authenticated):
        sys.exit(2)

response = input("Would you like to add data for an account ('a') or retrieve a saved password ('r')?")
while(response != "exit"):
    if(response == 'a'):
        url = input("What is the URL for this account?")
        username = input("What is the username for this account?")
        response = input("Would you like to provide a password for this account ('p') or have one randomly generated ('r')?")
        password = ""
        if(response == 'p'):
            password = input("Enter your password for this account:")
        elif(response == 'r'):
            password = get_random_password()
#        profile.addAccount(url, username)
    elif(response == 'r'):
        url = input("What is the URL for this account?")
        username = input("What is the username for this account?")
#        password = profile.retrieve_pwd(url, username)
        #copies password to user's clipboard
        pyperclip.copy(password)
        password = get_random_bytes(len(password))
        #TODO: Query database to find whether such a user exists

    response = input("Would you like to add data for an account ('a') or retrieve a saved password ('r')?")
