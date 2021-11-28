"""PySide6 port of the widgets/layouts/basiclayout example from Qt v5.x"""
import createdb
import sys
import backend_functions
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QWidget, QTableView, QTableWidget,
                               QTableWidgetItem, QAbstractItemView, QHeaderView,
                               QMainWindow, QCompleter, QLineEdit)
from PySide6.QtCore import QObject, Qt, QSize, QTimer
from PySide6.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                           QSqlRelationalTableModel)
from devWindow import DevWindow
from order_summary import OrderSummaryWindow

class BookstoreWidget(QWidget):

    def __init__(self):
        super().__init__()


        self.updated_book = False
        self.cart = []
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.create_book_view()
        self.create_book_info_widget()
        self.create_completer()
        self.create_cart_button_widget()
        self.create_checkout_button_widget()
        self.create_cart_widget()
        self.connect_dev_window()
        self.connect_order_windows()


        self.left_layout.addWidget(self.completer)
        self.left_layout.addWidget(QLabel("Books Table"))
        self.left_layout.addWidget(self.book_view)
        self.left_layout.addWidget(self.info_book)
        self.left_layout.addWidget(self.button_cart)
        self.right_layout.addWidget(QLabel("Checkout Cart"))
        self.right_layout.addWidget(self.cart_widget)
        self.right_layout.addWidget(self.button_check_out)
        self.main_layout.addWidget(self.dev_but) #!
        self.main_layout.addWidget(self.order_but) #!
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.setLayout(self.main_layout)

    def connect_dev_window(self):
        self.devw = None
        self.dev_but = QPushButton("open dev window")
        self.dev_but.clicked.connect(self.toggle_devw)

    def connect_order_windows(self):
        self.orderw = None
        self.order_but = QPushButton("open order summary")
        self.order_but.clicked.connect(self.toggle_orderw)

    def toggle_orderw(self):
        if self.orderw is None:
            self.orderw = OrderSummaryWindow()
            self.orderw.show()
        else:
            self.orderw = None  #bug: x'ing window won't toggle

    def toggle_devw(self):
        if self.devw is None:
            self.devw = DevWindow()
            self.devw.show()
        else:
            self.devw = None #bug: x'ing window won't toggle

    def create_cart_widget(self):
        self.cart_widget = QTableWidget()
        self.cart_widget.setColumnCount(9)
        self.cart_widget.setHorizontalHeaderLabels(["ISBN", "title", "author", "pub_name", "genre", "num_pages", "price", "quantity", "sale_percent"])

    def create_book_info_widget(self):
        self.info_book = QDialog()
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel("ISBN:"))
        info_layout.addWidget(QLabel("title:"))
        info_layout.addWidget(QLabel("author:"))
        info_layout.addWidget(QLabel("pub_name:"))
        info_layout.addWidget(QLabel("genre:"))
        info_layout.addWidget(QLabel("num_pages:"))
        info_layout.addWidget(QLabel("price:"))
        info_layout.addWidget(QLabel("quantity:"))
        info_layout.addWidget(QLabel("sale_percent:"))
        self.info_book.setLayout(info_layout)

    def create_cart_button_widget(self):
        self.button_cart = QPushButton("Add To Cart")
        self.button_cart.clicked.connect(self.add_to_cart_handler)

    def create_checkout_button_widget(self):
        self.button_check_out = QPushButton("Check Out")
        self.button_check_out.clicked.connect(self.check_out_handler)

    def create_completer(self):
        titles = self._get_titles()
        completer = QCompleter(titles)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer = QLineEdit()
        self.completer.setCompleter(completer)

    def _get_titles(self):
        model = self.book_view.model()
        titles = []
        for row in range(model.rowCount()):
            titles.append(str(model.data(model.index(row, 1))))
        return titles

    def create_book_view(self):
        model = self.create_model("books")
        self.book_view = self.create_view(model)

    def create_view(self, model):
        view = QTableView()
        view.setModel(model)
        for i in range(9):
            view.hideColumn(i)
        for i in [1,2,4]:
            view.showColumn(i)
        view.resizeColumnsToContents()
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        view.setSelectionMode(QAbstractItemView.SingleSelection)
        view.selectionModel().currentRowChanged.connect(self.display_book_info_handler)
        return view

    def create_model(self, name):
        model = QSqlRelationalTableModel()
        model.setTable(name)
        model.select()
        return model

    def display_book_info_handler(self, curr, prev):
        selected_row = curr.row()

        model = self.book_view.model()
        self.ISBN = str(model.data(model.index(selected_row, 0)))
        self.title = model.data(model.index(selected_row, 1))
        self.author = model.data(model.index(selected_row, 2))
        self.pub_name = model.data(model.index(selected_row, 3))
        self.genre = model.data(model.index(selected_row, 4))
        self.num_pages = str(model.data(model.index(selected_row, 5)))
        self.price = str(model.data(model.index(selected_row, 6)))
        self.quantity = str(model.data(model.index(selected_row, 7)))
        self.sale_percent = str(model.data(model.index(selected_row, 8)))

        layout = self.info_book.layout()

        layout.itemAt(0).widget().setText("ISBN: " + self.ISBN)
        layout.itemAt(1).widget().setText("title: " + self.title)
        layout.itemAt(2).widget().setText("author: " + self.author)
        layout.itemAt(3).widget().setText("pub_name: " + self.pub_name)
        layout.itemAt(4).widget().setText("genre: " + self.genre)
        layout.itemAt(5).widget().setText("num_pages: " + self.num_pages)
        layout.itemAt(6).widget().setText("price: " + self.price)
        layout.itemAt(7).widget().setText("quantity: " + self.quantity)
        layout.itemAt(8).widget().setText("sale_percent: " + self.sale_percent)

        self.updated_book = True

    def check_out_handler(self):
        backend_functions.checkout(dict(username="gordontang"), self.cart)

    def add_to_cart_handler(self):
        if not self.updated_book:
            return

        book = {
            "ISBN":int(self.ISBN),
            "title":self.title,
            "author":self.author,
            "pub_name":self.pub_name,
            "genre":self.genre,
            "num_pages":float(self.num_pages),
            "price":float(self.price),
            "quantity":float(self.quantity),
            "sale_percent":float(self.sale_percent)
        }

        if book not in self.cart:
            row = self.cart_widget.rowCount()
            rowPosition = self.cart_widget.rowCount()
            self.cart_widget.insertRow(rowPosition)
            self.cart_widget.setItem(row, 0, QTableWidgetItem(self.ISBN))
            self.cart_widget.setItem(row, 1, QTableWidgetItem(self.title))
            self.cart_widget.setItem(row, 2, QTableWidgetItem(self.author))
            self.cart_widget.setItem(row, 3, QTableWidgetItem(self.pub_name))
            self.cart_widget.setItem(row, 4, QTableWidgetItem(self.genre))
            self.cart_widget.setItem(row, 5, QTableWidgetItem(self.num_pages))
            self.cart_widget.setItem(row, 6, QTableWidgetItem(self.price))
            self.cart_widget.setItem(row, 7, QTableWidgetItem(self.quantity))
            self.cart_widget.setItem(row, 8, QTableWidgetItem(self.sale_percent))
            self.cart.append(book)
            self.cart_widget.setRowCount(row+1)

class BookstoreWindow(QMainWindow):
    def __init__(self):
        super(BookstoreWindow, self).__init__()
        widget = BookstoreWidget()
        self.setCentralWidget(widget)
        self.setWindowTitle("Bookstore Window")
        self.setMinimumWidth(1000)
