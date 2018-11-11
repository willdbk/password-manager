Purpose
---------

The purpose of this password manager is to provide a command-line-based,
encrypted password-management system.


add_new_account.py
-specify a password
-create a DB associated with the account

access_account.py



overwrite it with random bits

flow (for login):
-login to user session (ask for username, master key for that user)
  -overwrite bits of master password in memory once verified
-create new user


flow (for account creation/adding):
-specify account details
-What do we ask for?
      -username
      -URL
      -password
        -user also has the option for program to generate password for them
  -prompt user to re-enter master key to encrypt new information
    -verify that master key matches with username of the session
        -checking that hash of username & password match the one in database
    -overwrite bits of master key


flow (for password retrieval):
-user searches account/url:
    -enter master password
        -stretch so checking takes a long time
    -plaintext password printed if account found
    -overwrite bits

-exit garbage collection


assumptions:
    -attacker can compromise database
    -offline dictionary attack possible
    -attacker can be a valid user?
