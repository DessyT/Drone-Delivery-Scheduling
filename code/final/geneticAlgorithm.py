from pyeasyga import pyeasyga
import random
import db
import numpy as np
import bearing

import weatherdata
import E6B
from haversine import haversine, Unit

#Class to perform a genetic search on given coordinates
class RouteFinder:
    def __init__(self,data):

        self.ga = pyeasyga.GeneticAlgorithm(data,
                                    population_size=200,
                                    generations=100,
                                    crossover_probability=0.8,
                                    mutation_probability=0.2,
                                    elitism=True,
                                    maximise_fitness=False)

        self.data = data

        self.bearingFinder = bearing.BearingFinder()
        self.e6b = E6B.E6B()

        #Get wind data
        weather = weatherdata.WeatherData(57.1497,-2.0943)
        self.windDir = weather.getWindDirection(57.1497,-2.0943)
        self.windSpeed = weather.getWindSpeed(57.1497,-2.0943)
        #Sample parameters
        self.droneSpeed = 15

    #Calculate distance from one location to another using euclidean
    def distance(self,loc1,loc2):
        xDis = abs(loc1[0] - loc2[0])
        yDis = abs(loc1[1] - loc2[1])
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance

    #Creates a random individual route
    def createIndividual(self,data):
        route = data[:]
        random.shuffle(route)
        return route

    #Define crossover function
    #Randomly selects a point and switches data between two inputs
    #Creates two children from this
    def crossover(self,parent1,parent2):
        crossoverLoc = random.randrange(1,len(parent1))

        child1a = parent1[:crossoverLoc]
        child1b = [i for i in parent2 if i not in child1a]
        child1 = child1a + child1b

        child2a = parent2[crossoverLoc:]
        child2b = [i for i in parent1 if i not in child2a]
        child2 = child2a + child2b

        return child1,child2

    #Mutation operation. Randomly selects 2 locations and switches them
    def mutate(self,route):
        loc1 = random.randrange(len(route))
        loc2 = random.randrange(len(route))
        route[loc1], route[loc2] = route[loc2], route[loc1]

    #Selection operation
    def selection(self,population):
        return random.choice(population)

    #Fitness function
    #Calculates the length of the current route and time customer has waited
    #Larger score = worse
    def fitness(self,route,data):
        fitness = 0.0
        #print(route)
        for i in range(len(route)):

            fromLoc = route[i]
            toLoc = 0

            #Make sure we dont overflow
            if (i + 1) < len(route):
                toLoc = route[i+1]
            else:
                toLoc = route[0]

            #fitness += self.distance(fromLoc,toLoc)

            loc1 = (fromLoc[0],fromLoc[1])
            loc2 = (toLoc[0],toLoc[1])
            #fitness += self.getRealLength(loc1,loc2)

            #Get score for speed of travel
            #Lower speed = worse score

            droneDir = self.getBearing(loc1,loc2)

            correctedDir,dir = self.e6b.getCorrectedDirection(self.windSpeed,self.windDir,droneDir,self.droneSpeed)
            speed = self.e6b.getCorrectedSpeed(self.windSpeed,self.windDir,droneDir,self.droneSpeed,dir)

            #Do speed distance time to calculate time to travel a section
            distance = self.getRealLength(loc1,loc2)

            time = distance / speed
            #print("Time score =,",(time / 10))
            fitness += (time / 10)

            #Get score for bearing
            #The greater the angle, the worse the score

            #fitness += self.getBearing(loc1,loc2)

            #Get score from order time.
            #Unix timestamp is multiplied by position in the queue.
            #Thus GA should tend towards the longest wait being at the front
            #Need to scale down the value so route length is still a factor
            #print("ROUTE",route[i])
            time = route[i][2]
            time = time/1000000000
            #print("Wait score =",(time * i))
            fitness += (time * i)

            #print("Real LEN = ", self.getRealLength(loc1,loc2))
            #print("Real Bearing = ", self.getBearing(loc1,loc2))
            #print("Real time = ",(time * i))

        return fitness

    def getRealLength(self,loc1,loc2):
        #length = haversine(loc,loc2)
        length = haversine(loc1,loc2,unit="m")
        #print(length)
        return length

    #get the difference in angle between wind direction and travel direction
    def getBearing(self,loc1,loc2):

        bearing = self.bearingFinder.getBearing(loc1,loc2)
        #print(bearing)
        return bearing

        '''
        lat1,lon1 = loc1[0],loc1[1]
        lat2,lon2 = loc2[0],loc1[1]

        print("LATS",lat1,lat2)
        print("LONS",lon1,lon2)
        bearing = Geodesic.WGS84.Inverse(lat1, lon2, lat2, lon2)["azi1"]
        print("test",bearing)
        return bearing
        '''
        '''
        WORKS ON PC NOT LAPTOP
        #Calculate the degree of travel
        bearing = sphere.bearing(loc1,loc2)
        print("BEARING",bearing)
        return bearing
        '''

        '''
        lat1,lon1 = loc1[0],loc1[1]
        lat2,lon2 = loc2[0],loc1[1]

        bearing = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)['azi2']
        #bearing = Geodesic.WGS84.Inverse(-41.32, 174.81, 40.96, -5.50)['azi1']
        print("brns",bearing)
        return bearing
        '''

        '''
        lat1,lon1 = loc1[0],loc1[1]
        lat2,lon2 = loc2[0],loc1[1]
        geodesic = pyproj.Geod(ellps='WGS84')
        fwd_azimuth,back_azimuth,distance = geodesic.inv(lat1, lon1, lat2, lon2)
        print("Bearing",fwd_azimuth)
        return fwd_azimuth
        '''

        '''
        #Get the difference between the wind direction and travel direction
        difference = (bearing - self.windDir) % 360.0

        #Normalise to +- 180
        if difference >= 180:
            difference -= 360

        #Convert to positive if negative
        difference = abs(difference) / 100

        return difference'''

    #Assign all functions to ga and run
    def run(self):

        if len(self.data) <= 1:
            return self.data
        else:
            self.ga.create_individual = self.createIndividual
            self.ga.crossover_function = self.crossover
            self.ga.mutate_function = self.mutate
            self.ga.selection_function = self.selection
            self.ga.fitness_function = self.fitness
            self.ga.run()

            coordsList = []

            #We only want to return coords for use later
            for item in self.ga.best_individual()[1]:
                coordsList.append(item[:-1])

            #print("Wind dir = ",self.windDir)
            return coordsList
            #return self.ga.best_individual()[1]

#TEST
'''
testDB = db.DBHandler("aberdeen.sqlite3")
locData = testDB.getLocsTime()
#locData = [[-1,5,1256],[-1,50,123],[-1,-6,123]]
#print(locData)

test = RouteFinder(locData)
print(test.run())
'''
