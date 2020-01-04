import sys
import os
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

app = QtWidgets.QApplication(sys.argv)
view = QtWebEngineWidgets.QWebEngineView()

view.load(QtCore.QUrl().fromLocalFile(
    os.path.split(os.path.abspath(__file__))[0]+r'/html/my_map2.html'
))

view.show()
sys.exit(app.exec_())
