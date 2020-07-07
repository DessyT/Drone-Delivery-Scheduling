import folium
import db
import os

class MapMaker:
    def __init__(self,lat,lon):
        #Create map object and allow click to get location
        self.lat,self.lon = lat,lon
        self.map = folium.Map(location=[lat,lon], width=500, height=500, zoom_start=13)
        self.map.add_child(folium.LatLngPopup())
        #self.routedPath = "html/routedMap.html"
        self.routedPath = os.path.split(os.path.abspath(__file__))[0]+r'/html/routedMap.html'
        #To create a new one if we need self.map.save("html/baseMap.html")

    #Add a single line between two points
    def addLine(self,startLat,startLon,endLat,endLon,colour):
        folium.PolyLine(locations = [(startLat, startLon), (endLat, endLon)],
                        line_opacity = 0.5,color=colour).add_to(self.map)

    #Add depot
    def addDepot(self):
        folium.Marker([self.lat,self.lon],"Depot").add_to(self.map)
        self.map.save(self.routedPath)

    #Add all markers
    def addMarkers(self,allData):

        self.addDepot()

        for i in range(len(allData)):
            lat = allData[i][0]
            lon = allData[i][1]
            item = allData[i][2]

            folium.Marker([lat,lon],item).add_to(self.map)

        self.map.save(self.routedPath)

    #Add every line along a route
    def addAllLines(self,locData,colour):
        for i in range(len(locData)):

            #Make sure we dont overflow
            if (i + 1) < len(locData):
                start = locData[i]
                end = locData[i+1]
            else:
                start = locData[i]
                end = locData[0]

            #Start and end lat and lon
            startLat = start[0]
            startLon = start[1]
            endLat = end[0]
            endLon = end[1]

            #Add this line and save map
            self.addLine(startLat,startLon,endLat,endLon,colour)

            self.map.save(self.routedPath)

    #Creates a blank map for when a new DB is opened or a different algorithm is used to search
    def removeEverything(self):

        self.map = folium.Map(location = [self.lat,self.lon], width=500, height=500, zoom_start=13)
        self.map.add_child(folium.LatLngPopup())
        self.map.save(self.routedPath)

'''
test = MapMaker()
#Testing with DB. Need to get data first
testDB = db.DBHandler("/home/andrew/Documents/uni/project/Drone-Delivery-Scheduling/code/final/aberdeen.sqlite3")
locData = testDB.getLocsTime()
print(locData)
test.addMarkers(locData)
test.removeEverything()
'''