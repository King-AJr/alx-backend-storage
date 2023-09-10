#!/usr/bin/python3
"""
Main
"""
import MySQLdb
import sys

username = sys.argv[1]
pwd = sys.argv[2]
db_name = sys.argv[3]


db = MySQLdb.connect(user=username, passwd=pwd, db=db_name, host='localhost')

cursor = db.cursor(MySQLdb.cursors.DictCursor)


def listOfUsers():
    """ List all users.id """
    cursor.execute('SELECT id, email, name FROM users;')
    rows = cursor.fetchall()
    return [{'id': i['id'], 'email': i['email'], 'name': i['name']} for i in rows]

def createUser(email, name):
    """ Create a user """
    try:
        if email is None:
            cursor.execute('INSERT INTO users (name) VALUES ("{}")'.format(name))
        else:
            cursor.execute('INSERT INTO users (email, name) VALUES ("{}", "{}")'.format(email, name))
        db.commit()
    except:
        pass


# No user
if len(listOfUsers()) != 0:
    print("Table is not empty at the beginning")
    exit(1)


# Create one user with an email
uEmail = "user1@test.com"
uName = "user1"
createUser(uEmail, uName)
users = listOfUsers()
if len(users) != 1:
    print("Missing user")
    exit(1)

user = users[0]
if user['email'] != uEmail:
    print("Missing new email user: {} / {}".format(uEmail, user))
    exit(1)
if user['name'] != uName:
    print("Missing new name user: {} / {}".format(uName, user))
    exit(1)


# Create one user without an email => fail
u2Email = None
u2Name = "user2"
createUser(u2Email, u2Name)
users = listOfUsers()
if len(users) != 1:
    print("Number of users should stay at 1")
    exit(1)
user = users[0]
if user['email'] != uEmail:
    print("Missing first email user: {} / {}".format(uEmail, user))
    exit(1)
if user['name'] != uName:
    print("Missing first name user: {} / {}".format(uName, user))
    exit(1)


# Create one user with same email but different name => fail
u3Email = "{}".format(uEmail)
u3Name = "user3"
createUser(u3Email, u3Name)
users = listOfUsers()
if len(users) != 1:
    print("Number of users should stay at 1")
    exit(1)
user = users[0]
if user['email'] != uEmail:
    print("Missing first email user: {} / {}".format(uEmail, user))
    exit(1)
if user['name'] != uName:
    print("Missing first name user: {} / {}".format(uName, user))
    exit(1)


# create 10 new users
nameByEmail = {}
for i in range(10):
    iEmail = "iuser{}@test.com".format(i)
    iName = "User {}".format(i)
    createUser(iEmail, iName)
    nameByEmail[iEmail] = iName

users = listOfUsers()
for user in users:
    uEmail = user['email']
    if nameByEmail.get(uEmail, '') == user['name']:
        del nameByEmail[uEmail]

if len(nameByEmail) != 0:
    print("Some users are not created: {}".format(nameByEmail))
    exit(1)

db.close()

print("OK", end="")
