"""PySide6 port of the widgets/layouts/basiclayout example from Qt v5.x"""
import createdb
import sys

# from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QWidget, QTableView, QTableWidget,
                               QTableWidgetItem)

from PySide6.QtCore import QObject, Qt
from PySide6.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                           QSqlRelationalTableModel)
# from PySide6.QtWidgets import QApplication, QTableView


def initializeModel(model):

    model.setTable("books")
    model.setRelation("books")
    model.setRelation(2, QSqlRelation("authors", "id", "name")) #for col 2, join city using id select name

    model.select()


def createView(title, model):

    table_view = QTableView()
    table_view.setModel(model)
    table_view.setItemDelegate(QSqlRelationalDelegate(table_view))
    table_view.setWindowTitle(title)

    return table_view


class Dialog(QDialog):
    num_grid_rows = 3
    num_buttons = 4

    def __init__(self):
        super().__init__()

        self.create_menu()
        self.create_horizontal_group_box()
        self.create_grid_group_box()
        self.create_form_group_box()

        big_editor = QTextEdit()
        big_editor.setPlainText("This widget takes up all the remaining space "
                "in the top-level layout.")

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        model = QSqlRelationalTableModel()
        # initializeModel(model)
        # widget1 = createView("maybe", model)
        widget2 = QTableWidget()
        widget2.setColumnCount(5)

        widget2.setHorizontalHeaderLabels(["ISBN", "title", "author", "pub_name", "genre"])
        query = QSqlQuery("SELECT ISBN, title, author, pub_name, genre FROM books")
        # rows = 1
        while query.next():
            rows = widget2.rowCount()
            '''print(query.value(0))
            print(query.value(1))
            print(query.value(2))
            print(query.value(3))
            print(query.value(4))'''

            widget2.setRowCount(rows + 1)
            widget2.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
            widget2.setItem(rows, 1, QTableWidgetItem(query.value(1)))
            widget2.setItem(rows, 2, QTableWidgetItem(query.value(2)))
            widget2.setItem(rows, 3, QTableWidgetItem(query.value(3)))
            widget2.setItem(rows, 4, QTableWidgetItem(query.value(4)))
            # rows+=1


        main_layout = QVBoxLayout()
        main_layout.setMenuBar(self._menu_bar)
        main_layout.addWidget(self._horizontal_group_box)
        main_layout.addWidget(self._grid_group_box)
        main_layout.addWidget(self._form_group_box)
        main_layout.addWidget(big_editor)
        main_layout.addWidget(button_box)
        main_layout.addWidget(widget2)
        self.setLayout(main_layout)

        self.setWindowTitle("Basic Layouts")

    def create_menu(self):
        self._menu_bar = QMenuBar()

        self._file_menu = QMenu("&File", self)
        self._exit_action = self._file_menu.addAction("E&xit")
        self._menu_bar.addMenu(self._file_menu)

        self._exit_action.triggered.connect(self.accept)

    def create_horizontal_group_box(self):
        self._horizontal_group_box = QGroupBox("Horizontal layout")
        layout = QHBoxLayout()

        for i in range(Dialog.num_buttons):
            button = QPushButton(f"Button {i + 1}")
            layout.addWidget(button)

        self._horizontal_group_box.setLayout(layout)

    def create_grid_group_box(self):
        self._grid_group_box = QGroupBox("Grid layout")
        layout = QGridLayout()

        for i in range(Dialog.num_grid_rows):
            label = QLabel(f"Line {i + 1}:")
            line_edit = QLineEdit()
            layout.addWidget(label, i + 1, 0)
            layout.addWidget(line_edit, i + 1, 1)

        self._small_editor = QTextEdit()
        self._small_editor.setPlainText("This widget takes up about two thirds "
                "of the grid layout.")

        layout.addWidget(self._small_editor, 0, 2, 4, 1)

        layout.setColumnStretch(1, 10)
        layout.setColumnStretch(2, 20)
        self._grid_group_box.setLayout(layout)

    def create_form_group_box(self):
        self._form_group_box = QGroupBox("Form layout")
        layout = QFormLayout()
        layout.addRow(QLabel("Line 1:"), QLineEdit())
        layout.addRow(QLabel("Line 2, long text:"), QComboBox())
        layout.addRow(QLabel("Line 3:"), QSpinBox())
        self._form_group_box.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    createdb.init_db()



    dialog = Dialog()
    sys.exit(dialog.exec())