from sklearn.cluster import KMeans
import db

class KMeansClusters:
    def __init__(self,locTimes,noClusters):

        #We want to cluster based on coordinates so remove times
        print("TYPE",type(noClusters))

        self.coords = []
        for item in locTimes:
            self.coords.append(item[:-1])

        self.noClusters = int(noClusters)
        self.locTimes = locTimes


    def getCentralNodes(self):
        return self.clusterCentreLocs

    def getClusters(self):

        #Catch if number of drones is > customers
        #If so, just give each customer their own drone
        if self.noClusters > len(self.coords):
            print("Drones > Locations")
            self.noClusters = len(self.coords)
            self.kmeans = KMeans(n_clusters=self.noClusters, random_state=0).fit(self.coords)
        else:
            self.kmeans = KMeans(n_clusters=self.noClusters, random_state=0).fit(self.coords)


        self.clusterCentreLocs = self.kmeans.cluster_centers_
        self.cluster = []
        self.clusters = []

        #For number of clusters
        #i holds the index of each cluster
        for i in range(len(self.clusterCentreLocs)):
            self.cluster = []
            #Check if the indexes match and append to correct cluster array
            #Loop through every item and compare indexes. Append if they match
            for j in range(len(self.kmeans.labels_)):
                if self.kmeans.labels_[j] == i:
                    self.cluster.append(self.locTimes[j])

            #Append the depot
            self.cluster.append([57.152910, -2.107126,1578318631])
            self.clusters.append(self.cluster)

        return self.clusters

        #return None

'''
#Testing with DB. Need to get data first
testDB = db.DBHandler("aberdeen.sqlite3")
locData = testDB.getLocsTime()

#Now get class and clusters
test = KMeansClusters(locData,15)
clusters = test.getClusters()
i = 0
for cluster in clusters:
    i += 1
    print("Cluster:",i,cluster)

    #test = geneticAlgorithm.RouteFinder(herp)
    #print(test.run())
'''
