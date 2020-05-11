import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
path = "data.csv"

file = open(path,"r")
reader = csv.reader(file)

data = []

#Set to however many graphs u want
for line in reader:
    if line[0] == "GA15":
        data.append(line)
    elif line[0] == "GBF15":
        data.append(line)

#Remove empty items
trimmedData = []
for item in data:
    while item[-1] == '':
        item.pop()
    trimmedData.append(item)

#Remove title
trimmedData[0].pop(0)
trimmedData[1].pop(0)
print(trimmedData)

kms = []
time = []

#Seperate km and time
for item in trimmedData:
    tempKms = []
    tempTime = []
    for elem in item:
        split = elem.split(":")
        tempKms.append(split[0])
        tempTime.append(split[1])

    kms.append(tempKms)
    time.append(tempTime)

timeGA = time[0]
timeGBF = time[1]

GA = []
GBF = []

labels = []

#Convert to ints
for i in range(0,len(timeGA)):
    GA.append(float(timeGA[i]))
    GBF.append(float(timeGBF[i]))

    string = str(i + 1)
    labels.append(string)

print(labels)
tupLabels = tuple(labels)

ax = plt.subplot(111)
x = np.arange(len(labels))
print(x)
#labels = ["Route 1","Route 2","Route 3","Route 4","Route 5","Route 6","Route 7","Route 8","Route 9","Route 10","Route 11","Route 12","Route 13","Route 14","Route 15",]

ax.bar(x-0.1,GA,width=0.2,color="r",align="center",label="Genetic Algorithm")
ax.bar(x+0.1,GBF,width=0.2,color="b",align="center",label="Greedy Best First")

plt.title("Length of time to complete route in seconds")
plt.ylabel("Time")
plt.xlabel("Route")
plt.xticks(x,tupLabels)
plt.legend()

outString = "Length_" + str(len(GA)) + ".png"
plt.savefig(outString)
plt.show()

### FOR ADDING LINES TO GRAPHS

kmGA = kms[0]
kmGBF = kms[1]
print(kmGA)
print(type(kmGA[0]))
