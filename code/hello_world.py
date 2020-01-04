import sys
import os

from PyQt5.QtWidgets import *

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import *

def window():
   app = QApplication(sys.argv)
   widget = QWidget()

   lblIntro = QLabel(widget)
   lblIntro.setText("Welcome to your Delivery Scheduler")
   lblIntro.move(20,20)

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
   btnAdd = QPushButton(widget)
   btnAdd.setText("Add")
   btnAdd.move(600,50)
   btnAdd.clicked.connect(btnAddClicked)

   lblMaxDist = QLabel(widget)
   lblMaxDist.setText("Max Dist:")
   lblMaxDist.move(600,83)

   txtMaxDist = QLineEdit(widget)
   txtMaxDist.move(650,80)

   lblNoDrones = QLabel(widget)
   lblNoDrones.setText("Drones:")
   lblNoDrones.move(600,113)

   txtNoDrones = QLineEdit(widget)
   txtNoDrones.move(650,110)

   view = QtWebEngineWidgets.QWebEngineView(widget)
   view.setGeometry(20,50,500,500)

   view.load(QtCore.QUrl().fromLocalFile(
       os.path.split(os.path.abspath(__file__))[0]+r'/html/my_map2.html'
   ))

   print(os.path.split(os.path.abspath(__file__))[0]+r'/html/my_map2.html')
   widget.setGeometry(50,50,800,800)
   widget.setWindowTitle("Delivery Scheduler")
   widget.show()
   sys.exit(app.exec_())

def btnAddClicked():
    print("kek")


if __name__ == '__main__':
   window()
