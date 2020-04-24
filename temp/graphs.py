import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
path = "data.csv"

file = open(path,"r")
reader = csv.reader(file)

data = []
#Just get for 5 routes
for line in reader:
    if line[0] == "GA5":
        data.append(line)
    elif line[0] == "GBF5":
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

#Convert to ints
for i in range(0,len(timeGA)):
    GA.append(float(timeGA[i]))
    GBF.append(float(timeGBF[i]))

ax = plt.subplot(111)
x = np.arange(1,6)
print(x)
labels = ["Route 1","Route 2","Route 3","Route 4","Route 5"]

ax.bar(x-0.1,GA,width=0.2,color="r",align="center",label="Genetic Algorithm")
ax.bar(x+0.1,GBF,width=0.2,color="b",align="center",label="Greedy Best First")

plt.title("Length of time to complete route in seconds")
plt.ylabel("Time")
plt.xlabel("Route")
plt.legend()

plt.savefig("Length_5.png")
plt.show()
