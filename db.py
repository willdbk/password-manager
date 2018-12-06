import sqlite3
import random

class Database:

    def __init__(self):
        self.db_file = 'profiles.sqlite'
        self.table_name = 'profiles'
        self.column_name_hash = 'profile_name_hash'
        self.column_salt = 'profile_salt'
        self.column_auth_key = 'authentication_key'
        self.column_file_ref = 'profile_file_ref' # Reference to account sql file for each account
        self.field_type = 'TEXT' # CHANGE BACK TO BLOB!!! (or do we have to?)
        # Column names for account databases

        # Account has 5 fields: hash(URL), hash(username), salt, nonce, enc(pwd)
        self.prof_table_name = 'accounts'
        self.column_prof_URL_hash = 'prof_url_hash'
        self.column_prof_username_hash = 'prof_username_hash'
        self.column_prof_salt = 'prof_salt'
        self.column_prof_nonce = 'prof_nonce'
        self.column_prof_enc_pwd = 'prof_pwd_enc'

        self.conn = sqlite3.connect(self.db_file)
        c = self.conn.cursor()

        # creating a new SQLlite table with 1 column and set it as the PRIMARY KEY
        try:
            c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
            .format(tn=self.table_name, nf=self.column_name_hash, ft=self.field_type))

            # adding new column for salt values
            c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
            .format(tn=self.table_name, cn=self.column_salt, ct=self.field_type))

            # adding a new column for authentication key
            c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
            .format(tn=self.table_name, cn=self.column_auth_key, ct=self.field_type))

            # adding file reference
            c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
            .format(tn=self.table_name, cn=self.column_file_ref, ct=self.field_type))
        except:
            x=0

        # committing changes and closing the connection
        self.conn.commit()

    def print_all(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM profiles')
        all_rows = c.fetchall()
        print('DATA:', all_rows)

    def add_profile(self, name_hash, salt, auth_key):
        c = self.conn.cursor()
        try:
            prof_file_ref_name = str(random.randrange(100000000, 999999999))+'.sqlite'
            self.create_profile_db(prof_file_ref_name)
            c.execute("INSERT INTO profiles (profile_name_hash, profile_salt, authentication_key, profile_file_ref) VALUES (?, ?, ?, ?)", (name_hash, salt, auth_key, prof_file_ref_name))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists')
            return False

    def set_active_profile(self,name_hash):
        file_ref = self.get_file_ref(name_hash)
        self.profile_conn = sqlite3.connect(file_ref)

# retrieval functions
    def get_value_from_profile(self,name_hash,column_name):
        if(self.exists(name_hash)):
            c = self.conn.cursor()
            c.execute('SELECT {cw} FROM {tn} WHERE {cn}="{nh}"'.\
            format(cw=column_name,tn=self.table_name,cn=self.column_name_hash,nh=name_hash))
            return c.fetchone()[0] #is this correct? (does not work when there are multiple accounts with the same prof ref... which there should never be)
        else:
            raise ValueError('ERROR: no value for column' + column_name + " found under account hash "+name_hash)

    def get_salt(self, name_hash):
        return self.get_value_from_profile(name_hash,self.column_salt)

    def get_authkey(self, name_hash):
        return self.get_value_from_profile(name_hash,self.column_auth_key)

    def get_file_ref(self, name_hash):
        return self.get_value_from_profile(name_hash,self.column_file_ref)

    def exists(self, name_hash):
        c = self.conn.cursor()
        try:
            c.execute('SELECT * FROM {tn} WHERE {cn}="{nh}"'.\
            format(tn=self.table_name, cn=self.column_name_hash, nh=name_hash))
            if(c.fetchone() == None):
                return False
            return True
        except:
            return False

# account db functions
    def create_profile_db(self, prof_file_ref_name):
        self.profile_conn = sqlite3.connect(prof_file_ref_name)
        c = self.profile_conn.cursor()

        # creating a new SQLlite table with 1 column and set it as the PRIMARY KEY
        try:
            # adding new column for URL hash
            c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
            .format(tn=self.prof_table_name, nf=self.column_prof_URL_hash, ft=self.field_type))

            # adding new column for username hash
            c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
            .format(tn=self.prof_table_name, cn=self.column_prof_username_hash, ct=self.field_type))

            # adding new column for salt
            c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
            .format(tn=self.prof_table_name, cn=self.column_prof_salt, ct=self.field_type))

            # adding new column for nonce
            c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
            .format(tn=self.prof_table_name, cn=self.column_prof_nonce, ct=self.field_type))

            # adding new column for enc(pwd)
            c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
            .format(tn=self.prof_table_name, cn=self.column_prof_enc_pwd, ct=self.field_type))
        except:
            print("table already exists")

        # committing changes and closing the connection
        self.conn.commit()

    def add_account(self, URL_hash, username_hash, salt, nonce, pwd_enc):
        c = self.profile_conn.cursor()
        try:
            c.execute("INSERT INTO accounts (prof_url_hash, prof_username_hash, prof_salt, prof_nonce, prof_pwd_enc) VALUES (?, ?, ?, ?, ?)", (URL_hash, username_hash, salt, nonce, pwd_enc))
            self.profile_conn.commit()
            return True
        except sqlite3.IntegrityError:
            print('ERROR: account already exists')
            return False

# account retrieval functions
    def get_value_from_account(self,URL_hash, username_hash,column_name):
        c = self.profile_conn.cursor()
        c.execute('SELECT {cw} FROM {tn} WHERE {cn}="{nh}" AND {uh}="{cuh}"'.\
        format(cw=column_name,tn=self.prof_table_name,cn=self.column_prof_URL_hash,nh=URL_hash,uh=self.column_prof_username_hash,cuh=username_hash))
        output = c.fetchone();
        if(output is not None):
            return output[0] #is this correct? (does not work when there are multiple accounts with the same prof ref... which there should never be)
        return None

    def get_account_enc_pwd(self, URL_hash, username_hash):
        return self.get_value_from_account(URL_hash,username_hash,self.column_prof_enc_pwd)


    def get_account_salt(self, URL_hash, username_hash):
        return self.get_value_from_account(URL_hash,username_hash,self.column_prof_salt)


    def get_account_nonce(self, URL_hash, username_hash):
        return self.get_value_from_account(URL_hash,username_hash,self.column_prof_nonce)
