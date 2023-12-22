from random import randint
from cs50 import SQL

db = SQL("sqlite:///questions.db")

def fun(x, l):

    # choose a random question
    i = randint(1,l)
    q = db.execute("SELECT q FROM (?) WHERE id = (?)", x, i)[0]["q"]
    a = db.execute("SELECT a FROM (?) WHERE id = (?)", x, i)[0]["a"]
    arr = [q,a]

    # ensure the answer options do not repeat
    tmp = [a]
    option_2 = a
    option_3 = a
    option_4 = a
    option_5 = a
    while(option_2 in tmp):
        option_2 = db.execute("SELECT a FROM (?) WHERE id = (?)", x, randint(1,l))[0]["a"]
    tmp += [option_2]
    while(option_3 in tmp):
        option_3 = db.execute("SELECT a FROM (?) WHERE id = (?)", x, randint(1,l))[0]["a"]
    tmp += [option_3]
    while(option_4 in tmp):
        option_4 = db.execute("SELECT a FROM (?) WHERE id = (?)", x, randint(1,l))[0]["a"]
    tmp += [option_4]
    while(option_5 in tmp):
        option_5 = db.execute("SELECT a FROM (?) WHERE id = (?)", x, randint(1,l))[0]["a"]
    tmp += [option_5]

    # randomize the order of the options
    order = randint(1,5)
    if order == 1:
        arr += [a,option_2,option_3,option_4,option_5]
    elif order == 2:
        arr += [option_2,a,option_3,option_4,option_5]
    elif order == 3:
        arr += [option_2,option_3,a,option_4,option_5]
    elif order == 4:
        arr += [option_2,option_3,option_4,a,option_5]
    else:
        arr += [option_2,option_3,option_4,option_5,a]
    return arr