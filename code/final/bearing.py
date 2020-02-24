
import math as m

'''
lat1,lon1,lat2,lon2 = 57.1497, -2.0943, 52.5200, -13.4050
print("OUT")
print(lat1)
print(lon1)
print(lat2)
print(lon2)
lonDiff = m.radians(lon2) - m.radians(lon1)
latDiff = lat2 - lat1
y = m.sin(lonDiff) * m.cos(m.radians(lat2))
x = m.cos(m.radians(lat1)) * m.sin(m.radians(lat2)) - m.sin(m.radians(lat1)) * m.cos(m.radians(lat2)) * m.cos(lonDiff)

bearing = m.degrees(m.atan2(y,x))

if (bearing < 0):
    bearing += 360

print("plz",bearing)
'''
class BearingFinder():
    def __init__(self):
        pass

    def getBearing(self,loc1,loc2):
        lat1,lon1 = loc1[0],loc1[1]
        lat2,lon2 = loc2[0],loc2[1]

        lonDiff = m.radians(lon2) - m.radians(lon1)
        latDiff = lat2 - lat1
        y = m.sin(lonDiff) * m.cos(m.radians(lat2))
        x = m.cos(m.radians(lat1)) * m.sin(m.radians(lat2)) - m.sin(m.radians(lat1)) * m.cos(m.radians(lat2)) * m.cos(lonDiff)

        bearing = m.degrees(m.atan2(y,x))

        if (bearing < 0):
            bearing += 360

        return int(bearing)
'''
#TEST
loc1 = [57.1497, -2.0943]
loc2 = [52.5200, -13.4050]
test = BearingFinder()
bearing = test.getBearing(loc1,loc2)
print("plz2",bearing)
'''
