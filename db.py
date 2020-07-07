import sqlite3
import psutil
import os
from itertools import chain
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
            item varchar(20) NOT NULL,
            time integer NOT NULL,
            depot BOOL DEFAULT 'FALSE');"""

        #Save and disconnect
        self.cur.execute(sql)
        self.con.commit()

    def addItem(self,item):

        sql = """
        INSERT INTO orders (lat,lon,item,time,depot)
        VALUES (?,?,?,?,?);"""

        self.cur.execute(sql,item)
        self.con.commit()

    #Get depot location
    def getDepotLoc(self):

        #Get data
        sql = "SELECT lat, lon FROM orders WHERE depot = 'TRUE'"
        self.cur.execute(sql)

        #Convert to list
        result = self.cur.fetchall()
        latLon = list(chain(*result))

        return latLon

    #Return all locations in a formatted list
    def getAllLocs(self):

        #Get data from DB
        sql = "SELECT lat, lon FROM orders WHERE depot = 'FALSE'"

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

        sql = "SELECT lat, lon, item FROM orders WHERE depot = 'FALSE'"
        self.cur.execute(sql)
        result = self.cur.fetchall()

        #Convert tuple to list
        data = []
        for item in result:
            str = list(item)
            data.append(str)

        return data

    def getLocsTime(self):

        sql = "SELECT lat, lon, time FROM orders WHERE depot = 'FALSE'"
        self.cur.execute(sql)
        result = self.cur.fetchall()

        #Convert tuple to list
        data = []
        for item in result:
            str = list(item)
            data.append(str)
        #print(allData)

        return data

    def getNewestItem(self):

        sql = "SELECT lat, lon, time FROM orders WHERE depot = 'FALSE' ORDER BY id DESC LIMIT 1 "
        self.cur.execute(sql)
        result = self.cur.fetchall()
        data = list(result[0])

        return data

    def getLocs(self):

        sql = "SELECT lat,lon FROM orders WHERE depot = 'FALSE'"
        self.cur.execute(sql)
        result = self.cur.fetchall()

        #Convert tuple to list
        data = []
        for item in result:
            str = list(item)
            data.append(str)
        #print(allData)

        return data

    #Check if db is connected
    def checkStatus(self,path):

        for proc in psutil.process_iter():
            try:
                files = proc.get_open_files()
                if files:
                    for _file in files:
                        if _file.path == path:
                            return True
            except psutil.NoSuchProcess as err:
                print(err)
        return False

"""
path = os.path.split(os.path.abspath(__file__))[0]+r'/testAberdeen.sqlite3'
print(path)
test = DBHandler(path)
print("1    ",test.getLocsItems())
print("2    ",test.getLocsTime())
print("3    ",test.getDepotLoc())
"""