from bookstore import BookstoreWindow
from createdb import init_db
from order_summary import OrderSummaryWindow
from devWindow import DevWindow
from PySide6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    main = BookstoreWindow()
    main.show()

    sys.exit(app.exec())
