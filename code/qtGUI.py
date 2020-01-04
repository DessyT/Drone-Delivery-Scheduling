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

    def initUI(self):

        #widget = QWidget()

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
        self.setGeometry(50,50,800,800)
        self.setWindowTitle("Delivery Scheduler")
        self.show()

    def btnAddClicked(self):
        print("ADD")

'''
if __name__ == '__main__':

    app = QApplication(sys.argv)
    test = SchedulerUI()
    sys.exit(app.exec())
'''
