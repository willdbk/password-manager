import pyperclip
import random
import getpass
import sqlite3
import sys, getopt, random
from base64 import b64encode, b64decode
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.strxor import strxor
import db

profile_name_hash = ""
database = db.Database()

def get_random_password():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 8
    p =  "".join(random.sample(s,passlen)) # cryptographically secure???
    return p

def add_profile(pwd):
    salt = get_random_bytes(8)
    authkey = PBKDF2(pwd, salt)
    # database.add_profile(profile_name_hash,salt,authkey)
    database.add_profile(profile_name_hash,"salt","authkey")


def profile_exists():
    return database.exists(profile_name_hash)

def print_database():
    database.print_all()

def authenticate(pwd):
    salt = database.get_salt(profile_name_hash)[0]
    print(salt)
    authkey = PBKDF2(pwd, salt)
    print(database.get_authkey(profile_name_hash)[0])
    if(database.get_authkey(profile_name_hash) == authkey):
        return True;
    return True;

# Account has 5 fields: hash(URL), hash(username), salt, nonce, enc(pwd)
# the pwd is encrypted with a key generated from PBKDF2 using the salt and the master_password
# then pwd is then encrypted in CTR mode with the nonce
def add_account(self, URL, username, pwd, master_password):
    #these references to the database aren't right
    URL_hash = URL
    username_hash = username
    salt = get_random_bytes(8)
    nonce = get_random_bytes(8)

    enc_key = PBKDF2(master_password, salt)
    # create a counter object and set the nonce as its prefix and set the initial counter value to 0
    ctr = Counter.new(64, prefix=nonce, initial_value=0)
    cipher = AES.new(enc_key, AES.MODE_CTR, counter=ctr)

    # encrypt the plaintext
    enc_pwd = cipher.encrypt(plaintext)
    database.add_account(URL_hash, username_hash, salt, nonce, enc_pwd)


def retrieve_pwd(self, URL, username, master_password):
    #these references to the database aren't right
    account = db.get_account_with_url_and_username()
    salt = account["salt"]
    nonce = account["nonce"]
    enc_pwd = account["enc_pwd"]


    dec_key = PBKDF2(master_password, salt)
    # create a counter object and set the nonce as its prefix and set the initial counter value to 0
    ctr = Counter.new(64, prefix=nonce, initial_value=0)
    cipher = AES.new(enc_key, AES.MODE_CTR, counter=ctr)

    # encrypt the plaintext
    dec_pwd = cipher.decrypt(plaintext)
    return dec_pwd



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

print_database()


profile_name = input("Enter your profile name: ")
profile_name_hash = profile_name


if(not profile_exists()):
    print("A Profile with given username does not exist.")
    answer = input("Would you like to create a password management profile? (y or n)\n")
    if('y' in answer):
        password = getpass.getpass("Enter the MASTER password for this profile: ")
        add_profile(password)
        password = get_random_bytes(len(password))
    else:
        sys.exit(2)
else:
    password = getpass.getpass("Enter your MASTER password: ")
    authenticated = authenticate(password)
    password = get_random_bytes(len(password))
    if(not authenticated):
        sys.exit(2)
    database.set_active_account(profile_name_hash)

print()
print("You are INNN")
print()

response = input("Would you like to add data for an account ('a') or retrieve a saved password ('r')? ")
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
