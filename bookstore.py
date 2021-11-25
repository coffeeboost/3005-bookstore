"""PySide6 port of the widgets/layouts/basiclayout example from Qt v5.x"""
import createdb
import sys

from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QWidget, QTableView, QTableWidget,
                               QTableWidgetItem, QAbstractItemView, QHeaderView,
                               QMainWindow, QCompleter, QLineEdit)

from PySide6.QtCore import QObject, Qt, QSize
from PySide6.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                           QSqlRelationalTableModel)


class DevWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.create_book_view()
        self.get_titles()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(QLabel("Books Table"))
        self.info = QDialog()

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

        self.info.setLayout(info_layout)

        self.create_completer()


        self.main_layout.addWidget(self.completer)
        self.main_layout.addWidget(self.book_view)
        self.main_layout.addWidget(self.info)



        self.setLayout(self.main_layout)
        self.setWindowTitle("Bookstore Window")
        self.setMinimumWidth(300)

    def create_completer(self):
        completer = QCompleter(self.titles)
        self.completer = QLineEdit()
        self.completer.setCompleter(completer)


    def get_titles(self):
        model = self.book_view.model()
        self.titles = []
        for row in range(model.rowCount()):
            self.titles.append(str(model.data(model.index(row, 1))))

    def create_book_view(self):
        model = self.create_model("books")
        self.book_view = self.create_view(model)

    def create_view(self, model):
        view = QTableView()
        view.setModel(model)
        for i in range(9):
            view.hideColumn(i)
        view.showColumn(1)
        view.resizeColumnsToContents()
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        view.setSelectionMode(QAbstractItemView.SingleSelection)
        view.selectionModel().currentRowChanged.connect(self.handler)
        return view

    def handler(self, curr, prev):
        selected_row = curr.row()

        model = self.book_view.model()
        ISBN = str(model.data(model.index(selected_row, 0)))
        title = model.data(model.index(selected_row, 1))
        author = model.data(model.index(selected_row, 2))
        pub_name = model.data(model.index(selected_row, 3))
        genre = model.data(model.index(selected_row, 4))
        num_pages = str(model.data(model.index(selected_row, 5)))
        price = str(model.data(model.index(selected_row, 6)))
        quantity = str(model.data(model.index(selected_row, 7)))
        sale_percent = str(model.data(model.index(selected_row, 8)))

        layout = self.info.layout()

        layout.itemAt(0).widget().setText("ISBN: " + ISBN)
        layout.itemAt(1).widget().setText("title: " + title)
        layout.itemAt(2).widget().setText("author: " + author)
        layout.itemAt(3).widget().setText("pub_name: " + pub_name)
        layout.itemAt(4).widget().setText("genre: " + genre)
        layout.itemAt(5).widget().setText("num_pages: " + num_pages)
        layout.itemAt(6).widget().setText("price: " + price)
        layout.itemAt(7).widget().setText("quantity: " + quantity)
        layout.itemAt(8).widget().setText("sale_percent: " + sale_percent)


    def create_model(self, name):
        model = QSqlRelationalTableModel()
        model.setTable(name)
        model.select()
        return model


if __name__ == '__main__':
    app = QApplication(sys.argv)
    createdb.init_db()

    a = DevWindow()
    sys.exit(a.exec())
