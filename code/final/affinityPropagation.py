from sklearn.cluster import AffinityPropagation
from sklearn import metrics
import matplotlib.pyplot as pyplot
from itertools import cycle
import db
import geneticAlgorithm

class APClusters:
    def __init__(self,locTimes):

        print(type(locTimes))
        self.af = AffinityPropagation(preference=-10,damping=0.5,convergence_iter=15,affinity='euclidean').fit(locTimes[:-1])
        self.locTimes = locTimes

    def getCentralNodes(self):
        return self.clusterCentreLocs

    def getClusters(self):

        self.clusterCentreLocs = self.af.cluster_centers_indices_
        self.cluster = []
        self.clusters = []
        #self.locTimes = locTimes

        #For number of clusters
        for i in range(len(self.clusterCentreLocs)):
            self.cluster = []
            #print("TEST",self.locTimes)
            #Check if the indexes match and append to correct cluster array
            for j in range(len(self.af.labels_)):
                if self.af.labels_[j] == i:
                    print("LABEL",self.af.labels_[j])
                    self.cluster.append(self.locTimes[j])
            #Append the depot, my flat for now
            self.cluster.append([57.152074,-2.091727,1578318631])
            self.clusters.append(self.cluster)

        #print("No clusters = ",len(self.clusterCentreLocs))
        return self.clusters

#Sample locTimes
#locs = [[-1,5],[-1,4],[-1,3],[-3,4],[-0.5,2],[-1,-1],[-2,-2],[-0.1,-4],[2,5],[4,2],[6,-2],[3,-4]]


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
