db = load_db("db")

class Profile:
    # Profile has 1 attributes: the hash(profile_name)
    # a boolean variable authenticated (whether the profile has been authenticated yet)
    # In the database, profiles are queried by profile_name and each profile has two attributes: salt, authkey

    def __init__(self, profile_name):
        self.profile_name_hash = hash(profile_name)

    def exists(self):
        return db[self.profile_name]

    def create_profile(self, pwd):
        salt = get_random_bytes(8)
        db[self.profile_name]["salt"] = salt
        authkey = PBKDF2(pwd, salt)
        db[self.profile_name]["authkey"] = authkey

    def authenticate(self, pwd):
        salt = db[self.profile_name_hash]["salt"]
        pwdkey = PBKDF2(password, salt)
        if(db[self.profile_name]["pwdkey"]=pwdkey):
            return True;
        return False;

    # Account has 5 attributes: hash(URL), hash(username), salt, nonce, enc(pwd)
    # the pwd is encrypted with a key generated from PBKDF2 using the salt and the master_password
    # then pwd is then encrypted in CTR mode with the nonce
    def create_account(self, URL, username):
        db[self.profile_name_hash]["URL_hash"] = hash(URL)
        db[self.profile_name_hash]["username_hash"] = hash(username)
        salt = get_random_bytes(8)
        db[self.profile_name_hash]["salt"] = salt
        nonce = get_random_bytes(8)
        db[self.profile_name_hash]["nonce"] = nonce

    def add_pwd(self, )
