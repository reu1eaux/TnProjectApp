import datetime

class User:
    def __init__(self, id, username, password, name, family_id, status):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.family_id = family_id
        self.family = None
        self.status = status
        if self.status == 1: self.status_str = "Глава семьи"
        elif self.status == 2: self.status_str = "Член семьи"
        elif self.status == 3: self.status_str = "Ребенок"

class Family:
    def __init__(self, id, name, owner_id, balance, safemode):
        self.id = id
        self.name = name
        self.owner_id = owner_id
        self.balance = balance
        self.safemode = safemode

class Transaction:
    def __init__(self, id, amount, type, family_id, user_id, category, time):
        self.id = id
        self.amount = amount
        self.type = type
        self.family_id = family_id
        self.user_id = user_id
        self.category = category
        self.time = datetime.datetime.fromtimestamp(time)
        self.time_str = self.time.strftime('%Y.%m.%d %H:%M.%S')

class Category:
    def __init__(self, id, name, owner_id):
        self.id = id
        self.name = name
        self.owner_id = owner_id