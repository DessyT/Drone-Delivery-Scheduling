#Nearest Neighbour
from haversine import haversine, Unit
import db
import bearing
import weatherdata
import E6B
import os

class GreedyBestFirst:

    def __init__(self,allLocs,droneSpeed,windSpeed,windDir):
        print("Using greedy best first")
        self.allLocs = allLocs
        self.allLocs = [locs[:-1] for locs in allLocs]
        self.allTimes = [times[-1] for times in allLocs]
        print(self.allLocs)
        #Starting location
        self.route = []

        self.bearingFinder = bearing.BearingFinder()
        self.e6b = E6B.E6B()

        #Get wind data
        self.windDir = windDir
        self.windSpeed = windSpeed
        #Get drone speed
        self.droneSpeed = droneSpeed

    def routeFinder(self):

        #Loop until all locations have been visited
        while len(self.allLocs) >= 1:
            #Keep place
            minDist = 0
            closestLoc = []

            bestScore = 0
            bestLoc = []

            #Find distance from last visisted location and each remaining location
            #Pick shortest distance as next self.route to take
            for loc in self.allLocs:

                #Distance from end of self.route to current loc
                #if len(self.route) == 0:
                if not self.route:
                    #legDist = self.getDist(self.allLocs[0],loc)
                    legScore = self.heuristic(self.allLocs[0],loc)
                else:
                    #legDist = self.getDist(self.route[-1],loc)
                    legScore = self.heuristic(self.route[-1],loc)

                if bestScore == 0:
                    bestScore = legScore
                    bestLoc = loc
                elif legScore < bestScore:
                    bestScore = legScore
                    bestLoc = loc
            #print(f"testing self.route {self.route}\n")

            #Append shortest distance and remove from available array
            #print(f"testing closestLoc {closestLoc}\n")
            self.route.append(bestLoc)
            self.allLocs.remove(bestLoc)

        #Add start point to end of route
        #self.route.append(route[0])

        return self.route

    def getDist(self,loc1,loc2):
        #length = haversine(loc,loc2)
        dist = haversine(loc1,loc2,unit="m")
        #print(length)
        return dist

    def heuristic(self,loc1,loc2):

        fitness = 0

        #Get desired bearing
        droneDir = self.bearingFinder.getBearing(loc1, loc2)

        #Get required flight bearing and speed
        correctedDir, dir = self.e6b.getCorrectedDirection(self.windSpeed, self.windDir, droneDir, self.droneSpeed)
        speed = self.e6b.getCorrectedSpeed(self.windSpeed, self.windDir, droneDir, self.droneSpeed, dir)

        # Do speed distance time to calculate time to travel a section
        distance = haversine(loc1,loc2,unit="m")

        #Get time
        time = distance / speed

        fitness += (time / 10)

        return fitness

'''#Test

route = [[57.152910, -2.107126]]
path = os.path.split(os.path.abspath(__file__))[0] + r'/aberdeen.sqlite3'

testDB = db.DBHandler(path)
locData = testDB.getLocs()
print(locData)
GBF = GreedyBestFirst(locData,13)
route = GBF.routeFinder()

#self.route = self.routeFinder(self.allLocs,self.route)
print(f"Shortest route:\n{route}")

'''