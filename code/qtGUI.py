import sys
import os

from PyQt5.QtWidgets import *

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import *

class SchedulerUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.bla = 0

    def initUI(self):

        self.setGeometry(50,50,800,800)
        self.setWindowTitle("Delivery Scheduler")

        self.lblIntro = QLabel(self)
        self.lblIntro.setText("Welcome to your Delivery Scheduler")
        self.lblIntro.move(20,20)

        '''
        btnCluster = QPushButton(widget)
        btnCluster.setText("Cluster")
        btnCluster.move(600,20)
        btnCluster.clicked.connect(btnClusterClicked)

        btnGA = QPushButton(widget)
        btnGA.setText("GA")
        btnGA.move(700,20)
        btnGA.clicked.connect(btnGAClicked)
        '''
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

        path = os.path.split(os.path.abspath(__file__))[0]+r'/html/my_map2.html'
        self.view = QtWebEngineWidgets.QWebEngineView(self)
        self.view.setGeometry(20,50,500,500)
        self.view.load(QtCore.QUrl().fromLocalFile(path))

        print(path)

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
            #Get data from dialog box
            coords = dlg.getLocs()
            print(coords)

        self.lblIntro.setText(coords)
        #Update GUI with new data
        self.update()

#New delivery input dialog
class AddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    #Layout
    def initUI(self):

        self.setGeometry(50,50,250,250)
        self.setWindowTitle("Delivery Scheduler")

        self.txtLat = QLineEdit(self)
        self.txtLon = QLineEdit(self)
        #self.txtLat.move(50,50)
        #self.txtLon.move(50,100)

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.txtLat)
        self.layout.addWidget(self.txtLon)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    #Return coordinates to main form
    def getLocs(self):

        lat = self.txtLat.text()
        lon = self.txtLon.text()
        coords = lat + "," + lon

        return coords

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
