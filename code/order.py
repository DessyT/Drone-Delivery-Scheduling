import numpy as np, random, operator

#Class to model a single order
class Order:
    def __init__(self,lat,lon,name):
        self.lat = lat
        self.lon = lon
        self.name = name

    def toString(self):
        return("lat = ",self.lat, "lon = ",self.lon, " name = ",self.name)

    #Get the distance between this location and another
    #Simple euclidean. Not effective for
    def distance(self,location):
        latDiff = abs(self.lat - location.lat)
        lonDiff = abs(self.lon - location.lon)
        distance = np.sqrt((latDiff ** 2) + (lonDiff ** 2))

        return distance

#Test for now
o1 = Order(57.1497,2.0943,"Aberdeen")
o2 = Order(51.5074,0.1278,"London")
o3 = Order(52.5200,13.4050,"Berlin")
o4 = Order(40.7128,74.0060,"New York")
print(o1.toString())
print(o2.toString())

print("Distances")
print(o1.distance(o2))

dist = o1.distance(o4)
dist2 = o3.distance(o4)

print(o1.name, " is ", dist, " distance from ", o4.name)
print(o3.name, " is ", dist2, " distance from ", o4.name)
