import pymysql, datetime
from entities import User, Family, Category, Transaction

HOST = 'localhost'
USER = 'root'
PASSWORD = ''
DB = 'moneycareus'

class DataManager:

    def __init__(self):
        self.user = None
        self.family = None
        self.transactions = []
        self.categories = []
        self.family_users = []

    def prepareData(self):
        self.expenses = {}
        for t in self.transactions:
            if t.type != 2: continue
            cat_name = self.getCategoryById(t.category).name
            sum = self.expenses.get(cat_name)
            amount = t.amount
            if sum is None: self.expenses[cat_name] = amount
            else: self.expenses[cat_name] = sum + amount

    def getFamilyUserById(self, id):
        for i in self.family_users:
            if i.id == id: return i
        return None

    def getCategoryById(self, id):
        for i in self.categories:
            if i.id == id: return i
        return Category(-1, "None", -1)

    def loadUserDataById(self, user_id):

        self.transactions.clear()
        self.categories.clear()
        self.family_users.clear()

        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cursor = conn.cursor()
        sql = "SELECT * FROM `users` WHERE `ID` = '%s'" % (user_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        self.user = User(result[0], result[1], result[2], result[3], result[4], result[5])

        sql = "SELECT * FROM `families` WHERE `ID` = '%d'" % (self.user.family_id)
        cursor.execute(sql)
        result = cursor.fetchone()
        self.family = Family(result[0], result[1], result[2], result[3], result[4])

        sql = "SELECT * FROM `categories` WHERE `Owner_ID` = '%d' OR `Owner_ID` = '0'" % (self.user.family_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        for s in result: self.categories.append(Category(s[0], s[1], s[2]))

        sql = "SELECT * FROM `users` WHERE `Family_ID` = '%d'" % (self.user.family_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        for s in result: self.family_users.append(User(s[0], s[1], s[2], s[3], s[4], s[5]))

        sql = "SELECT * FROM `transactions` WHERE `Family_ID` = '%d' ORDER BY `Datetime` DESC" % (self.user.family_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        for s in result:
            if self.family.safemode == 1 and self.user.status == 3:
                b_user = self.getFamilyUserById(s[4])
                if b_user.status != 3: continue
                else: self.transactions.append(Transaction(s[0], s[1], s[2], s[3], s[4], s[5], s[6]))
            else: self.transactions.append(Transaction(s[0], s[1], s[2], s[3], s[4], s[5], s[6]))

        cursor.close()
        conn.close()

    def loadUserData(self, username):
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cursor = conn.cursor()
        sql = "SELECT `ID` FROM `users` WHERE `Username` = '%s'" % (username)
        cursor.execute(sql)
        result = cursor.fetchone()
        user_id = result[0]

        self.loadUserDataById(user_id)

    def checkUsername(self, username):
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cursor = conn.cursor()
        sql = "SELECT COUNT(`ID`) FROM `users` WHERE `Username` = '%s'" % (username)
        cursor.execute(sql)
        return cursor.fetchone()[0]

    def checkUsernamAndPassword(self, username, password):
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cursor = conn.cursor()
        sql = "SELECT COUNT(`ID`) FROM `users` WHERE `Username` = '%s' AND `Password` = '%s'" % (username, password)
        cursor.execute(sql)
        return cursor.fetchone()[0]

    def addFamily(self, username, name, family_name, password, status):
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cursor = conn.cursor()
        sql = "INSERT INTO `families` (`Name`, `Owner_ID`) VALUES ('%s', '%d')" % (family_name, 0)
        cursor.execute(sql)
        family_id = cursor.lastrowid

        sql = "INSERT INTO `users` (`Username`, `Password`, `Name`, `Family_ID`, `Status`) VALUES ('%s', '%s', '%s', '%d', '%s')" % (username, password, name, family_id, status)
        cursor.execute(sql)
        user_id = cursor.lastrowid


        sql = "UPDATE `families` SET `Owner_ID` = '%d' WHERE `ID` = '%d'" % (user_id, family_id)
        cursor.execute(sql)

        conn.commit()
        cursor.close()
        conn.close()

    def addUser(self, username, name, password, family_id, status):
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')
        cursor = conn.cursor()

        sql = "INSERT INTO `users` (`Username`, `Password`, `Name`, `Family_ID`, `Status`) VALUES ('%s', '%s', '%s', '%s', '%s')" % (username, password, name, family_id, status)
        cursor.execute(sql)

        conn.commit()
        cursor.close()
        conn.close()

    def addTransaction(self, type, amount, category, user_id):
        self.loadUserDataById(user_id)
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')

        if int(type) == 1: self.family.balance += float(amount)
        else: self.family.balance -= float(amount)

        cursor = conn.cursor()
        sql = "INSERT INTO `transactions` (`Amount`, `Type`, `Family_ID`, `User_ID`, `Category`, `Datetime`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
              (amount, type, self.user.family_id, self.user.id, category, datetime.datetime.today().timestamp())
        cursor.execute(sql)
        sql = "UPDATE `families` SET `Balance` = '%f' WHERE `ID` = '%d'" % (self.family.balance, self.family.id)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def addCategory(self, name, family_id):
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')

        cursor = conn.cursor()
        sql = "INSERT INTO `categories` (`Name`, `Owner_ID`) VALUES ('%s', '%d')" % \
              (name, family_id)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def updateSafeMode(self, enable, user_id):
        self.loadUserDataById(user_id)
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')

        self.family.safemode = enable

        cursor = conn.cursor()
        sql = "UPDATE `families` SET `SafeMode` = '%s' WHERE `ID` = '%s'" % \
              (enable, self.family.id)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def removeCategory(self, id):
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, charset='utf8')

        cursor = conn.cursor()
        sql = "DELETE FROM `categories` WHERE `ID` = '%s'" % \
              (id)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()