from pyeasyga import pyeasyga
import random
import numpy as np

#Location data
locData = [[-1,5],[-1,4],[-1,3],[-3,4],[-0.5,2],[-1,-1],[-2,-2],[-0.1,-4],[2,5],[4,2],[6,-2],[3,-4]]

#Calculate distance from one location to another
def distance(loc1,loc2):
    xDis = abs(loc1[0] - loc2[0])
    yDis = abs(loc1[1] - loc2[1])
    distance = np.sqrt((xDis ** 2) + (yDis ** 2))
    return distance

ga = pyeasyga.GeneticAlgorithm(locData,
                            population_size=200,
                            generations=100,
                            crossover_probability=0.8,
                            mutation_probability=0.2,
                            elitism=True,
                            maximise_fitness=False)

#Creates a random individual route
def createIndividual(data):
    route = data[:]
    random.shuffle(route)
    return route

#Define crossover function
#Randomly selects a point and switches data between two inputs
#Creates two children from this
def crossover(parent1,parent2):
    crossoverLoc = random.randrange(1,len(parent1))

    child1a = parent1[:crossoverLoc]
    child1b = [i for i in parent2 if i not in child1a]
    child1 = child1a + child1b

    child2a = parent2[crossoverLoc:]
    child2b = [i for i in parent1 if i not in child2a]
    child2 = child2a + child2b

    return child1,child2

#Mutation operation. Randomly selects 2 locations and switches them
def mutate(route):
    loc1 = random.randrange(len(route))
    loc2 = random.randrange(len(route))
    route[loc1], route[loc2] = route[loc2], route[loc1]

#Selection operation
def selection(population):
    return random.choice(population)

#Fitness function
#Calculates the length of the current route and inverts it
#Larger score = worse
def fitness(route,data):
    pathDistance = 0
    fitness = 0.0
    for i in range(0,len(route)):

        fromLoc = route[i]
        toLoc = 0

        if (i + 1) < len(route):
            toLoc = route[i+1]
        else:
            toLoc = route[0]

        pathDistance += distance(fromLoc,toLoc)

    return pathDistance

ga.create_individual = createIndividual
ga.crossover_function = crossover
ga.mutate_function = mutate
ga.selection_function = selection
ga.fitness_function = fitness

ga.run()
print(ga.best_individual())
