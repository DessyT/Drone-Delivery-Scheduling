import sys
import os

import kmeans
import db
import HTMLGen
import affinityPropagation
import geneticAlgorithm
import greedyBestFirst
import bearing
import E6B
import weatherdata
import time


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

        #Instantiate classes and global variables
        self.path = os.path.split(os.path.abspath(__file__))[0]+r'/html/routedMap.html'
        self.basePath = os.path.split(os.path.abspath(__file__))[0]+r'/html/baseMap.html'

        self.dbOpenFlag = False
        self.bearingFinder = bearing.BearingFinder()
        self.e6b = E6B.E6B()

        #List of colours for output
        self.colours = ['#e6194b', '#3cb44b', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000','#e6194b', '#3cb44b', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
        self.colourNames = ["crimson","light green","royal blue","orange","dark purple","turquoise","pink","lime green","off pink","teal","mauve","brown","lemon","maroon","mint","olive","sand","navy","grey","white","black","crimson","light green","royal blue","orange","dark purple","turquoise","pink","lime green","off pink","teal","mauve","brown","lemon","maroon","mint","olive","sand","navy","grey","white","black"]

        #For modifying the HTML
        self.noDrones = 0
        self.noCustomers = 0
        self.globalAllPossible = True
        self.globalImpossibleRoutes = []
        self.noRoutes = 0
        self.lengths = []
        self.times = []
        self.routes = []

        #Genetic algorithm params
        self.popSize = 50
        self.noGens = 150

        #Draw the GUI
        self.initUI()

    #Setup out main window GUI items & layout
    def initUI(self):

        self.setGeometry(50,50,800,575)
        self.setWindowTitle("Delivery Scheduler")

        self.lblIntro = QLabel(self)
        self.lblIntro.setText("Welcome to your Delivery Scheduler")
        self.lblIntro.move(10,20)

        self.view = QtWebEngineWidgets.QWebEngineView(self)
        self.view.setGeometry(10,50,500,500)
        self.view.load(QtCore.QUrl().fromLocalFile(self.basePath))

        self.btnAdd = QPushButton(self)
        self.btnAdd.setText("Add")
        self.btnAdd.move(525,170)
        self.btnAdd.clicked.connect(self.btnAddClicked)

        self.lblNoDrones = QLabel(self)
        self.lblNoDrones.setText("Drones:")
        self.lblNoDrones.move(525,52)

        self.txtNoDrones = QLineEdit(self)
        self.txtNoDrones.move(660,50)

        self.lblMaxTime = QLabel(self)
        self.lblMaxTime.setText("Max Flight Time (s):")
        self.lblMaxTime.move(525,82)

        self.txtMaxTime = QLineEdit(self)
        self.txtMaxTime.move(660,80)

        self.lblMaxSpeed = QLabel(self)
        self.lblMaxSpeed.setText("Flight Speed (m/s):")
        self.lblMaxSpeed.move(525,112)

        self.txtMaxSpeed = QLineEdit(self)
        self.txtMaxSpeed.move(660,110)

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

            #Show depot location dialog
            depotDialog = depotLocationDialog()
            if depotDialog.exec_():

                #Get lat and lon
                self.depotLat,self.depotLon = depotDialog.getLatLon()

                #Now cast to tuple and save to db
                item = (self.depotLat,self.depotLon,"depot",0,"TRUE")
                self.database.addItem(item)

                #Get weather data
                self.weather = weatherdata.WeatherData(self.depotLat,self.depotLon)
                self.windDir = self.weather.getWindDirection(self.depotLat,self.depotLon)
                self.windSpeed = self.weather.getWindSpeed(self.depotLat,self.depotLon)

            #Globally declare the mapmaker
            self.mapMaker = HTMLGen.MapMaker(self.depotLat,self.depotLon)

            #Remove everything from existing map and add depot
            self.mapMaker.removeEverything()
            self.mapMaker.addDepot()

            #Reload map
            self.view.load(QtCore.QUrl().fromLocalFile(self.path))

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
            #Allow db operations
            self.dbOpenFlag = True

            #Get depot location
            depotLoc = self.database.getDepotLoc()
            print(depotLoc)
            self.depotLat,self.depotLon = depotLoc[0],depotLoc[1]

            #Get weather data
            self.weather = weatherdata.WeatherData(self.depotLat, self.depotLon)
            self.windDir = self.weather.getWindDirection(self.depotLat, self.depotLon)
            self.windSpeed = self.weather.getWindSpeed(self.depotLat, self.depotLon)

            #Remove everything from existing map
            self.mapMaker = HTMLGen.MapMaker(self.depotLat,self.depotLon)
            self.mapMaker.removeEverything()

            #Get all data for markers and plot
            allData = self.database.getLocsItems()
            self.mapMaker.addDepot()
            self.mapMaker.addMarkers(allData)

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
            #For outputting to html
            self.noCustomers = len(locsTimes)

            #Remove everything from existing map
            self.mapMaker.removeEverything()

            #Find which clustering and search algorithms to use
            clusterAlg = self.drpCluster.currentIndex()
            self.searchAlg = self.drpSearch.currentIndex()

            #Get parameters and validate them
            speedBool,self.droneSpeed = self.validateParam(self.txtMaxSpeed.text())
            timeBool,self.maxTime = self.validateParam(self.txtMaxTime.text())
            dronesBool,self.noDrones = self.validateParam(self.txtNoDrones.text())

            #Holds output for csv
            dataOut = []
            name = ""

            #Only run if params are all valid
            if speedBool and timeBool and dronesBool:

                if clusterAlg == 0:
                    ''' KMEANS '''
                    #Get number of drones from textbox and validate > 0
                    #Defaults to 5 drones if no input or invalid

                    if self.noDrones <= 0:
                        self.noDrones = 5
                        self.txtNoDrones.setText("5")

                    #Get clusters
                    self.clusterer = kmeans.KMeansClusters(locsTimes,self.noDrones,self.depotLat,self.depotLon)
                    clusters = self.clusterer.getClusters()
                else:
                    ''' Affinity Propagation '''
                    clusterer = affinityPropagation.APClusters(locsTimes)
                    clusters = clusterer.getClusters()

                #For holding all lengths
                lens = []

                #Default to 900s (15m) if we get invalid input
                if self.maxTime <= 0:
                    self.maxTime = 900
                    self.txtMaxTime.setText("900")

                tempClusters = []
                allPossible = False
                count = 0
                self.globalImpossibleRoutes = []

                while not allPossible:
                    count = 0
                    self.routes = []
                    tempClusters = []
                    impossibleRoutes = []
                    i = 0

                    #Reset times and distances
                    self.times = []
                    self.lengths = []

                    print("Finding clusters and routes..\n")
                    print(f"{len(clusters)} clusters")

                    runTime = 0
                    runTimeOut = []

                    for cluster in clusters:
                        #Find a route
                        print("\nRoute {}".format(i + 1))
                        print(f"\nRoute {i+1}. Colour = {self.colourNames[i]}")

                        #Select search algorithm we want
                        if self.searchAlg == 0:
                            #GA
                            print("Using genetic algorithm")
                            startTime = time.time()

                            routeFinder = geneticAlgorithm.RouteFinder(cluster,self.droneSpeed,
                                                                       self.windSpeed,self.windDir,
                                                                       self.popSize,self.noGens)
                            route = routeFinder.run()

                            #for csv
                            name = "GA" + str(len(clusters))
                        else:
                            #GBF
                            print("Using greedy best first")
                            startTime = time.time()

                            GBF = greedyBestFirst.GreedyBestFirst(cluster,self.droneSpeed,self.windSpeed,self.windDir)
                            route = GBF.routeFinder()

                            #for csv
                            name = "GBF" + str(len(clusters))

                        runTime += round(time.time() - startTime, 2)
                        runTimeOut.append(runTime)

                        #Get real length
                        realLength,realTime = self.getRealLengthTime(route)
                        print(f"Length of route: {realLength}km")
                        print(f"Time taken: {realTime}s")

                        #For HTML output
                        self.lengths.append(realLength)
                        self.times.append(realTime)

                        """ Not needed, data for report writing
                        #Ouput Dict for csv
                        string = str(realLength) + ":" + str(realTime)
                        #dataOut.append(string)

                        lengthO = str(realLength)
                        timeO = str(realTime)
                        dataOut.append(lengthO)
                        dataOut.append(timeO)
                        """

                        #If the route is too long we split it in 2 and append to temp array
                        #After every route is found, clusters becomes temp clusters
                        if realTime > self.maxTime:

                            #Spaghetti code
                            if [self.depotLat,self.depotLon,0] in cluster:
                                cluster.remove([self.depotLat,self.depotLon,0])

                            #Split into 2 clusters
                            tempClusterer = kmeans.KMeansClusters(cluster,2,self.depotLat,self.depotLon)
                            supertempClusts = tempClusterer.getClusters()

                            #Make sure we don't end here
                            count += 1
                            #If there is only 1 cluster returned the route is already direct and thus impossible
                            if len(supertempClusts) == 1:
                                tempClusters.append(supertempClusts[0])
                                self.routes.append(route)
                                #Just report it for now

                                #Remove from lengths and times arrays
                                self.lengths.remove(realLength)
                                self.times.remove(realTime)

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

                    """ Not needed, just for outputting data for report writing
                    dataOut.insert(0,name)

                    import csv

                    ### OUTPUTTING TO CSV TEMP HERE
                    f = open("data.csv","a")
                    with f:
                        w = csv.writer(f)
                        w.writerow(dataOut)

                    g = open("runtimes.csv", "a")

                    with g:
                        w = csv.writer(g)

                        w.writerow(runTimeOut)
                    """
                    print(f"Original = {self.noDrones}\nNew = {len(tempClusters)}")
                    #Assign new array to loop array
                    clusters = tempClusters

                    #Exit condition
                    if count == 0:
                        i = 0
                        #Draw routes on map
                        for route in self.routes:
                            self.globalAllPossible = True
                            self.mapMaker.addAllLines(route,self.colours[i])
                            i += 1

                        if len(impossibleRoutes) != 0:
                            print("Some customers are too far away")
                            for route in impossibleRoutes:
                                self.globalAllPossible = False
                                self.globalImpossibleRoutes.append(route)

                                #Remove impossible from possible route list
                                self.routes.remove(route)

                        self.noRoutes = len(tempClusters) - len(self.globalImpossibleRoutes)

                        #End loop
                        allPossible = True

                #Refresh map
                self.refreshMap()

                #Modify HTML for overview file
                self.modifyHTML()

            #Throw error if input params are not valid
            else:
                QMessageBox.about(self, "Error", "Ensure input parameters are positive integers")

    #Add button functionality
    def btnAddClicked(self):

        #Call our dialog box
        if not self.dbOpenFlag:
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

                #Redo clustering and path finding to find new best routes
                self.btnRunClicked()

                """ #Old code - finds closest cluster an appends new customer to it.
                    #No guarantee that routes are still optimal
                #Now find closest cluster, get route, show on map
                #Inside try except block in case user hasn't used run function before add
                newLoc = self.database.getNewestItem()
                try:
                    getNew = self.clusterer.addNewToCluster(newLoc)
                    oldCluster = getNew[0]
                    newCluster = getNew[1]
                    # print(f"OLDCLUSTER = {oldCluster}\nNEWCLUST = {newCluster}\n")

                    if self.searchAlg == 0:
                        # GA
                        routeFinder = geneticAlgorithm.RouteFinder(newCluster, self.droneSpeed,
                                                                   self.windSpeed, self.windDir,
                                                                   self.popSize, self.noGens)
                        route = routeFinder.run()
                    else:
                        # GBF
                        GBF = greedyBestFirst.GreedyBestFirst(newCluster,self.droneSpeed,self.windSpeed,self.windDir)
                        route = GBF.routeFinder()

                    # Search location
                    searchLoc = newCluster[0][0]
                    # Don't search on the depot
                    if searchLoc == self.depotLat:
                        searchLoc = newCluster[1][0]
                    # Loop through all items in self.routes to find a matching location
                    # Once we find it, replace the whole route with the new one
                    # For breaking once we find a match
                    itemFoundFlag = False

                    # Loop through all lat lon pairs
                    for i in range(len(self.routes)):
                        for location in self.routes[i]:
                            # If we find it, this location becomes the new route
                            if searchLoc in location:
                                # print(f"Old = {self.routes[i]}\nNew = {route}")
                                # print(f"lens old = {len(self.routes[i])}\nNew = {len(route)}")
                                self.routes[i] = route

                                # Escaping
                                itemFoundFlag = True
                                break

                        # Escaping
                        if itemFoundFlag: break

                    # Now refresh the map
                    self.refreshMap()

                except AttributeError:
                    #Show item added alert
                    QMessageBox.about(self, "Success", "Item added to database\nPress run to see it on the map!")
                """
    #Quit button functionality
    def btnQuitClicked(self):
        sys.exit()

    #Validate our inputs are integers > 0
    def validateParam(self,param):
        try:
            val = int(param)
            if val < 0:
                return False,val
            return True,val
        except ValueError:
            val = 0
            return False,val

    #Refresh the map
    def refreshMap(self):
        #get new mapmaker instance
        mapMaker = HTMLGen.MapMaker(self.depotLat,self.depotLon)

        #Get all data for markers and plot
        allData = self.database.getLocsItems()
        mapMaker.addMarkers(allData)

        i = 0
        #Draw routes on map
        for route in self.routes:
            mapMaker.addAllLines(route,self.colours[i])
            i += 1

        self.view.load(QtCore.QUrl().fromLocalFile(self.path))


    #Calculates the actual length of each route in km
    def getRealLengthTime(self,route):

        distanceTotal = 0
        timeTotal = 0
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
            #Find length in km
            dist = haversine(loc1,loc2)

            #Add to total
            distanceTotal = distanceTotal + dist

            #Now get the time
            #Get flight bearing first
            bearing = self.bearingFinder.getBearing(loc1, loc2)

            time = self.getFlightTime(dist,bearing,self.droneSpeed)

            timeTotal = timeTotal + time

            print(f"{loc1} --> {loc2} Distance: {round(dist,2)}km Time Taken: {round(time,2)}s")

        distanceTotal = round(distanceTotal,2)
        timeTotal = round(timeTotal,2)
        return distanceTotal,timeTotal

    def getFlightTime(self,distance,bearing,droneSpeed):

        correctedDir, dir = self.e6b.getCorrectedDirection(self.windSpeed, self.windDir, bearing, droneSpeed)
        speed = self.e6b.getCorrectedSpeed(self.windSpeed, self.windDir, bearing, droneSpeed, dir)

        #Multiply by 1000 to get to metres
        time = (distance * 1000) / speed
        #print(f"windDir = {windDir}\nwindSpeed = {windSpeed}\ndroneSpeed = {speed}")

        return time

    #Modify the file created by folium to include other data
    def modifyHTML(self,):

        if self.globalAllPossible:
            possible = "All customers are close enough for delivery"
        else:
            possible = "Some customers are too far away for delivery - they appear with no route line to them"

        tableStr = """
            <TABLE style='width:50%;'>
                <TR>
                    <TH style='text-align:center;'>Drone</TH>
                    <TH style='text-align:center;'>Route Colour</TH>
                    <TH style='text-align:center;'>Time (s)</TH>
                    <TH style='text-align:center;'>Distance (km)</TH>
                </TR>
        """

        tableLine = ""
        #Once per drone

        noRuns = 0
        remainder = 0

        ##GET REMAINDER AND MULTIPLE
        if self.noRoutes > self.noDrones:
            remainder = self.noRoutes % self.noDrones

            temp = self.noRoutes - remainder
            noRuns = int(temp / self.noDrones)
        else:
            remainder = 0
            noRuns = 1

        count = 0
        while count < self.noRoutes:
            for i in range(self.noDrones):
                tableLine = f"<TR><TD>Drone {i+1}</TD><TD></TD><TD></TD><TD></TD></TR>"
                tableStr += tableLine
                '''
                tableLine = f"""
                            <TR><TD></TD><TD>{self.colourNames[i]}</TD><TD>{self.times[i]}</TD><TD>{self.lengths[i]}</TD></TR>
                            """
                tableStr += tableLine'''

                #First do x multiples required
                for j in range(noRuns):
                    tableLine = f"""
                            <TR><TD></TD><TD>{self.colourNames[count]}</TD><TD>{self.times[count]}</TD><TD>{self.lengths[count]}</TD></TR>
                        """
                    tableStr += tableLine
                    count += 1

                #Then make sure we do remainder
                if remainder > 0:
                    tableLine = f"""
                               <TR><TD></TD><TD>{self.colourNames[count]}</TD><TD>{self.times[count]}</TD><TD>{self.lengths[count]}</TD></TR>
                           """
                    tableStr += tableLine
                    count += 1
                    remainder -= 1

                if count >= self.noRoutes:
                    break

            '''
            #Make sure deliveries more than the no. drones are given to existing drones
            #Also make sure it goes in the route with the shortest time
            if i == j and search:
                num = self.noDrones + count
                tableLine = f"""
                        <TR><TD></TD><TD>{self.colourNames[num]}</TD><TD>{self.times[num]}</TD><TD>{self.lengths[num]}</TD></TR>
                    """
                tableStr += tableLine
                count += 1
                if count < len(indexArray):
                    j = indexArray[count]
            #Make sure we don't have any remainder
            if remainder > 0:
                tableLine = f"""
                        <TR><TD></TD><TD>{self.colourNames[self.noRoutes-remainder]}</TD><TD>{self.times[-remainder]}</TD><TD>{self.lengths[-remainder]}</TD></TR>
                    """
                tableStr += tableLine
                remainder -= 1
            '''
        tableStr += "</TABLE>"

        #Insert into HTML file
        from bs4 import BeautifulSoup

        with open(self.path) as html:
            soup = BeautifulSoup(html.read(),features='html.parser')

            #Get name of div
            div = soup.findAll("div", {"class":"folium-map"})

            # Build body string
            html_str = f"""
                    <h1>Drone Schedule</h1>
                    <h3>Number of customers: {self.noCustomers}</h3>
                    <h3>Number of drones: {self.noDrones}</h3>
                    <h3>Number of routes: {self.noRoutes}
                    <h3>Wind Speed: {self.windSpeed}m/s</h3>
                    <h3>Wind Bearing: {self.windDir}°</h3>
                    <h3>{possible}</h3>
                    <p>Details of deliveries:</br>
                        {tableStr}
                    </p>
                    {div[0]}
            """

            #Remove everything from body
            soup.body.clear()

            #Replace with new HTML
            new_body = soup.new_tag("div")
            new_body.append(html_str)
            soup.body.insert(0,new_body)

            new_head = soup.new_tag("head")
            css = """
                <STYLE>
                    table,th,td,tr {
                    border:1px solid black;
                    text-align:center;
                    }
                </STYLE>
            """
            new_head.append(css)
            soup.head.insert(0,new_head)
            #So it outputs properly
            new_text = soup.prettify()

        #Replace html chars
        ltFix = new_text.replace("&lt;","<")
        fixedHTML = ltFix.replace("&gt;",">")

        with open("schedule.html",mode="w") as file:
            file.write(fixedHTML)

class depotLocationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    #Layout
    def initUI(self):
        self.setGeometry(50,50,250,250)
        self.setWindowTitle("Select depot location")

        self.lblLat = QLabel("Latitude")
        self.lblLon = QLabel("Longitude")
        self.txtLat = QLineEdit(self)
        self.txtLon = QLineEdit(self)

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
        self.grid.addWidget(self.buttonBox,5,0)
        self.setLayout(self.grid)

    def getLatLon(self):
        lat = self.txtLat.text()
        lon = self.txtLon.text()

        return lat,lon

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
        order = lat + "," + lon + "," + item + "," + time + "," + 'FALSE'

        return order

    #Return item to main form
    def getItems(self):

        item = self.txtItem.text()
        return item

if __name__ == '__main__':

    app = QApplication(sys.argv)
    test = SchedulerUI()
    sys.exit(app.exec())
