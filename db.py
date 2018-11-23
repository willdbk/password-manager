import sqlite3

class Database:

    def __init__(self):
        self.db_file = 'password_manager.sqlite'
        self.table_name = 'users'
        self.column_name = 'profile_name_hash'
        self.column_salt = 'profile_salt'
        self.column_auth_key = 'authentication key'
        field_type = 'TEXT' # CHANGE BACK TO BLOB!!!

        self.conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # creating a new SQLlite table with 1 column and set it as the PRIMARY
        #  KEY
        c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=table_name, nf=column_name, ft=field_type))

        # adding new column for salt values
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=new_salt, ct=field_type))

        # adding a new column for authentication key
        c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=column_auth_key, ct=field_type))

        # committing changes and closing the connection
        conn.commit()

    def print_all(self):
        c = conn.cursor()
        c.execute('SELECT * FROM {tn} WHERE {cn}="Hi World"'.\
        format(tn=table_name, cn=column_name))
        all_rows = c.fetchall()
        print('DATA:', all_rows)

    def add_profile(self, name_hash, salt, auth_key):
        c = conn.cursor()
        try:
            c.execute("INSERT INTO {tn} VALUES ({nh}, {st}, {ak})".\
        format(tn=table_name, nh=name_hash, st=salt, ak=auth_key))
        except sqlite3.IntegrityError:
            print('ERROR: ID already exists in PRIMARY KEY column')
