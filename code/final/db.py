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
            lon double NOT NULL,
            item varchar(20) NOT NULL);"""

        #Save and disconnect
        self.cur.execute(sql)
        self.con.commit()
        #self.con.close()

    def addItem(self,item):

        sql = """
        INSERT INTO orders (lat,lon,item)
        VALUES (?,?,?);"""

        self.cur.execute(sql,item)
        self.con.commit()
        #self.con.close()

    #Return all locations in a formatted list
    def getAllLocs(self):

        #Get data from DB
        sql = "SELECT lat, lon FROM orders"

        self.cur.execute(sql)

        #Load into array
        result = self.cur.fetchall()

        #Convert tuple to list
        locData = []
        for item in result:
            str = list(item)
            locData.append(str)
        #print(locData)

        return locData


    def getLocsItems(self):

        sql = "SELECT lat, lon, item FROM orders"

        self.cur.execute(sql)

        result = self.cur.fetchall()

        #Convert tuple to list
        allData = []
        for item in result:
            str = list(item)
            allData.append(str)
        #print(allData)

        return allData


#test = DBHandler("db.sqlite3")
#test.createTable()
#item = (57.1497,2.0943,"TEST")
#test.addItem(item)
#test.getAllLocs()
#test.getLocsItems()
