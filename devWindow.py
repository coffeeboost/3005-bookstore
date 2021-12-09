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

class DevWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.create_publishers_view()
        self.create_books_view()
        self.create_users_view()
        self.create_orders_view()

        self.publisher_label = QLabel("Publisher Table")
        self.books_label = QLabel("Books Table")
        self.users_label = QLabel("Users Table")
        self.orders_label = QLabel("Orders Table")

        self.main_layout = QVBoxLayout()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_button_handler)
        self.main_layout.addWidget(self.refresh_button)
        self.main_layout.addWidget(self.publisher_label)
        self.main_layout.addWidget(self._publishers_view)
        self.main_layout.addWidget(self.books_label)
        self.main_layout.addWidget(self._books_view)
        self.main_layout.addWidget(self.users_label)
        self.main_layout.addWidget(self._users_view)
        self.main_layout.addWidget(self.orders_label)
        self.main_layout.addWidget(self._orders_view)

        self.setLayout(self.main_layout)
        self.setWindowTitle("Dev Window")
        self.setMinimumWidth(500)
        self.setMinimumHeight(700)
        self.show()

    def refresh_button_handler(self):
        self.main_layout.removeWidget(self.refresh_button)
        self.main_layout.removeWidget(self.publisher_label)
        self.main_layout.removeWidget(self._publishers_view)
        self.main_layout.removeWidget(self.books_label)
        self.main_layout.removeWidget(self._books_view)
        self.main_layout.removeWidget(self.users_label)
        self.main_layout.removeWidget(self._users_view)
        self.main_layout.removeWidget(self.orders_label)
        self.main_layout.removeWidget(self._orders_view)

        self.create_publishers_view()
        self.create_books_view()
        self.create_users_view()
        self.create_orders_view()

        self.main_layout.addWidget(self.refresh_button)
        self.main_layout.addWidget(self.publisher_label)
        self.main_layout.addWidget(self._publishers_view)
        self.main_layout.addWidget(self.books_label)
        self.main_layout.addWidget(self._books_view)
        self.main_layout.addWidget(self.users_label)
        self.main_layout.addWidget(self._users_view)
        self.main_layout.addWidget(self.orders_label)
        self.main_layout.addWidget(self._orders_view)



    def create_publishers_view(self):
        model = self.create_model("publishers")
        self._publishers_view = self.create_view(model)

    def create_books_view(self):
        model = self.create_model("books")
        self._books_view = self.create_view(model)

    def create_users_view(self):
        model = self.create_model("users")
        self._users_view = self.create_view(model)

    def create_orders_view(self):
        model = self.create_model("orders")
        self._orders_view = self.create_view(model)

    def create_view(self, model):
        view = QTableView()
        view.setModel(model)
        return view

    def create_model(self, name):
        model = QSqlRelationalTableModel()
        model.setTable(name)
        model.select()
        return model
