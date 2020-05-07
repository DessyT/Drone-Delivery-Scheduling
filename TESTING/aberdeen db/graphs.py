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
kmGA = kms[0]
kmGBF = kms[1]


GA = []
GBF = []
distGA = []
distGBF = []

labels = []

#Convert to ints
for i in range(0,len(timeGA)):
    #Time
    GA.append(float(timeGA[i]))
    GBF.append(float(timeGBF[i]))

    #Distance
    distGA.append(float(kmGA[i]))
    distGBF.append(float(kmGBF[i]))

    string = str(i + 1)
    labels.append(string)

print(labels)
tupLabels = tuple(labels)

ax = plt.subplot(111)
x = np.arange(len(labels))
print(x)
#labels = ["Route 1","Route 2","Route 3","Route 4","Route 5","Route 6","Route 7","Route 8","Route 9","Route 10","Route 11","Route 12","Route 13","Route 14","Route 15",]

barGA = ax.bar(x-0.1,GA,width=0.2,color="r",align="center",label="GA Time")
barGBF = ax.bar(x+0.1,GBF,width=0.2,color="b",align="center",label="GBF Time")
ax.set_ylabel("Time (s)")
ax.set_xlabel("Route no.")

ax2 = ax.twinx()
ax2.set_ylabel("Distance (km)")
lineGA = ax2.plot(distGA,color="darkorange",label="GA Distance")
lineGBF = ax2.plot(distGBF,color="cyan",label="GBF Distance")


plt.title("Genetic Algorithm (GA) vs Greedy Best First (GBF)",y=1.08)
#plt.ylabel("Time")
plt.xlabel("Route")
plt.xticks(x,tupLabels)
#plt.legend()
ax2.legend(handles=[barGA,barGBF,lineGA[0],lineGBF[0]],loc="upper center",bbox_to_anchor=(0.5,1.08),ncol=2)

outString = "Length_" + str(len(GA)) + ".png"
plt.savefig(outString)
plt.show()
