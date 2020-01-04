import sqlite3

class DBHandler:

    def __init__(self,path):
        self.dbConnect(path)

    #Connect to DB
    def dbConnect(self,path):
        self.con = sqlite3.connect(path)

    def createTable(self):

        #Connect to DB and get cursor for manipluation
        #con = db_connect(path)
        self.cur = self.con.cursor()

        #Generate table
        sql = """
        CREATE TABLE IF NOT EXISTS orders (
            id integer PRIMARY KEY AUTOINCREMENT,
            lat double NOT NULL,
            lon double NOT NULL);"""

        #Save and disconnect
        self.cur.execute(sql)
        self.con.commit()
        #self.con.close()

    def addItem(self,item):

        self.cur = self.con.cursor()

        sql = """
        INSERT INTO orders (lat,lon)
        VALUES (?,?);"""

        self.cur.execute(sql,item)
        self.con.commit()
        #self.con.close()

'''
test = DBHandler("db.sqlite3")
test.createTable()
item = (57.1497,2.0943)
test.addItem(item)
'''
