import pyperclip
import random
import getpass
import sqlite3
import sys, getopt, random
from base64 import b64encode, b64decode
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.strxor import strxor
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
from Crypto.Hash import SHA256
import db


profile_name_hash = ""
database = db.Database()

def get_random_password():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 12
    p =  "".join(random.sample(s,passlen)) # cryptographically secure???
    return p

def valid(pwd_str):
    lc = set("abcdefghijklmnopqrstuvwxyz")
    uc = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    nums = set("01234567890")
    sc = set("!@#$%^&*()?")
    pwd = set(pwd_str)
    return len(pwd_str)>=8 and bool(lc & pwd) and bool(uc & pwd) and bool(nums & pwd) and bool(sc & pwd)

def hash(str):
    h = SHA256.new()
    h.update(str.encode("utf-8"))
    return h.digest().hex()


def add_profile(pwd):
    salt = get_random_bytes(8)
    authkey = PBKDF2(pwd, salt)
    database.add_profile(profile_name_hash,salt,authkey)


def authenticate(pwd):
    salt = database.get_salt(profile_name_hash)
    authkey = PBKDF2(pwd, salt)
    if(database.get_authkey(profile_name_hash) == authkey):
        return True;
    return False;

# Account has 5 fields: hash(URL), hash(username), salt, nonce, enc(pwd)
# the pwd is encrypted with a key generated from PBKDF2 using the salt and the master_password
# then pwd is then encrypted in CTR mode with the nonce
def add_account(URL, username, pwd, master_password):
    #these references to the database aren't right
    URL_hash = hash(URL)
    username_hash = hash(username)
    salt = get_random_bytes(8)
    nonce = get_random_bytes(8)

    enc_key = PBKDF2(master_password, salt)
    # create a counter object and set the nonce as its prefix and set the initial counter value to 0
    ctr = Counter.new(64, prefix=nonce, initial_value=0)
    cipher = AES.new(enc_key, AES.MODE_CTR, counter=ctr)

    # encrypt the plaintext
    enc_pwd = cipher.encrypt(pwd.encode('utf-8'))
    database.add_account(URL_hash, username_hash, salt, nonce, enc_pwd)


def retrieve_pwd(URL, username, master_password):
    #these references to the database aren't right
    URL_hash = hash(URL)
    username_hash = hash(username)

    salt = database.get_account_salt(URL_hash, username_hash)
    if(salt is None):
        return None
    nonce = database.get_account_nonce(URL_hash, username_hash)
    enc_pwd = database.get_account_enc_pwd(URL_hash, username_hash)

    dec_key = PBKDF2(master_password, salt)
    # create a counter object and set the nonce as its prefix and set the initial counter value to 0
    ctr = Counter.new(64, prefix=nonce, initial_value=0)
    cipher = AES.new(dec_key, AES.MODE_CTR, counter=ctr)

    # encrypt the plaintext
    dec_pwd = cipher.decrypt(enc_pwd).decode('utf-8')
    return dec_pwd



print("Welcome to the Password Farm where we work from dawn to dusk to protect your passwords!")
# print("usage note: at any point type exit to quit out of the program")

# database.print_all()

profile_name = input("Enter your profile name: ")
profile_name_hash = hash(profile_name)


if(not database.exists(profile_name_hash)):
    print("A Profile with given username does not exist.")
    answer = input("Would you like to create a password management profile ('y' or 'n')? ")
    if('y' in answer):
        print("Password specifications: >=8 characters, >=1 character of: UPPERCASE, lowercase, number, and special)")
        password = getpass.getpass("Enter the MASTER password for this profile: ")
        while(not valid(password)):
            print("Password does not meet specifications.")
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
        print("Incorrect Password. Session Terminated.")
        sys.exit(2)
    database.set_active_profile(profile_name_hash)

print("You are INNN\n")

response = input("Would you like to add data for an account ('a') or retrieve a saved password ('r')? ")
while(response != "exit"):
    if(response == 'a'):
        url = input("Enter the URL for this account: ")
        username = input("Enter the username for this account: ")
        # check if url/username pair exists
        response = input("Would you like to provide a password for this account ('p') or have one randomly generated ('r')? ")
        password = ""
        if(response == 'p'):
            print("Password specifications: more than 8 characters, contain at least 1 character of: UPPERCASE, lowercase, number, and special)")
            password = getpass.getpass("Enter your password for this account:")
            while(not valid(password)):
                print("Password does not meet specifications.")
                password = getpass.getpass("Enter your password for this account:")
        elif(response == 'r'):
            while(not valid(password)):
                password = get_random_password()
        master_password = getpass.getpass("Enter your MASTER password: ")
        authenticated = authenticate(master_password)
        if(not authenticated):
            print("Incorrect Password. Session Terminated.")
            sys.exit(2)
        add_account(url, username, password, master_password)
        print("Account added\n")
    elif(response == 'r'):
        url = input("Enter the URL for this account: ")
        username = input("Enter the username for this account: ")
        master_password = getpass.getpass("Enter your MASTER password: ")
        password = retrieve_pwd(url, username, master_password)
        if(password == None):
            print("No account found with that URL and Username.")

        else:
            pyperclip.copy(password)
            print("The password for this account has been copied to your clipboard.")
        password = get_random_bytes(len(password))
        print()
    else:
        print("Input not recognized. Please type a valid command ('a' or 'r')\n")

    response = input("Would you like to add data for an account ('a') or retrieve a saved password ('r')? ")
