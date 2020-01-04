# import folium package
import folium
map = folium.Map(location = [57.151954, -2.091723], width=500, height=500, zoom_start=15)

folium.Marker([57.151954, -2.091723], popup="Depot").add_to(map)
folium.Marker([57.152437, -2.095494], popup="Morrisons").add_to(map)

folium.PolyLine(locations = [(57.151954, -2.091723), (57.152437, -2.095494)],
                line_opacity = 0.5).add_to(map)

map.save("html/my_map2.html")
'''
class MapMaker:
    def __init__(self):
        self.map = folium.Map(location = [57.151954, -2.091723], width=500, height=500, zoom_start=15)

    def addLine(self,startLat,startLon,endLat,endLon):
        folium.PolyLine(locations = [(startLat, startLon), (endLat, endLon)],
                        line_opacity = 0.5).add_to(self.map)

    def addAllLines(self,locData):

        #for loc in locData:

        for i in range(len(locData)):

            #Make sure we don't overflow
            if (i + 1 == len(locData)):
                start = locData[1][i]
                end = locData[1][0]
            else:
                start = locData[1][i]
                end = locData[1][i + 1]

            startLat = start[0]
            startLon = start[1]
            endLat = end[0]
            endLon = end[1]

            print("TEST: ",i, " ",startLat,startLon,endLat,endLon)

            addLine(startLat,startLon,endLat,endLon)
'''
