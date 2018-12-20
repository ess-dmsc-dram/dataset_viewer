from datasetviewer.app.MainWindow import MainWindow
from PyQt5 import QtWidgets
import sys

def main():
    """
    Start the application.
    """

    QAPP = QtWidgets.QApplication(sys.argv)
    APP = MainWindow()
    APP.show()
    QAPP.exec_()
