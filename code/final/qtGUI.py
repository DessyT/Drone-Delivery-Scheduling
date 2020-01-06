import sys
import os

import db
import HTMLGen
import affinityPropagation
import geneticAlgorithm

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

        #Get DB object
        self.database = db.DBHandler("db.sqlite3")
        #Create table if it doesn't exist
        self.database.createTable()

        self.initUI()
        self.bla = 0

    def initUI(self):

        self.setGeometry(50,50,800,800)
        self.setWindowTitle("Delivery Scheduler")

        self.lblIntro = QLabel(self)
        self.lblIntro.setText("Welcome to your Delivery Scheduler")
        self.lblIntro.move(20,20)

        self.btnAdd = QPushButton(self)
        self.btnAdd.setText("Add")
        self.btnAdd.move(600,50)
        self.btnAdd.clicked.connect(self.btnAddClicked)

        self.lblMaxDist = QLabel(self)
        self.lblMaxDist.setText("MaxgeneticAlgorithm Dist:")
        self.lblMaxDist.move(600,83)

        self.txtMaxDist = QLineEdit(self)
        self.txtMaxDist.move(650,80)

        self.lblNoDrones = QLabel(self)
        self.lblNoDrones.setText("Drones:")
        self.lblNoDrones.move(600,113)

        self.txtNoDrones = QLineEdit(self)
        self.txtNoDrones.move(650,110)

        path = os.path.split(os.path.abspath(__file__))[0]+r'/html/baseMap.html'
        self.view = QtWebEngineWidgets.QWebEngineView(self)
        self.view.setGeometry(20,50,500,500)
        self.view.load(QtCore.QUrl().fromLocalFile(path))

        self.show()

    def btnAddClicked(self):

        '''Testing
        if self.bla == 0:
            path = os.path.split(os.path.abspath(__file__))[0]+r'/html/my_map2.html'
            self.view.load(QtCore.QUrl().fromLocalFile(path))

            self.bla = 1
        else:
            path = os.path.split(os.path.abspath(__file__))[0]+r'/html/my_map1.html'
            self.view.load(QtCore.QUrl().fromLocalFile(path))

            self.bla = 0
        '''

        #Call our dialog box
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

            #Get data from DB
            locsTimes = self.database.getLocsTime()
            clusterer = affinityPropagation.APClusters(locsTimes)
            clusters = clusterer.getClusters()

            #Instantiate mapmaker
            mapMaker = HTMLGen.MapMaker()

            #Get all data for markers
            allData = self.database.getLocsItems()
            mapMaker.addMarkers(allData)

            #Plot points on map for each cluster
            for cluster in clusters:
                routeFinder = geneticAlgorithm.RouteFinder(cluster)
                #print("CLUSTER",cluster)
                route = routeFinder.run()
                mapMaker.addAllLines(route)

                realLength = self.getRealLength(route)
                print("LEN",realLength)

            #Refresh the HTML to show changes
            path = os.path.split(os.path.abspath(__file__))[0]+r'/html/routedMap.html'
            self.view.load(QtCore.QUrl().fromLocalFile(path))
            #self.view.page().action(QWebEnginePage.Reload).trigger()

            #Update GUI with new data
            #self.update()

    def getRealLength(self,route):

        total = 0

        for i in range(len(route)):

            #So we don't overflow
            if (i + 1 == len(route)):
                start = route[i]
                end = route[0]
            else:
                start = route[i]
                end = route[i + 1]

            #Start and end lat and lon
            startLat = start[0]
            startLon = start[1]
            endLat = end[0]
            endLon = end[1]

            loc1 = (startLat,startLon)
            loc2 = (endLat,endLon)

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
        #self.lblLat.setText("Latitude")
        #self.lblLon.setText("Longitude")

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

        '''
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lblLat)
        self.layout.addWidget(self.txtLat)
        self.layout.addWidget(self.lblLon)
        self.layout.addWidget(self.txtLon)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        '''

    #Return coordinates to main form
    def getOrder(self):

        lat = self.txtLat.text()
        lon = self.txtLon.text()
        item = self.txtItem.text()
        time = self.txtTime.text()
        order = lat + "," + lon + "," + item + "," + time

        return order

    def getItems(self):

        item = self.txtItem.text()
        return item

        '''
        self.btnAdd = QPushButton(self)
        self.btnAdd.setText("Add")
        self.btnAdd.move(50,150)
        self.btnAdd.clicked.connect(self.btnAddClicked)

        self.btnCancel = QPushButton(self)
        self.btnCancel.setText("Cancel")
        self.btnCancel.move(150,150)
        self.btnCancel.clicked.connect(self.btnCancelClicked)
        '''

        '''
    #Button functions
    def btnAddClicked(self):
        print("Added")
        self.close()
    def btnCancelClicked(self):
        print("Cancelled")
        self.close()
        '''

if __name__ == '__main__':

    app = QApplication(sys.argv)
    test = SchedulerUI()
    sys.exit(app.exec())
