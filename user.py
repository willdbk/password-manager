
class User:

    def __init__(self, _username):
        self.username = username
        self.authenticated = False

    def exists(self):
        # check if the username already exists and if it doesn't then
        # return self.database.find(username)
        return True

    def create_account(self, pwd):
        salt = get_random_bytes(8)
        self.database[username]["salt"] = salt
        pwdkey = PBKDF2(password, salt)
        self.database["pwdkey"] = pwdkey

    def authenticate(self, pwd):
        salt = self.database[username]["salt"]
        pwdkey = PBKDF2(password, salt)
        if(self.database[username][pwdkey]=pwdkey):
            self.authenticated = True
            return True;
        return False;
