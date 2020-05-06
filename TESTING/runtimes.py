import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
path = "runtimes.csv"

file = open(path,"r")
reader = csv.reader(file)
strGA = []
strGBF = []

#Split data into GA and GBF
i = 0
for line in reader:

    if i % 2 == 0:
        strGA.append(line[0])
    else:
        strGBF.append(line[0])

    i += 1

print(strGA)
print(strGBF)

GA = []
GBF = []
labels = []

#Convert to float
for i in range(0,len(strGA)):
    GA.append(float(strGA[i]))
    GBF.append(float(strGBF[i]))

    string = str(i + 1)
    labels.append(string)

print(GA)
print(GBF)

tupLabels = tuple(labels)
print(tupLabels)
#Now do stuff

ax = plt.subplot(111)
x = np.arange(len(tupLabels))
print(x)
#labels = ["Route 1","Route 2","Route 3","Route 4","Route 5","Route 6","Route 7","Route 8","Route 9","Route 10","Route 11","Route 12","Route 13","Route 14","Route 15",]

ax.bar(x-0.1,GA,width=0.2,color="r",align="center",label="Genetic Algorithm")
ax.bar(x+0.1,GBF,width=0.2,color="b",align="center",label="Greedy Best First")

plt.title("Length of time to find routes in seconds")
plt.ylabel("Time")
plt.xlabel("Route")
plt.xticks(x,tupLabels)
plt.legend()

outString = "Times" + str(len(GA)) + ".png"
plt.savefig(outString)
plt.show()
