from sklearn.cluster import AffinityPropagation
from sklearn import metrics
import matplotlib.pyplot as pyplot
from itertools import cycle
import db
import geneticAlgorithm

class APClusters:
    def __init__(self,locTimes):

        #self.af = AffinityPropagation(preference=-10,damping=0.5,convergence_iter=15,affinity='euclidean').fit(locTimes[:-1])
        self.af = AffinityPropagation(preference=-10,damping=0.5,convergence_iter=15,affinity='euclidean').fit(locTimes)
        self.locTimes = locTimes

    def getCentralNodes(self):
        return self.clusterCentreLocs

    def getClusters(self):

        self.clusterCentreLocs = self.af.cluster_centers_indices_
        self.cluster = []
        self.clusters = []

        #For number of clusters
        #i holds the index of each cluster
        for i in range(len(self.clusterCentreLocs)):
            self.cluster = []
            #Check if the indexes match and append to correct cluster array
            #Loop through every item and compare indexes. Append if they match
            for j in range(len(self.af.labels_)):
                print(j)
                if self.af.labels_[j] == i:
                    self.cluster.append(self.locTimes[j])

            #Append the depot
            self.cluster.append([57.152910, -2.107126,1578318631])
            self.clusters.append(self.cluster)


        return self.clusters

'''
#Testing with DB. Need to get data first
testDB = db.DBHandler("db.sqlite3")
locData = testDB.getLocsTime()

#Now get class and clusters
test = APClusters(locData)
derp = test.getClusters()
print("DERP",derp)

for herp in derp:
    print("HERP",herp)
    test = geneticAlgorithm.RouteFinder(herp)
    print(test.run())
'''
