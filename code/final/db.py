import sqlite3

class DBHandler:

    def __init__(self,path):
        self.dbConnect(path)

    #Connect to DB
    def dbConnect(self,path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def createTable(self):

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

        sql = """
        INSERT INTO orders (lat,lon)
        VALUES (?,?);"""

        self.cur.execute(sql,item)
        self.con.commit()
        #self.con.close()

    #Return all locations in a formatted list
    def getAllLocs(self):

        #Get data from DB
        sql = """
        SELECT lat, lon FROM orders"""

        self.cur.execute(sql)

        #Load into array
        result = self.cur.fetchall()

        #Convert tuple to list
        data = []
        for item in result:
            str = list(item)
            data.append(str)
        #print(data)

        return data


#test = DBHandler("db.sqlite3")
#test.createTable()
#item = (57.1497,2.0943)
#test.addItem(item)
#test.getAllLocs()
