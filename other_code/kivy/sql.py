import bcrypt
from Tools.DB import connect


def login(username, password):
    sql = connect.postgresql()
    password = str(password).encode()
    username = str(username).lower()
    users = sql.dataframe('login', 'username', 'password')
    check = (users[users[0] == username])
    try:
        db_pw = check.iloc[0, 1]
        if bcrypt.checkpw(password, db_pw.encode()):
            return True
        else:
            return False
    except IndexError:
        return None


def register():
    sql = connect.postgresql()
    username = input('Username: ').lower()
    password = input('Password: ')
    if password == input('Repeat password: '):
        check = sql.dataframe('login', 'username')
        if len(check[check[0] == username]):
            print('User already exists')
            return False
        sql.insert('login', username=username)
        ID = "username = '%s'" % username
        if sql.update_encrypted('login', ID, password=password):
            print('User registered')
            return True
    else:
        print("Passwords didn't match")
        return None
