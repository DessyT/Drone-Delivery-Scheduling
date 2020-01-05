from pyeasyga import pyeasyga
import random
import db
import numpy as np

#Class to perform a genetic search on given coordinates
class RouteFinder:
    def __init__(self,locData):

        self.ga = pyeasyga.GeneticAlgorithm(locData,
                                    population_size=200,
                                    generations=100,
                                    crossover_probability=0.8,
                                    mutation_probability=0.2,
                                    elitism=True,
                                    maximise_fitness=False)

        self.locData = locData

    #Calculate distance from one location to another
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
    #Calculates the length of the current route and inverts it
    #Larger score = worse
    def fitness(self,route,data):
        pathDistance = 0
        fitness = 0.0
        for i in range(0,len(route)):

            fromLoc = route[i]
            toLoc = 0

            if (i + 1) < len(route):
                toLoc = route[i+1]
            else:
                toLoc = route[0]

            pathDistance += self.distance(fromLoc,toLoc)

        return pathDistance

    #Assign all functions to ga and run
    def run(self):

        if len(self.locData) <= 1:
            return self.locData
        else:
            self.ga.create_individual = self.createIndividual
            self.ga.crossover_function = self.crossover
            self.ga.mutate_function = self.mutate
            self.ga.selection_function = self.selection
            self.ga.fitness_function = self.fitness
            self.ga.run()

            return self.ga.best_individual()[1]



#locData = [[-1,5],[-1,4],[-1,3],[-3,4],[-0.5,2],[-1,-1],[-2,-2],[-0.1,-4],[2,5],[4,2],[6,-2],[3,-4]]
''' WORKING WITH DB
testDB = db.DBHandler("db.sqlite3")
locData = testDB.getAllLocs()

test = RouteFinder(locData)
print(test.run())'''
