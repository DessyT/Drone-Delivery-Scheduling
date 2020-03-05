#Nearest Neighbour
from haversine import haversine, Unit
import db

class GreedyBestFirst:

    def __init__(self,allLocs):
        print("Using greedy best first")
        self.allLocs = allLocs
        self.allLocs = [locs[:-1] for locs in allLocs]
        #Starting location
        self.route = []

    def routeFinder(self):

        #Loop until all locations have been visited
        while len(self.allLocs) >= 1:
            #Keep place
            minDist = 0
            closestLoc = []

            #Find distance from last visisted location and each remaining location
            #Pick shortest distance as next self.route to take
            for loc in self.allLocs:
                #Distance from end of self.route to current loc
                if len(self.route) == 0:
                    legDist = self.getDist(self.allLocs[0],loc)
                else:
                    legDist = self.getDist(self.route[-1],loc)

                #If first run of loop, this dist becomes the min
                if minDist == 0:
                    minDist = legDist
                    closestLoc = loc
                #If we find a shorter distance, use that
                elif legDist < minDist:
                    closestLoc = loc

            #Append shortest distance and remove from available array
            #print(f"testing self.route {self.route}\n")
            #print(f"testing closestLoc {closestLoc}\n")
            self.route.append(closestLoc)
            self.allLocs.remove(closestLoc)

        #Add start point to end of route
        #self.route.append(route[0])

        return self.route

    def getDist(self,loc1,loc2):
        #length = haversine(loc,loc2)
        dist = haversine(loc1,loc2,unit="m")
        #print(length)
        return dist
'''
#Test

route = [[57.152910, -2.107126]]
testDB = db.DBHandler("aberdeen.sqlite3")
locData = testDB.getLocs()

GBF = GreedyBestFirst(locData)
route = GBF.routeFinder()

#self.route = self.routeFinder(self.allLocs,self.route)
print(f"Shortest route:\n{route}")
'''
