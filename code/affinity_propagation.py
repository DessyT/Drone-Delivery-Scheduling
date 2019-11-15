from sklearn.cluster import AffinityPropagation
from sklearn import metrics
import matplotlib.pyplot as pyplot
from itertools import cycle

#Sample locations
locs = [[-1,5],[-1,4],[-1,3],[-3,4],[-0.5,2],[-1,-1],[-2,-2],[-0.1,-4],[2,5],[4,2],[6,-2],[3,-4]]

af = AffinityPropagation(damping=0.5,convergence_iter=15,affinity='euclidean').fit(locs)
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
print("Locations")
print(locs)

print("Number of clusters: ", len(clusterCentreLocs))

print("Central locations:")
for i in clusterCentreLocs:
    print(locs[i])

print("Clusters:")
for group in clusters:
    print(group)
