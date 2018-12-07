import pyperclip
import random
import getpass
import sqlite3
import sys, getopt, random
import time
from base64 import b64encode, b64decode
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.strxor import strxor
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
from Crypto.Hash import SHA256


def get_random_password():
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 12
    p =  "".join(random.sample(s,passlen))
    return p


start_t = time.time()
for x in range(0,100):
    salt = get_random_bytes(8)
    authkey = PBKDF2(get_random_password(), salt, 16, 2000000)
    print(time.time() - start_t)
print(time.time()- start_t)
