import folium
import db

class MapMaker:
    def __init__(self):
        #Create map object and allow click to get location
        self.map = folium.Map(location = [57.151954, -2.091723], width=500, height=500, zoom_start=15)
        self.map.add_child(folium.LatLngPopup())

    def addLine(self,startLat,startLon,endLat,endLon):
        folium.PolyLine(locations = [(startLat, startLon), (endLat, endLon)],
                        line_opacity = 0.5).add_to(self.map)

    def addMarkers(self,allData):

        for i in range(len(allData)):
            print(allData)
            lat = allData[i][0]
            lon = allData[i][1]
            item = allData[i][2]

            folium.Marker([lat,lon],item).add_to(self.map)

            self.map.save("html/routedMap.html")


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

            #Add this line and save map
            self.addLine(startLat,startLon,endLat,endLon)

            self.map.save("html/routedMap.html")


#test = MapMaker()
#Testing with DB. Need to get data first
#testDB = db.DBHandler("db.sqlite3")
#locData = testDB.getAllLocs()

#test.addAllLines([[0,0]])
#test.addMarkers([[5,6,"TEST"]])
