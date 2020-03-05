#Nearest Neighbour
from haversine import haversine, Unit

class GreedyBestFirst:

    def __init__(self,allLocs,route):
        print("Using greedy best first")
        self.allLocs = allLocs
        self.route = route

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

        return self.route

    def getDist(self,loc1,loc2):
        #length = haversine(loc,loc2)
        dist = haversine(loc1,loc2,unit="m")
        #print(length)
        return dist

#Test
route = [[6,5]]
allLocs = [[1,6],[7,8],[1,7],[7,5],[3,0]]

GBF = GreedyBestFirst(allLocs,route)
route = GBF.routeFinder()

#self.route = self.routeFinder(self.allLocs,self.route)
print(f"Shortest route:\n{route}")
