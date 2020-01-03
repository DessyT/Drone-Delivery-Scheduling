#First do affinity propagation to get clusters

from sklearn.cluster import AffinityPropagation
from sklearn import metrics
import matplotlib.pyplot as pyplot
from itertools import cycle
import folium
from pyeasyga import pyeasyga
import random
import numpy as np

#Sample map
map = folium.Map(location = [57.151954, -2.091723], width=750, height=500, zoom_start=15)
#Draws locations on map
def addLine(startLat,startLon,endLat,endLon):
    folium.PolyLine(locations = [(startLat, startLon), (endLat, endLon)],
                    line_opacity = 0.5).add_to(map)

#Sample locations
#locs = [[-1,5],[-1,4],[-1,3],[-3,4],[-0.5,2],[-1,-1],[-2,-2],[-0.1,-4],[2,5],[4,2],[6,-2],[3,-4]]

#testlocs ,[57.118804931640625,-2.135918140411377],[57.11985397338867,-2.133693218231201]
locs = [[57.153724670410156,-2.0857126712799072],[57.15508270263672,-2.0886473655700684]]

af = AffinityPropagation(damping=0.7,convergence_iter=15,affinity='euclidean').fit(locs)
clusterCentreLocs = af.cluster_centers_indices_
cluster = []
clusters = []

#For number of clusters
for i in range(len(clusterCentreLocs)):
    cluster = []

    #Check if they match

    for j in range(len(af.labels_)):
        if af.labels_[j] == i:
            cluster.append(locs[j])

    clusters.append(cluster)

print("Affinity Propagation")
print("\nLocations")
print(locs)

print("\nNumber of clusters: ", len(clusterCentreLocs))

print("\nCentral nodes:")
for i in clusterCentreLocs:
    print(locs[i])

print("\nClusters:")
for locData in clusters:

    #Show original clusters
    print("Original: ",locData)
    print("LEN = ", len(locData))
    #Skip GA if there is only 1 location in a cluster
    if (len(locData) == 1):

        lat = locData[0][0]
        lon = locData[0][1]

        #addLine(startLat,startLon,57.151954, -2.091723)
        addLine(57.151954, -2.091723, lat,lon)

    else:

        #Now do GA
        #Location data
        #locData = [[-1,5],[-1,4],[-1,3],[-3,4],[-0.5,2],[-1,-1],[-2,-2],[-0.1,-4],[2,5],[4,2],[6,-2],[3,-4]]

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
        print("Optimal route:", ga.best_individual(),"\n")

        #For producing a map
        best = ga.best_individual()
        best[1].append([57.151954, -2.091723])
        for i in range(len(best[1])):

            #Make sure we don't overflow
            if (i + 1 == len(best[1])):
                start = best[1][i]
                end = best[1][0]
            else:
                start = best[1][i]
                end = best[1][i + 1]

            startLat = start[0]
            startLon = start[1]
            endLat = end[0]
            endLon = end[1]

            print("TEST: ",i, " ",startLat,startLon,endLat,endLon)

            addLine(startLat,startLon,endLat,endLon)

map.save("maps/my_map2.html")
