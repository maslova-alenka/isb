import sys
import functions
import time

from PyQt5.QtCore import QBasicTimer, Qt, QSize, QEvent
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QGridLayout, QFormLayout, QLabel, QHBoxLayout,
                             QMainWindow, QMessageBox, QLineEdit, QProgressBar, QPushButton, QSlider,
                             QVBoxLayout, QWidget, QAction)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 300)
        self.setWindowTitle('SEARCH OF BANK CARD')
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        hash_btn = QPushButton('Find the card number by hash', self)
        luhn_btn = QPushButton('Check the number using the Luhn algorithm', self)
        graph_btn = QPushButton('Build a graph', self)
        exit_btn = QPushButton('Exit', self)

        btn_bins = QLineEdit(placeholderText="Enter the list of bins")
        btn_hash_card = QLineEdit(placeholderText="Enter the hash")
        btn_last_number = QLineEdit(placeholderText="Enter the last 4 digits")

        hbox = QVBoxLayout()
        hbox.addWidget(hash_btn)
        hbox.addWidget(luhn_btn)
        hbox.addWidget(graph_btn)
        hbox.addWidget(btn_bins)
        hbox.addWidget(btn_hash_card)
        hbox.addWidget(btn_last_number)
        hbox.addWidget(exit_btn)

        self.centralWidget.setLayout(hbox)

        self.show()

    def close_event(self, event):
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
