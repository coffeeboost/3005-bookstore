"""PySide6 port of the widgets/layouts/basiclayout example from Qt v5.x"""
import createdb
import sys

from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QWidget, QTableView, QTableWidget,
                               QTableWidgetItem, QAbstractItemView, QHeaderView,
                               QMainWindow, QRadioButton, QButtonGroup, QMessageBox)

from PySide6.QtCore import QObject, Qt, QSize
from PySide6.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                           QSqlRelationalTableModel)
import backend_functions

class AdminWindow(QWidget):

    def __init__(self):
        super().__init__()


        main_layout = QVBoxLayout()
        cs1 = QRadioButton ("Sales per genre")
        cs2 = QRadioButton ("Sales per author")
        cs3 = QRadioButton ("Sales per publisher")
        self.start_month = QLineEdit()
        self.end_month = QLineEdit()
        self.cs_group = QButtonGroup()
        self.cs_group.addButton(cs1)
        self.cs_group.addButton(cs2)
        self.cs_group.addButton(cs3)

        add_book_but = QPushButton("Add Book")
        add_book_but.clicked.connect(self.owner_add_book_handler)
        remove_book_but = QPushButton("Remove Book")
        remove_book_but.clicked.connect(self.owner_remove_book_handler)
        view_report_but = QPushButton("View Report")
        view_report_but.clicked.connect(self.get_report_handler)

        self.isbn_le = QLineEdit()
        self.title_le = QLineEdit()
        self.author_le = QLineEdit()
        self.pub_name_le = QLineEdit()
        self.genre_le = QLineEdit()
        self.num_pages_le = QLineEdit()
        self.price_le = QLineEdit()
        self.quantity_le = QLineEdit()
        self.sale_percent_le = QLineEdit()

        self.isbn_le_rm = QLineEdit()

        self.form = QGroupBox()
        layout = QFormLayout()
        layout.addRow(QLabel("ISBN:"), self.isbn_le)
        layout.addRow(QLabel("Title:"), self.title_le)
        layout.addRow(QLabel("Author:"), self.author_le)
        layout.addRow(QLabel("Publisher name:"), self.pub_name_le)
        layout.addRow(QLabel("Genre:"), self.genre_le)
        layout.addRow(QLabel("Number of pages:"), self.num_pages_le)
        layout.addRow(QLabel("Price:"), self.price_le)
        layout.addRow(QLabel("Quantity:"), self.quantity_le)
        layout.addRow(QLabel("Sale Percentage:"), self.sale_percent_le)

        self.form.setLayout(layout)

        self.form_remove_book = QGroupBox()
        layout_remove_book = QFormLayout()
        layout_remove_book.addRow(QLabel("ISBN:"), self.isbn_le_rm)
        self.form_remove_book.setLayout(layout_remove_book)

        main_layout.addWidget(QLabel("Add book"))
        main_layout.addWidget(self.form)
        main_layout.addWidget(add_book_but)
        main_layout.addWidget(QLabel("Remove book"))
        main_layout.addWidget(self.form_remove_book)

        #0
        self.form_pub.setLayout(layout)

        self.form_remove_pub = QGroupBox()
        layout_remove_pub = QFormLayout()
        layout_remove_pub.addRow(QLabel("ISBN:"), self.isbn_le_rm)
        self.form_remove_pub.setLayout(layout_remove_book)

        main_layout.addWidget(QLabel("Remove publisher"))
        main_layout.addWidget(self.form_remove_pub)

        main_layout.addWidget(remove_book_but)
        main_layout.addWidget(QLabel("Select the type of report"))
        temp = QHBoxLayout()
        temp.addWidget(cs1)
        temp.addWidget(cs2)
        temp.addWidget(cs3)
        main_layout.addLayout(temp)
        main_layout.addWidget(QLabel("Enter time range"))
        temp = QHBoxLayout()

        temp.addWidget(QLabel("Start month"))
        temp.addWidget(self.start_month)
        temp.addWidget(QLabel("End month"))
        temp.addWidget(self.end_month)
        main_layout.addLayout(temp)

        main_layout.addWidget(QLabel("View report"))
        main_layout.addWidget(view_report_but)

        self.setLayout(main_layout)
        self.setWindowTitle("Admin Window")
        self.setMinimumWidth(500)
        self.show()

    def owner_add_book_handler(self):
        book = {
            "ISBN": int(self.isbn_le.text()),
            "title": self.title_le.text(),
            "author": self.author_le.text(),
            "pub_name": self.pub_name_le.text(),
            "genre": self.genre_le.text(),
            "num_pages": self.num_pages_le.text(),
            "price": float(self.price_le.text()),
            "quantity": int(self.quantity_le.text()),
            "sale_percent": int(self.sale_percent_le.text())
        }
        res = backend_functions.owner_add_book(book)
        self.display_message(res["data"])

    def owner_remove_book_handler(self):
        book = {
            "ISBN": int(self.isbn_le_rm.text()),
        }
        res = backend_functions.owner_remove_book(book)
        self.display_message(res["data"])

    def get_report_handler(self):
        backend_functions.get_report(self.cs_group.checkedButton().text().split(" ")[-1],
                dict(type="M",start=int(self.start_month.text()),end=int(self.end_month.text())))

    def display_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()
