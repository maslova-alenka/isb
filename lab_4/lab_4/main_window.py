import sys
import functions
import time

from PyQt5.QtCore import QBasicTimer, Qt, QSize, QEvent
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QGridLayout, QFormLayout, QLabel, QHBoxLayout,
                             QMainWindow, QMessageBox, QLineEdit, QProgressBar, QPushButton, QSlider,
                             QVBoxLayout, QWidget, QAction, QInputDialog, QFileDialog)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 300)
        self.setWindowTitle('SEARCH OF BANK CARD')
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.btn_bins = QLineEdit(placeholderText="Enter the list of bins")
        self.btn_hash_card = QLineEdit(placeholderText="Enter the hash")
        self.btn_last_number = QLineEdit(placeholderText="Enter the last 4 digits")

        hash_btn = QPushButton('Find the card number by hash', self)
        hash_btn.clicked.connect(lambda: self.find_number())
        luhn_btn = QPushButton('Check the number using the Luhn algorithm')
        luhn_btn.clicked.connect(self.luna_alg)
        graph_btn = QPushButton('Build a graph', self)
        graph_btn.clicked.connect(lambda: self.graph_draw())
        exit_btn = QPushButton('Exit', self)
        exit_btn.clicked.connect(lambda: self.close_event())

        hbox = QVBoxLayout()
        hbox.addWidget(exit_btn)
        hbox.addWidget(hash_btn)
        hbox.addWidget(luhn_btn)
        hbox.addWidget(self.btn_bins)
        hbox.addWidget(self.btn_hash_card)
        hbox.addWidget(self.btn_last_number)
        hbox.addWidget(graph_btn)

        self.centralWidget.setLayout(hbox)

        self.show()

    def find_number(self) -> None:
        bins = self.btn_bins.text().split(",")
        hash_card = self.btn_hash_card.text()
        last_number = self.btn_last_number.text()
        directory = QFileDialog.getSaveFileName(self, "Select the file to save the found number:",
                                                "", "JSON File(*.json)",)[0]
        functions.get_card_number(hash_card, [int(item) for item in bins], last_number)
        QMessageBox.information(None, "Successful", f"The card number will find")



    def luna_alg(self) -> None:
        card_number = QInputDialog.getText(
            self, "Enter the card number", "Card number:"
        )
        card_number = card_number[0]
        if card_number == "":
            QMessageBox.information(
                None, "Enter the card number", "The card number was not entered"
            )
        result = functions.luhn_algorithm(card_number)
        if result is not False:
            QMessageBox.information(
                None, "The result of the check", "The card number is valid"
            )
        else:
            QMessageBox.information(
                None, "The result of the check", "The card number is invalid"
            )

    def graph_draw(self) -> None:
        bins = self.btn_bins.text().split(",")
        if (bins == "") or (self.btn_hash_card == "") or (self.btn_last_number == ""):
            QMessageBox.information(
                None,
                "Not all card details were specified",
                "Please fill in all the card details",
            )
        else:
            QMessageBox.information(None, "Successful", "The schedule is built")

    def close_event(self):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.accept()
        else:
            self.ignore()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
