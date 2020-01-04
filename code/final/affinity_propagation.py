from sklearn.cluster import AffinityPropagation
from sklearn import metrics
import matplotlib.pyplot as pyplot
from itertools import cycle
import db

#Sample locations
#locs = [[-1,5],[-1,4],[-1,3],[-3,4],[-0.5,2],[-1,-1],[-2,-2],[-0.1,-4],[2,5],[4,2],[6,-2],[3,-4]]

class APClusters:
    def __init__(self):

        self.af = AffinityPropagation(damping=0.7,convergence_iter=15,affinity='euclidean').fit(locData)

    def getCentralNodes(self):
        return self.clusterCentreLocs

    def getClusters(self,locations):

        self.clusterCentreLocs = self.af.cluster_centers_indices_
        self.cluster = []
        self.clusters = []
        self.locations = locations
        '''
        print("\nNumber of clusters: ", len(self.clusterCentreLocs))

        print("\nCentral nodes:")
        for i in self.clusterCentreLocs:
            print(locData[i])
            '''
        #For number of clusters
        for i in range(len(self.clusterCentreLocs)):
            self.cluster = []

            #Check if they match
            for j in range(len(self.af.labels_)):
                if self.af.labels_[j] == i:
                    self.cluster.append(locations[j])

            self.clusters.append(self.cluster)

        return self.clusters


#Testing with DB. Need to get data first
testDB = db.DBHandler("db.sqlite3")
locData = testDB.getAllLocs()

#Now get class and clusters
test = APClusters()
derp = test.getClusters(locData)
for herp in derp:
    print(herp)

'''
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
for group in clusters:
    print(group)
'''
