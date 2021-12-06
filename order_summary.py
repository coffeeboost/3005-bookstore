"""PySide6 port of the widgets/layouts/basiclayout example from Qt v5.x"""
import createdb
import sys

from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                           QDialogButtonBox, QGridLayout, QGroupBox,
                           QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                           QMenu, QMenuBar, QPushButton, QSpinBox,
                           QTextEdit, QVBoxLayout, QWidget, QTableView, QTableWidget,
                           QTableWidgetItem, QAbstractItemView, QHeaderView,
                           QMainWindow, QInputDialog)

from PySide6.QtCore import QObject, Qt, QSize
from PySide6.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                       QSqlRelationalTableModel)

import backend_functions

class OrderSummaryWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.order_widget = QTableWidget()
        self.order_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.order_widget.setColumnCount(4)
        self.order_widget.setHorizontalHeaderLabels(["ISBN", "title", "quantity", "status"])
        self.button_order = QPushButton("Track order")
        self.button_order.clicked.connect(self.order_view_handler)
        self.form = QGroupBox()
        layout = QFormLayout()
        self.order_id_line_edit = QLineEdit()
        layout.addRow(QLabel("Order id:"), self.order_id_line_edit)
        self.form.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Orders Table"))
        main_layout.addWidget(self.order_widget)
        main_layout.addWidget(self.form)
        main_layout.addWidget(self.button_order)

        self.setLayout(main_layout)

    def order_view_handler(self):
        self.order_widget.clear()
        self.order_widget.setRowCount(0)
        self.order_widget.setHorizontalHeaderLabels(["ISBN", "title", "quantity", "status"])
        self.order_id = int(self.order_id_line_edit.text())

        res = backend_functions.track_order(self.order_id)
        if res["error"]:
            print("error")
        else:
            self.orders = res["data"]
            for order in self.orders:
                row = self.order_widget.rowCount()
                rowPosition = self.order_widget.rowCount()
                self.order_widget.insertRow(rowPosition)
                self.order_widget.setItem(row, 0, QTableWidgetItem(str(order.get("ISBN"))))
                self.order_widget.setItem(row, 1, QTableWidgetItem(order.get("title")))
                self.order_widget.setItem(row, 2, QTableWidgetItem(str(order.get("quantity"))))
                self.order_widget.setItem(row, 3, QTableWidgetItem("shipped"))
                self.order_widget.setRowCount(row+1)

class OrderSummaryWindow(QMainWindow):
    def __init__(self):
        super(OrderSummaryWindow, self).__init__()
        widget = OrderSummaryWidget()
        self.setCentralWidget(widget)
        self.setWindowTitle("Order Summary Window")
        self.setMinimumWidth(800)
