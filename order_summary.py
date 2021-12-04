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
        # self.create_orders_view()
        self.order_widget = QTableWidget()
        self.order_widget.setColumnCount(3)
        self.order_widget.setHorizontalHeaderLabels(["ISBN", "title", "quantity"])

        self.button_order = QPushButton("Track order")
        self.button_order.clicked.connect(self.order_view_handler)

        ###
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Orders Table"))

        self.form = QGroupBox()
        layout = QFormLayout()
        self.username_line_edit = QLineEdit()
        layout.addRow(QLabel("Username:"), self.username_line_edit)
        self.form.setLayout(layout)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.handlerA)
        main_layout.addWidget(self.order_widget)
        main_layout.addWidget(self.button_order)
        main_layout.addWidget(self.form)
        main_layout.addWidget(buttonBox)
        self.setLayout(main_layout)

    def handlerA(self):
        print(self.username_line_edit.text())

    def order_view_handler(self):
        print(self.username)
        print(self.order_id)
        if not backend_functions.login(self.username):
            return

        self.orders = backend_functions.track_order(self.order_id)

        for order in self.orders:
            row = self.order_widget.rowCount()
            rowPosition = self.order_widget.rowCount()
            self.order_widget.insertRow(rowPosition)
            self.order_widget.setItem(row, 0, QTableWidgetItem(order.get("ISBN")))
            self.order_widget.setItem(row, 1, QTableWidgetItem(order.get("title")))
            self.order_widget.setItem(row, 2, QTableWidgetItem(order.get("quantity")))
            self.order_widget.setRowCount(row+1)

class OrderSummaryWindow(QMainWindow):
    def __init__(self):
        super(OrderSummaryWindow, self).__init__()
        widget = OrderSummaryWidget()
        self.setCentralWidget(widget)
        self.setWindowTitle("Order Summary Window")
        self.setMinimumWidth(500)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    createdb.init_db()
    a = OrderSummaryWindow()
    a.show()
    sys.exit(app.exec())
