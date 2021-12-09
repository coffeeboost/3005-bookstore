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
                               QMainWindow, QCompleter, QLineEdit, QRadioButton, QButtonGroup,
                               QMessageBox)
from PySide6.QtCore import QObject, Qt, QSize, QTimer
from PySide6.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                           QSqlRelationalTableModel)
from devWindow import DevWindow
from order_summary import OrderSummaryWindow
from adminWindow import AdminWindow

class BookstoreWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.updated_book = False
        self.cart = []

        self.connect_order_windows()
        self.connect_admin_windows()
        self.connect_dev_window()
        self.create_books_layout()
        self.create_cart_layout()
        self.create_search_layout()

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.open_devW_button) #development mode
        self.left_layout.addWidget(self.open_orderW_button)
        self.left_layout.addWidget(self.open_adminW_button)
        self.refresh_button = QPushButton("refresh button")
        self.refresh_button.clicked.connect(self.refresh_handler)
        self.left_layout.addWidget(self.refresh_button)

        self.mid_layout = QVBoxLayout()
        self.mid_layout.addLayout(self.search_layout)
        self.mid_layout.addLayout(self.books_layout)

        self.right_layout = QVBoxLayout()
        self.right_layout.addLayout(self.cart_layout)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.mid_layout)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)

    def connect_admin_windows(self):
        self.adminw = None
        self.open_adminW_button = QPushButton("open admin window")
        self.open_adminW_button.clicked.connect(self.toggle_adminw)

    def toggle_adminw(self):
        if self.adminw is None:
            self.adminw = AdminWindow()
            self.adminw.show()
        else:
            self.adminw = None  #bug: x'ing window won't toggle

    def connect_dev_window(self):
        self.devw = None
        self.open_devW_button = QPushButton("open dev window")
        self.open_devW_button.clicked.connect(self.toggle_devw)

    def connect_order_windows(self):
        self.orderw = None
        self.open_orderW_button = QPushButton("open order summary")
        self.open_orderW_button.clicked.connect(self.toggle_orderw)

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

    def create_search_layout(self):
        self.completer = QLineEdit()

        titles = []
        for row in range(self.model.rowCount()):
            titles.append(str(self.model.data(self.model.index(row, 1))))

        completer = QCompleter(titles)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompleter(completer)

        cs1 = QRadioButton ("Author")
        cs2 = QRadioButton ("Genre")
        cs3 = QRadioButton ("Publisher")

        self.search_button_group = QButtonGroup()
        self.search_button_group.addButton(cs1)
        self.search_button_group.addButton(cs2)
        self.search_button_group.addButton(cs3)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_handler)

        layout1 = QHBoxLayout()
        layout1.addWidget(cs1)
        layout1.addWidget(cs2)
        layout1.addWidget(cs3)
        layout1.addWidget(self.search_button)

        self.search_layout = QVBoxLayout()
        self.search_layout.addWidget(self.completer)
        self.search_layout.addLayout(layout1)

    def create_books_layout(self):
        self.model = self.create_model("books")
        self.book_view = self.create_view(self.model)
        self.create_book_info_widget()
        self.create_add_to_cart_button()
        self.create_similar_book_button()

        self.books_layout = QVBoxLayout()
        self.books_layout.addWidget(QLabel("Books Table"))
        self.books_layout.addWidget(self.book_view)
        self.books_layout.addWidget(self.info_book)
        self.books_layout.addWidget(self.add_to_cart_button)
        self.books_layout.addWidget(self.similar_button)

    def create_cart_layout(self):
        self.cart_widget = QTableWidget()
        self.cart_widget.setColumnCount(3)
        self.cart_widget.setHorizontalHeaderLabels(["ISBN", "title", "count"])
        self.cart_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.create_username_billing_shipping_form()
        self.create_checkout_button_widget()

        max_width = 300
        self.cart_widget.setMaximumWidth(max_width)
        self.form.setMaximumWidth(max_width)
        self.button_check_out.setMaximumWidth(max_width)

        self.cart_layout = QVBoxLayout()
        self.cart_layout.addWidget(QLabel("Checkout Cart"))
        self.cart_layout.addWidget(self.cart_widget)
        self.cart_layout.addWidget(self.form)
        self.cart_layout.addWidget(self.button_check_out)

    def create_similar_book_button(self):
        self.similar_button = QPushButton("View similar book")
        self.similar_button.clicked.connect(self.view_similar_books_handler)

    def create_username_billing_shipping_form(self):
        self.form = QGroupBox()
        layout = QFormLayout()
        self.username_line_edit = QLineEdit()
        self.billing_line_edit = QLineEdit()
        self.shipping_line_edit = QLineEdit()
        layout.addRow(QLabel("Username:"), self.username_line_edit)
        layout.addRow(QLabel("Billing:"), self.billing_line_edit)
        layout.addRow(QLabel("Shipping:"), self.shipping_line_edit)
        self.form.setLayout(layout)

    def create_book_info_widget(self):
        self.info_book = QDialog()
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel("ISBN:"))
        info_layout.addWidget(QLabel("Title:"))
        info_layout.addWidget(QLabel("Author:"))
        info_layout.addWidget(QLabel("Publisher:"))
        info_layout.addWidget(QLabel("Genre:"))
        info_layout.addWidget(QLabel("# pages:"))
        info_layout.addWidget(QLabel("Price:"))
        info_layout.addWidget(QLabel("Quantity:"))
        self.info_book.setLayout(info_layout)

    def create_add_to_cart_button(self):
        self.add_to_cart_button = QPushButton("Add To Cart")
        self.add_to_cart_button.clicked.connect(self.add_to_cart_handler)

    def create_checkout_button_widget(self):
        self.button_check_out = QPushButton("Check Out")
        self.button_check_out.clicked.connect(self.check_out_handler)

    def display_book_info_handler(self, curr, prev):
        selected_row = curr.row()

        model = self.model

        self.ISBN = str(model.data(model.index(selected_row, 0)))
        self.title = model.data(model.index(selected_row, 1))
        self.author = model.data(model.index(selected_row, 2))
        self.pub_name = model.data(model.index(selected_row, 3))
        self.genre = model.data(model.index(selected_row, 4))
        self.num_pages = str(model.data(model.index(selected_row, 5)))
        self.price = str(model.data(model.index(selected_row, 6)))
        self.quantity = str(model.data(model.index(selected_row, 7)))

        layout = self.info_book.layout()

        layout.itemAt(0).widget().setText("ISBN: " + self.ISBN)
        layout.itemAt(1).widget().setText("Title: " + self.title)
        layout.itemAt(2).widget().setText("Author: " + self.author)
        layout.itemAt(3).widget().setText("Publisher: " + self.pub_name)
        layout.itemAt(4).widget().setText("Genre: " + self.genre)
        layout.itemAt(5).widget().setText("# pages: " + self.num_pages)
        layout.itemAt(6).widget().setText("Price: " + self.price)
        layout.itemAt(7).widget().setText("Quantity: " + self.quantity)

        self.updated_book = True

    def check_out_handler(self):
        res = backend_functions.checkout(dict(username=self.username_line_edit.text(),
                                        billing=self.billing_line_edit.text(),
                                        shipping=self.shipping_line_edit.text()),self.cart)
        if res["error"]:
            self.display_error(res["data"])
        else:
            self.display_message(res["data"])
        self.reset_after_checkout()

    def add_to_cart_handler(self):
        if not self.updated_book:
            return

        book = {
            "ISBN":int(self.ISBN),
            "title":self.title,
            "quantity":1
        }

        if self.book_is_in_cart(book):
            new_count = self.increase_book_count(book)
            row = self.cart_widget.rowCount()
            for i in range(row):
                if self.cart_widget.item(i,0).text() == self.ISBN:
                    self.cart_widget.setItem(i, 2, QTableWidgetItem(str(new_count)))

        if not self.book_is_in_cart(book):
            row = self.cart_widget.rowCount()
            self.cart_widget.insertRow(row)
            self.cart_widget.setItem(row, 0, QTableWidgetItem(self.ISBN))
            self.cart_widget.setItem(row, 1, QTableWidgetItem(self.title))
            self.cart_widget.setItem(row, 2, QTableWidgetItem("1"))
            self.cart.append(book)
            self.cart_widget.setRowCount(row+1)

    def search_handler(self):
        search_by = self.search_button_group.checkedButton().text().lower()
        keyword = self.completer.text()
        keyword = " ".join([w.capitalize() for w in keyword.split(" ")])
        matched = backend_functions.search(keyword, search_by)
        if matched["error"]:
            self.display_error(res["data"])
        else:
            self.display_relevant_books(matched["data"], keyword, search_by)

    def refresh_handler(self):
        self.reset()

    def view_similar_books_handler(self):
        res = backend_functions.view_similar_books(dict(ISBN=int(self.ISBN),genre=self.genre))
        if res["error"]:
            self.display_error(res["data"])
        else:
            self.display_relevant_books(res["data"], self.genre, "genre")

    def book_is_in_cart(self, book):
        for b in self.cart:
            if b.get("ISBN") == book.get("ISBN"):
                return True
        return False

    def increase_book_count(self, book):
        count = 0
        for b in self.cart:
            if b.get("ISBN") == book.get("ISBN"):
                b["quantity"] += 1
                count = b["quantity"]
        return count

    def reset(self):
        self.books_layout.removeWidget(QLabel("Books Table"))
        self.books_layout.removeWidget(self.info_book)
        self.books_layout.removeWidget(self.add_to_cart_button)
        self.books_layout.removeWidget(self.similar_button)
        self.books_layout.removeWidget(self.book_view)

        self.model = self.create_model("books")
        self.book_view = self.create_view(self.model)

        self.books_layout.removeWidget(QLabel("Books Table"))
        self.books_layout.addWidget(self.book_view)
        self.books_layout.addWidget(self.info_book)
        self.books_layout.addWidget(self.add_to_cart_button)
        self.books_layout.addWidget(self.similar_button)

    def reset_after_checkout(self):
        self.books_layout.removeWidget(QLabel("Books Table"))
        self.books_layout.removeWidget(self.info_book)
        self.books_layout.removeWidget(self.add_to_cart_button)
        self.books_layout.removeWidget(self.similar_button)
        self.books_layout.removeWidget(self.book_view)

        self.model = self.create_model("books")
        self.book_view = self.create_view(self.model)
        self.cart = []
        self.updated_book = False
        self.cart_widget.clear()
        self.cart_widget.setRowCount(0)
        self.username_line_edit.setText("")

        self.books_layout.removeWidget(QLabel("Books Table"))
        self.books_layout.addWidget(self.book_view)
        self.books_layout.addWidget(self.info_book)
        self.books_layout.addWidget(self.add_to_cart_button)
        self.books_layout.addWidget(self.similar_button)

    def display_error(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(error)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    def display_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    def display_relevant_books(self, book_arr, keyword, search_by):
        process_results = ""
        for book in book_arr:
            process_results += f"{book['title']}\n"
        if len(process_results) == 0:
            process_results = "No books relevant"

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"Relevant books to {keyword} searched by {search_by}")
        msg.setDetailedText(process_results)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec()

    def create_view(self, model):
        view = QTableView()
        view.setModel(model)
        for i in range(9):
            view.hideColumn(i)
        for i in [1,2,4,7]:
            view.showColumn(i)
        view.resizeColumnsToContents()
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        view.setSelectionMode(QAbstractItemView.SingleSelection)
        view.selectionModel().currentRowChanged.connect(self.display_book_info_handler)
        view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        return view

    def create_model(self, name):
        model = QSqlRelationalTableModel()
        model.setTable(name)
        model.select()
        return model

class BookstoreWindow(QMainWindow):
    def __init__(self):
        super(BookstoreWindow, self).__init__()
        widget = BookstoreWidget()
        self.setCentralWidget(widget)
        self.setWindowTitle("Look Inna Book")
        self.setMinimumWidth(1050)
        self.setMinimumHeight(600)
