from pyeasyga import pyeasyga
import random
import db
import numpy as np
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
        for i in range(0,len(route)):

            #Get score from route length only
            fromLoc = route[i]
            toLoc = 0

            #Make sure we dont overflow
            if (i + 1) < len(route):
                toLoc = route[i+1]
            else:
                toLoc = route[0]

            #Get length of each section and add to score
            #print("dist",self.distance(fromLoc,toLoc))
            #print("FROM",fromLoc,"TO",toLoc)
            fitness += self.distance(fromLoc,toLoc)

            #Get score from order time.
            #Unix timestamp is multiplied by position in the queue.
            #Thus GA should tend towards the longest wait being at the front
            #Need to scale down the value so route length is still a factor
            #print("ROUTE",route[i])
            time = route[i][2]
            time = time/1000000000
            #print("time",time * i)
            fitness += (time * i)

            #While looping also get the real length for use later

        return fitness

    def getRealLength(self,loc1,loc2):

        length = haversine(loc,loc2)
        return length


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

            return coordsList
            #return self.ga.best_individual()[1]

#TEST
'''
testDB = db.DBHandler("db.sqlite3")
locData = testDB.getLocsTime()
#locData = [[-1,5,1256],[5,3,123],[123,6,123]]
#print(locData)

test = RouteFinder(locData)
print(test.run())
'''
