import sys
import functions
import working_with_a_file as file

from PyQt5.QtWidgets import (QApplication, QInputDialog, QFileDialog, QMainWindow,
                             QMessageBox, QLineEdit, QPushButton, QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(500, 300)
        self.setWindowTitle('SEARCH OF BANK CARD')
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.btn_bins = QLineEdit(placeholderText="Enter the list of bins")
        self.btn_bins.setStyleSheet('background-color: #fff;')
        self.btn_hash_card = QLineEdit(placeholderText="Enter the hash")
        self.btn_hash_card.setStyleSheet('background-color: #fff;')
        self.btn_last_number = QLineEdit(placeholderText="Enter the last 4 digits")
        self.btn_last_number.setStyleSheet('background-color: #fff;')

        self.hash_btn = QPushButton('Find the card number by hash')
        self.hash_btn.setStyleSheet('background-color: #dbdcff;')
        self.hash_btn.clicked.connect(lambda: self.find_number())
        self.luhn_btn = QPushButton('Check the number using the Luhn algorithm')
        self.luhn_btn.setStyleSheet('background-color: #dbdcff;')
        self.luhn_btn.clicked.connect(self.luna_alg)
        self.graph_btn = QPushButton('Build a graph')
        self.graph_btn.setStyleSheet('background-color: #dbdcff;')
        self.graph_btn.clicked.connect(lambda: self.graph_draw())
        self.exit_btn = QPushButton('Exit')
        self.exit_btn.setStyleSheet('background-color: #dbdcff;')
        self.exit_btn.clicked.connect(lambda: self.close_event())

        hbox = QVBoxLayout()
        hbox.addWidget(self.exit_btn)
        hbox.addWidget(self.hash_btn)
        hbox.addWidget(self.luhn_btn)
        hbox.addWidget(self.graph_btn)
        hbox.addWidget(self.btn_bins)
        hbox.addWidget(self.btn_hash_card)
        hbox.addWidget(self.btn_last_number)

        self.centralWidget.setLayout(hbox)

        self.setStyleSheet('background-color: #B0FFD9;')

        self.show()

    def find_number(self) -> None:
        bins = self.btn_bins.text().split(",")
        hash_card = self.btn_hash_card.text()
        last_number = self.btn_last_number.text()
        if not bins or not hash_card or not last_number:
            QMessageBox.information(
                None,
                "Not all card details were specified",
                "Please fill in all the card details",
            )
            return
        try:
            last_number = int(last_number)
            bins = [int(item) for item in bins]
        except ValueError:
            QMessageBox.information(
                None,
                "Invalid input",
                "Please enter valid values for the last 4 digits and BINs",
            )
            return
        card_number = functions.get_card_number(hash_card, bins, last_number)
        if card_number:
            directory = QFileDialog.getSaveFileName(
                self, "Select the file to save the found number:", "", "JSON File(*.json)"
            )[0]
            if directory:
                file.write_file(directory, card_number)
                QMessageBox.information(
                    None, "Successful", f"The card number has been saved in the file: {directory}"
                    )
        else:
            QMessageBox.information(
                None, "Not found", "The card number was not found based on the provided information."
            )

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
        hash_card = self.btn_hash_card.text()
        last_digit = self.btn_last_number.text()

        if not bins or not hash_card or not last_digit:
            QMessageBox.information(
                None,
                "Not all card details were specified",
                "Please fill in all the card details",
            )
            return
        try:
            last_digit = int(last_digit)
            bins = [int(item) for item in bins]
        except ValueError:
            QMessageBox.information(
                None,
                "Invalid input",
                "Please enter valid values for the last 4 digits and BINs",
            )
            return

        functions.graphing(hash_card, bins, last_digit)

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
