from sklearn.cluster import KMeans
import db

class KMeansClusters:
    def __init__(self,locTimes,noClusters):

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

            #Append the depot if its not there already
            if not [57.152910, -2.107126,1578318631] in self.cluster:
                self.cluster.append([57.152910, -2.107126,1578318631])

            #self.cluster.append([57.152910, -2.107126,1578318631])
            self.clusters.append(self.cluster)

        return self.clusters

    #To add new a location to an existing cluster
    def addNewToCluster(self,newLoc):

        #Get the closest cluster integer
        newLocList = list(newLoc[0])
        coords = newLocList[:-1]

        #Needs a 2d array
        coords2d = []
        coords2d.append(coords)
        closestCluster = self.kmeans.predict(coords2d)

        print(f"New location is closest to cluster {closestCluster.item(0)}")
        #Point to correct cluster
        element = closestCluster.item(0) - 1

        #Get cluster and append location
        newCluster = self.clusters[element]
        newCluster.append(newLocList)

        #Return
        return newCluster

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

newLoc = testDB.getNewestItem()
clust = test.addNewToCluster(newLoc)
print(clust)'''
