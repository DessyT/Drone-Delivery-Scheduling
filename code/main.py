import geneticAlgorithm
import qtGUI
import affinity_propagation
import sys
from PyQt5.QtWidgets import *

locs = [[-1,5],[-1,4],[-1,3],[-3,4],[-0.5,2],[-1,-1],[-2,-2],[-0.1,-4],[2,5],[4,2],[6,-2],[3,-4]]

AP = affinity_propagation.APClusters()
GA = geneticAlgorithm.RouteFinder(locs)

#Testing AP
clusters = AP.getClusters(locs)
print("TESTING AP")
for cluster in clusters:
    print(cluster)

#Testing GA
print("\nTESTING GA", GA.run(),"\n")

#Testing together
print("TESTING AP + GA")
for locData in clusters:
    GA = geneticAlgorithm.RouteFinder(locData)
    print(GA.run())

#Testing GUI
if __name__ == '__main__':

    app = QApplication(sys.argv)
    test = qtGUI.SchedulerUI()
    sys.exit(app.exec())
