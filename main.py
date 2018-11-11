
# flowwwww
username = input("enter your username:")
user = user.User(username)

if(not user.exists()):
    print("A User with given username does not exist.")
    answer = input("Would you like to create one? (y or n)")
    if('y' in answer):
        password = input("Enter the password:")
        user.create_account(password)
        password = get_random_bytes(len(password))
    else:
        sys.exit(2)

password = input("Enter the password:")
authenticated = user.authenticate(password)
password = get_random_bytes(len(password))
if(not authenticated):
    sys.exit(2)
