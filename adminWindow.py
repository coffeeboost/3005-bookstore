"""PySide6 port of the widgets/layouts/basiclayout example from Qt v5.x"""
import createdb
import sys

from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QWidget, QTableView, QTableWidget,
                               QTableWidgetItem, QAbstractItemView, QHeaderView,
                               QMainWindow)

from PySide6.QtCore import QObject, Qt, QSize
from PySide6.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                           QSqlRelationalTableModel)

class AdminWindow(QWidget):

    def __init__(self):
        super().__init__()


        main_layout = QVBoxLayout()

        add_book_but = QPushButton("Add Book")
        add_book_but.clicked.connect(self.handlerA)
        remove_book_but = QPushButton("Remove Book")
        remove_book_but.clicked.connect(self.handlerB)
        view_report_but = QPushButton("View Report")
        view_report_but.clicked.connect(self.handlerC)

        isbn = QLabel("ISBN:")
        self.isbn_le = QLineEdit()
        self.isbn_le_rm = QLineEdit()

        title = QLabel("Title:")
        self.title_le = QLineEdit()

        self.form = QGroupBox()
        layout = QFormLayout()

        layout.addRow(isbn, self.isbn_le)
        layout.addRow(title, self.title_le)
        self.form.setLayout(layout)

        self.form_remove_book = QGroupBox()
        layout_remove_book = QFormLayout()
        layout_remove_book.addRow(isbn, self.isbn_le_rm)
        self.form_remove_book.setLayout(layout_remove_book)

        # self.submit = QDialogButtonBox(QDialogButtonBox.Ok)
        # self.submit.accepted.connect(self.handlerA)


        main_layout.addWidget(QLabel("Add book"))
        main_layout.addWidget(self.form)
        main_layout.addWidget(add_book_but)
        main_layout.addWidget(QLabel("Remove book"))
        main_layout.addWidget(self.form_remove_book)
        main_layout.addWidget(remove_book_but)
        main_layout.addWidget(QLabel("View report"))
        main_layout.addWidget(view_report_but)
        # main_layout.addWidget(self.submit)

        self.setLayout(main_layout)
        self.setWindowTitle("Admin Window")
        self.setMinimumWidth(500)
        self.show()

    def handlerA(self):
        book = {
            "ISBN": self.isbn_le.text(),
            "title": self.title_le.text()
        }
        print(book)

    def handlerB(self):
        print(f"remove {self.isbn_le_rm.text()} book")

    def handlerC(self):
        print("view report")
