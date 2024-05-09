import sys
import functions
import time

from PyQt5.QtCore import QBasicTimer, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QGridLayout, QFormLayout, QLabel, QHBoxLayout,
                             QMainWindow, QMessageBox, QLineEdit, QProgressBar, QPushButton, QSlider,
                             QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.resize(1200, 900)
        self.setWindowTitle('SEARCH OF BANK CARD')
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        hbox = QHBoxLayout()
        hbox.addSpacing(1)

        vbox = QVBoxLayout()
        vbox.addSpacing(1)
        vbox.addLayout(hbox)

        self.centralWidget.setLayout(vbox)



        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
