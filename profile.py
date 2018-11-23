import sqlite3
import sys, getopt, random
from base64 import b64encode, b64decode
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.strxor import strxor
import db

class Profile:
    # Profile has 2 attributes: the hash(profile_name) and the database
    # a boolean variable authenticated (whether the profile has been authenticated yet)
    # In the database, profiles are queried by profile_name and each profile has two attributes: salt, authkey

    def __init__(self, profile_name):
        #self.profile_name_hash = hash(profile_name)
        self.profile_name_hash = profile_name

        self.database = db.Database()

    def add_profile(self, pwd):

        salt = get_random_bytes(8)
        authkey = PBKDF2(pwd, salt)

        # self.database.add_profile(profile_name_hash,salt,authkey)
        self.database.add_profile(self.profile_name_hash,"salt","authkey")


    def exists(self):
        return self.database.exists(self.profile_name_hash)

    def print_all(self):
        self.database.print_all()

'''
    def authenticate(self, pwd):
        salt = db[self.profile_name_hash]["salt"]
        authkey = PBKDF2(pwd, salt)
        if(db[self.profile_name_hash]["authkey"] == authkey):
            return True;
        return False;

    # Account has 5 fields: hash(URL), hash(username), salt, nonce, enc(pwd)
    # the pwd is encrypted with a key generated from PBKDF2 using the salt and the master_password
    # then pwd is then encrypted in CTR mode with the nonce
    def add_account(self, URL, username, pwd, master_password):
        #these references to the database aren't right
        db[self.profile_name_hash]["URL_hash"] = hash(URL)
        db[self.profile_name_hash]["username_hash"] = hash(username)
        salt = get_random_bytes(8)
        db[self.profile_name_hash]["salt"] = salt
        nonce = get_random_bytes(8)
        db[self.profile_name_hash]["nonce"] = nonce

        enc_key = PBKDF2(master_password, salt)
        # create a counter object and set the nonce as its prefix and set the initial counter value to 0
        ctr = Counter.new(64, prefix=nonce, initial_value=0)
        cipher = AES.new(enc_key, AES.MODE_CTR, counter=ctr)

        # encrypt the plaintext
        enc_pwd = cipher.encrypt(plaintext)
        db[self.profile_name_hash]["enc_pwd"] = enc_pwd

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
'''
