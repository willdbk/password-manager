import sqlite3

class Database:

    def __init__(self):
        self.db_file = 'password_manager.sqlite'
        self.table_name = 'users'
        self.column_name = 'profile_name_hash'
        self.column_salt = 'profile_salt'
        self.column_auth_key = 'authentication_key'
        self.field_type = 'TEXT' # CHANGE BACK TO BLOB!!!

        self.conn = sqlite3.connect(self.db_file)
        c = self.conn.cursor()

        # creating a new SQLlite table with 1 column and set it as the PRIMARY
        #  KEY
        try:
            c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
            .format(tn=self.table_name, nf=self.column_name, ft=self.field_type))

            # adding new column for salt values
            c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
            .format(tn=self.table_name, cn=self.column_salt, ct=self.field_type))

            # adding a new column for authentication key
            c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
            .format(tn=self.table_name, cn=self.column_auth_key, ct=self.field_type))
        except:
            print("table already exists")

        # committing changes and closing the connection
        self.conn.commit()

    def print_all(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM {tn} WHERE {cn}="salt"'.\
        format(tn=self.table_name, cn=self.column_salt))
        all_rows = c.fetchall()
        print('DATA:', all_rows)

    def add_profile(self, name_hash, salt, auth_key):
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO users (profile_name_hash, profile_salt, authentication_key) VALUES (?, ?, ?)", (name_hash, salt, auth_key))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists')
            return False

    def exists(self, name_hash):
        try:
            c.execute('SELECT * FROM {tn} WHERE {cn}="{nh}"'.\
            format(tn=self.table_name, cn=self.column_name, nh=name_hash))
            return True
        except:
            return False
