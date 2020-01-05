import folium
import db

class MapMaker:
    def __init__(self):
        self.map = folium.Map(location = [57.151954, -2.091723], width=500, height=500, zoom_start=15)

    def addLine(self,startLat,startLon,endLat,endLon):
        folium.PolyLine(locations = [(startLat, startLon), (endLat, endLon)],
                        line_opacity = 0.5).add_to(self.map)

    def addAllLines(self,locData):

        for i in range(len(locData)):

            #So we don't overflow
            if (i + 1 == len(locData)):
                start = locData[i]
                end = locData[0]
            else:
                start = locData[i]
                end = locData[i + 1]

            #Start and end lat and lon
            startLat = start[0]
            startLon = start[1]
            endLat = end[0]
            endLon = end[1]

            #print(startLat,startLon,endLat,endLon)

            self.addLine(startLat,startLon,endLat,endLon)

            self.map.save("html/my_map.html")

'''
test = MapMaker()
#Testing with DB. Need to get data first
testDB = db.DBHandler("db.sqlite3")
locData = testDB.getAllLocs()

test.addAllLines(locData)
'''
