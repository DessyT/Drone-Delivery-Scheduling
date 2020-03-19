import sys
import os

import kmeans
import db
import HTMLGen
import affinityPropagation
import geneticAlgorithm
import greedyBestFirst

from PyQt5.QtWidgets import *

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5 import *

from haversine import haversine, Unit

class SchedulerUI(QWidget):


    def __init__(self):
        super().__init__()
        #Instantiate mapmaker
        self.mapMaker = HTMLGen.MapMaker()
        self.path = os.path.split(os.path.abspath(__file__))[0]+r'/html/routedMap.html'
        self.dbOpenFlag = False

        #List of colours for output
        self.colours = ['#e6194b', '#3cb44b', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']

        self.initUI()

    #Setup out main window GUI
    def initUI(self):

        self.setGeometry(50,50,800,575)
        self.setWindowTitle("Delivery Scheduler")

        self.lblIntro = QLabel(self)
        self.lblIntro.setText("Welcome to your Delivery Scheduler")
        self.lblIntro.move(10,20)

        basePath = os.path.split(os.path.abspath(__file__))[0]+r'/html/baseMap.html'
        self.view = QtWebEngineWidgets.QWebEngineView(self)
        self.view.setGeometry(10,50,500,500)
        self.view.load(QtCore.QUrl().fromLocalFile(basePath))

        self.btnAdd = QPushButton(self)
        self.btnAdd.setText("Add")
        self.btnAdd.move(525,170)
        self.btnAdd.clicked.connect(self.btnAddClicked)

        self.lblMaxDist = QLabel(self)
        self.lblMaxDist.setText("Max Dist:")
        self.lblMaxDist.move(525,82)

        self.txtMaxDist = QLineEdit(self)
        self.txtMaxDist.move(610,80)

        self.lblNoDrones = QLabel(self)
        self.lblNoDrones.setText("Drones:")
        self.lblNoDrones.move(525,52)

        self.txtNoDrones = QLineEdit(self)
        self.txtNoDrones.move(610,50)

        self.btnRun = QPushButton(self)
        self.btnRun.setText("Run")
        self.btnRun.move(610,170)
        self.btnRun.clicked.connect(self.btnRunClicked)

        self.btnQuit = QPushButton(self)
        self.btnQuit.setText("Quit")
        self.btnQuit.move(695,170)
        self.btnQuit.clicked.connect(self.btnQuitClicked)

        self.btnOpenDB = QPushButton(self)
        self.btnOpenDB.setText("Open DB")
        self.btnOpenDB.move(525,140)
        self.btnOpenDB.clicked.connect(self.btnOpenDBClicked)

        self.btnCreateDB = QPushButton(self)
        self.btnCreateDB.setText("Create DB")
        self.btnCreateDB.move(610,140)
        self.btnCreateDB.clicked.connect(self.btnCreateDBClicked)

        self.drpCluster = QComboBox(self)
        self.drpCluster.addItem("kMeans")
        self.drpCluster.addItem("Aff. Prop.")
        self.drpCluster.move(695,140)

        self.drpSearch = QComboBox(self)
        self.drpSearch.addItem("Genetic Algorithm")
        self.drpSearch.addItem("Greedy Best First")
        self.drpSearch.move(525,200)

        self.show()

    #Create new DB button functionality
    def btnCreateDBClicked(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getOpenFileName()", "","sqlite3 files (*.sqlite3)", options=options)
        if self.fileName:
            #Get db object
            self.database = db.DBHandler(self.fileName+".sqlite3")
            #Create table if it doesn't exist
            self.database.createTable()
            #Allow db operations
            self.dbOpenFlag = True

    #Open DB button functionality
    def btnOpenDBClicked(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","sqlite3 files (*.sqlite3)", options=options)
        if self.fileName:
            #Get db object
            self.database = db.DBHandler(self.fileName)
            #Create table if it doesn't exist
            self.database.createTable()

            #Get all data for markers and plot
            allData = self.database.getLocsItems()
            self.mapMaker.addMarkers(allData)
            #Allow db operations
            self.dbOpenFlag = True
            #Refresh the HTML to show changes
            self.view.load(QtCore.QUrl().fromLocalFile(self.path))

    #Run button functionality
    def btnRunClicked(self):

        #If db isn't open show an error
        if(self.dbOpenFlag == False):
            QMessageBox.about(self,"Error","Load or create a database before running")
        else:

            #Get data from DB
            locsTimes = self.database.getLocsTime()

            #Find which clustering and search algorithms to use
            clusterAlg = self.drpCluster.currentIndex()
            self.searchAlg = self.drpSearch.currentIndex()

            if clusterAlg == 0:
                ''' KMEANS '''
                #Get number of drones from textbox and validate > 0
                #Defaults to 5 drones if no input or invalid
                noDrones = int(self.txtNoDrones.text())

                if noDrones <= 0:
                    noDrones = 5
                    self.txtNoDrones.setText("5")

                #Get clusters
                self.clusterer = kmeans.KMeansClusters(locsTimes,noDrones)
                clusters = self.clusterer.getClusters()
            else:
                ''' Affinity Propagation '''
                clusterer = affinityPropagation.APClusters(locsTimes)
                clusters = clusterer.getClusters()

            #For holding all lengths
            lens = []

            maxLen = int(self.txtMaxDist.text())
            #Default to 5 if we get invalid input
            if maxLen <= 0:
                maxLen = 5
                self.txtMaxDist.setText("5")

            self.routes = []
            tempClusters = []
            allPossible = False
            count = 0
            while allPossible == False:
                count = 0
                self.routes = []
                tempClusters = []
                impossibleRoutes = []
                i = 0

                print("Finding clusters and routes..\n")
                print(f"{len(clusters)} clusters")

                for cluster in clusters:
                    #Find a route
                    print("\nRoute {}".format(i + 1))

                    #Select search algorith we want
                    if self.searchAlg == 0:
                        #GA
                        routeFinder = geneticAlgorithm.RouteFinder(cluster)
                        route = routeFinder.run()
                    else:
                        #GBF
                        GBF = greedyBestFirst.GreedyBestFirst(cluster)
                        route = GBF.routeFinder()

                    #Get real length
                    realLength = self.getRealLength(route)
                    print(f"REALLEN {realLength}")

                    #If the route is too long we split it in 2 and append to temp array
                    #After every route is found, clusters becomes temp clusters
                    if realLength > maxLen:

                        #Spaghetti code
                        if [57.152910, -2.107126,1578318631] in cluster:
                            cluster.remove([57.152910, -2.107126,1578318631])

                        #Split into 2 clusters
                        tempClusterer = kmeans.KMeansClusters(cluster,2)
                        supertempClusts = tempClusterer.getClusters()

                        #Make sure we don't end here
                        count += 1
                        #If there is only 1 cluster returned the route is direct and thus impossible
                        if len(supertempClusts) == 1:
                            tempClusters.append(supertempClusts[0])
                            self.routes.append(route)
                            #Just report it for now
                            impossibleRoutes.append(route)
                        else:
                            #Otherwise append new clusters
                            tempClusters.append(supertempClusts[0])
                            tempClusters.append(supertempClusts[1])
                    else:
                        #If it's possible, just append
                        tempClusters.append(cluster)
                        self.routes.append(route)

                    #For colours
                    i += 1

                #Make sure we exit when we stop finding new clusters
                if len(clusters) == len(tempClusters):
                    count = 0

                print(f"Original = {len(clusters)}\nNew = {len(tempClusters)}")
                #Assign new array to loop array
                clusters = tempClusters

                #Exit condition
                if count == 0:
                    i = 0
                    #Draw routes on map
                    for route in self.routes:
                        self.mapMaker.addAllLines(route,self.colours[i])
                        i += 1

                    if len(impossibleRoutes) != 0:
                        print("Some routes aren't possible due to their length:")
                        for route in impossibleRoutes:
                            print(f"Route:\n{route}\n")

                    #End loop
                    allPossible = True

            #Refresh map
            self.refreshMap()

    #Add button functionality
    def btnAddClicked(self):

        #Call our dialog box
        if(self.dbOpenFlag == False):
            QMessageBox.about(self,"Error","Load or create a database before adding")
        else:
            dlg = AddDialog()
            if dlg.exec_():

                #Get data from dialog box and cast to tuple
                order = dlg.getOrder()
                orderList = order.split(",")
                coords = tuple(orderList[:-1])

                #Now cast to tuple for storage
                item = tuple(orderList)

                #Add item to db
                self.database.addItem(item)
                print("Item added",item)

                '''TESTING 
                locsTimes = self.database.getLocsTime()
                noDrones = int(self.txtNoDrones.text())

                noDrones = int(self.txtNoDrones.text())

                if noDrones <= 0:
                    noDrones = 5
                    self.txtNoDrones.setText("5")

                #Get clusters
                self.clusterer = kmeans.KMeansClusters(locsTimes,noDrones)
                clusters = self.clusterer.getClusters()

                 END TESTING DOESNT WORK'''


                #Now find closest cluster, get route, show on map
                newLoc = self.database.getNewestItem()
                newCluster = self.clusterer.addNewToCluster(newLoc)
                print(f"NEWCLUST = {newCluster}\n")

                if self.searchAlg == 0:
                    #GA
                    routeFinder = geneticAlgorithm.RouteFinder(newCluster)
                    route = routeFinder.run()
                else:
                    #GBF
                    GBF = greedyBestFirst.GreedyBestFirst(newCluster)
                    route = GBF.routeFinder()

                #Search location
                searchLoc = newCluster[0][0]
                #Loop through all items in self.routes to find a matching location
                #Once we find it, replace the whole route with the new one
                #For breaking once we find a match
                itemFoundFlag = False

                #Loop through all lat lon pairs
                for i in range(len(self.routes)):
                    for location in self.routes[i]:
                        #If we find it, this location becomes the new route
                        if searchLoc in location:
                            print(f"Old = {self.routes[i]}\nNew = {route}")
                            print(f"lens old = {len(self.routes[i])}\nNew = {len(route)}")
                            self.routes[i] = route

                            #Escaping
                            itemFoundFlag = True
                            break

                    #Escaping
                    if itemFoundFlag: break

                #Now refresh the map
                self.refreshMap()

    def refreshMap(self):
        #get new mapmaker instance
        mapMaker = HTMLGen.MapMaker()

        #Get all data for markers and plot
        allData = self.database.getLocsItems()
        mapMaker.addMarkers(allData)

        i = 0
        #Draw routes on map
        for route in self.routes:
            mapMaker.addAllLines(route,self.colours[i])
            i += 1

        self.view.load(QtCore.QUrl().fromLocalFile(self.path))

    #Quit button functionality
    def btnQuitClicked(self):
        sys.exit()

    #Calculates the actual length of each route in km
    def getRealLength(self,route):

        total = 0
        for i in range(len(route)):
            #Make sure we dont overflow
            if (i + 1) < len(route):
                start = route[i]
                end = route[i+1]
            else:
                start = route[i]
                end = route[0]

            #Start and end lat and lon
            startLat = start[0]
            startLon = start[1]
            endLat = end[0]
            endLon = end[1]

            #Cast to variable
            loc1 = (startLat,startLon)
            loc2 = (endLat,endLon)
            print(f"{loc1} --> {loc2}")
            #Find length in km
            dist = haversine(loc1,loc2)

            total = total + dist

        return total

#New delivery input dialog
class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    #Layout
    def initUI(self):

        self.setGeometry(50,50,250,250)
        self.setWindowTitle("Delivery Scheduler")

        self.lblLat = QLabel("Latitude")
        self.lblLon = QLabel("Longitude")
        self.lblItem = QLabel("Item")
        self.lblTime = QLabel("Time")

        self.txtLat = QLineEdit(self)
        self.txtLon = QLineEdit(self)
        self.txtItem = QLineEdit(self)
        self.txtTime = QLineEdit(self)
        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.grid = QGridLayout()
        self.grid.setSpacing(2)
        self.grid.addWidget(self.lblLat,1,0)
        self.grid.addWidget(self.txtLat,1,1)
        self.grid.addWidget(self.lblLon,2,0)
        self.grid.addWidget(self.txtLon,2,1)
        self.grid.addWidget(self.lblItem,3,0)
        self.grid.addWidget(self.txtItem,3,1)
        self.grid.addWidget(self.lblTime,4,0)
        self.grid.addWidget(self.txtTime,4,1)
        self.grid.addWidget(self.buttonBox,5,0)
        self.setLayout(self.grid)

    #Return coordinates to main form
    def getOrder(self):

        lat = self.txtLat.text()
        lon = self.txtLon.text()
        item = self.txtItem.text()
        time = self.txtTime.text()
        order = lat + "," + lon + "," + item + "," + time

        return order

    #Return item to main form
    def getItems(self):

        item = self.txtItem.text()
        return item

if __name__ == '__main__':

    app = QApplication(sys.argv)
    test = SchedulerUI()
    sys.exit(app.exec())
