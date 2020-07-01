from pyeasyga import pyeasyga
import random
import db
import numpy as np
import bearing
import weatherdata
import E6B
from haversine import haversine, Unit
from operator import attrgetter

#Class to perform a genetic search on given coordinates
class RouteFinder:
    def __init__(self,data,droneSpeed,windSpeed,windDir,populationsize,generations):

        self.ga = pyeasyga.GeneticAlgorithm(data,
                                    population_size=populationsize,
                                    generations=generations,
                                    crossover_probability=0.9,
                                    mutation_probability=0.05,
                                    elitism=True,
                                    maximise_fitness=False)

        self.data = data

        self.bearingFinder = bearing.BearingFinder()
        self.e6b = E6B.E6B()

        #Get wind data
        self.windDir = windDir
        self.windSpeed = windSpeed
        #Get drone speed
        self.droneSpeed = droneSpeed

        self.maximise_fitness = False
        self.tournament_size = populationsize // 10

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
    def randomSelection(self,population):
        return random.choice(population)

    def tournamentSelection(self,population):
        if self.tournament_size == 0:
            self.tournament_size = 2
        members = random.sample(population, self.tournament_size)
        members.sort(key=attrgetter('fitness'), reverse=self.maximise_fitness)
        return members[0]

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
            #Thus GA should tend towards the longest waiting customer being at the front
            #Need to scale down the value so route length is still a factor
            #print("ROUTE",route[i])
            #unixTime = route[i][2]
            #unixTime = unixTime/1000000000
            #print("Wait score =",(time * i))
            #fitness += (unixTime * i)

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


    #Assign all functions to ga and run
    def run(self):

        if len(self.data) <= 1:
            return self.data
        else:
            self.ga.create_individual = self.createIndividual
            self.ga.crossover_function = self.crossover
            self.ga.mutate_function = self.mutate
            self.ga.selection_function = self.tournamentSelection
            self.ga.fitness_function = self.fitness
            self.ga.run()

            coordsList = []

            #We only want to return coords for use later
            for item in self.ga.best_individual()[1]:
                coordsList.append(item[:-1])

            #print("Wind dir = ",self.windDir)
            return coordsList
            #print(self.ga.best_individual())
'''
#TEST

testDB = db.DBHandler("aberdeen.sqlite3")
locData = testDB.getLocsTime()
locData.insert(0,[57.152910, -2.107126,1578318631])
#locData = [[-1,5,1256],[-1,50,123],[-1,-6,123]]
#print(locData)

test = RouteFinder(locData)
print(test.run())
'''
