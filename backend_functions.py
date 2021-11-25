from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                           QSqlRelationalTableModel)
import createdb
from datetime import date, datetime

THRESHOLD_VALUE = 5
CHECKOUT_CART = []

    
def register(user):
    def check(func, *args):
        if not func(*args):
            raise ValueError(func.__self__.lastError())
    query = QSqlQuery()
    check(query.prepare, createdb.INSERT_USERS_SQL)
    createdb.add_user(query, user.get('username'), user.get('password'), user.get('billing_info'), user.get('shipping_info'))


def login(user):
    query = QSqlQuery('SELECT username, password FROM BOOKS WHERE username = {name}'.format(name=user.get('username')))
    if (query.lastError().isValid()):
        print("Error while logging in")
        print(query.lastError())
        return False
    else:
        return True
 
    
def search(term, searchBy):
     query = QSqlQuery('SELECT ISBN, title, author, pub_name, genre, num_pages, price FROM books WHERE {searching} = {term}'.format(searching=searchBy, term=term))
     if (query.lastError().isValid()):
        print("Error while searching")
        print(query.lastError())
     else:
        return query
  
    
def viewBook(book):
    query = QSqlQuery('SELECT ISBN, title, author, pub_name, genre, num_pages, price FROM books WHERE ISBN = {isbn}'.format(isbn=book.get('ISBN')))
    if (query.lastError().isValid()):
        print("Error while trying to view book")
        print(query.lastError())
    else:
        return query


def add_to_checkout(book):
    quantity = book.get('quantity')
    if (quantity == 0):
        print("This book is currently out of stock. Apologies for the inconvenience")
    else:
        if (book.get('title') in CHECKOUT_CART):
            CHECKOUT_CART[CHECKOUT_CART.index(book.get('title'))]['quantity'] = CHECKOUT_CART[CHECKOUT_CART.index(book.get('title'))].get('quantity') + 1
        else:
           CHECKOUT_CART.append(dict(title=book.get('title'), ISBN=book.get('ISBN'), quantity=1))   
        return CHECKOUT_CART
 
    
def checkout(user, order_id):
    def check(func, *args):
        if not func(*args):
            raise ValueError(func.__self__.lastError())
            
    if (len(CHECKOUT_CART) == 0):
        print("Nothing present in cart")
        return
    else:
        query = QSqlQuery()
        check(query.prepare, createdb.INSERT_ORDERS_SQL) 
        now = datetime.now()
        dateString = now.year + '-' + now.month + '-' + now.day
        for i in range(len(CHECKOUT_CART)):
            for j in range(CHECKOUT_CART[i].get('quantity')):
                createdb.add_order(query, order_id, user.get('username'), CHECKOUT_CART[i].get('ISBN'), dateString)
                query = QSqlQuery('UPDATE BOOKS SET quantity = quantity - 1 WHERE ISBN = {isbn}'.format(isbn=CHECKOUT_CART[i].get('ISBN')))
                if (query.lastError().isValid()):
                    print("Error while changing quantity of books")
                    print(query.lastError())
                    return
                query = QSqlQuery('SELECT ISBN, title, author, pub_name, genre, num_pages, price, quantity FROM BOOKS WHERE ISBN = {isbn}'.format(isbn=CHECKOUT_CART[i].get('ISBN')))
                if (query.lastError().isValid()):
                    print("Error while checking minimum threshold")
                    print(query.lastError())
                else:
                    book=dict(ISBN=query.value(0), title=str(query.value(1)), author=str(query.value(2)),
                          pub_name=str(query.value(3)), genre=str(query.value(4)), num_pages=query.value(5),
                          price=query.value(6), quantity=query.value(7))
                    check_threshold(book)


def track_order(order_id):
    query = QSqlQuery('SELECT ISBN, title, author, pub_name, genre, num_pages, price FROM ORDERS JOIN BOOKS USING(ISBN) WHERE order_id = {oid}'.format(oid=order_id)) 
    if (query.lastError().isValid()):
        print("Error while tracking: ", order_id)
        print(query.lastError())        
    else:
        return query
    
    
def owner_add_book(book):
    def check(func, *args):
        if not func(*args):
            raise ValueError(func.__self__.lastError())
            
    query = QSqlQuery()
    check(query.prepare, createdb.INSERT_BOOKS_SQL)
    createdb.add_book(query, book.get('ISBN'), book.get('title'), book.get('author'), book.get('pub_name'), book.get('genre'), book.get('num_pages'), 
             book.get('price'), book.get('quantity'), book.get('sale_percent'))


def owner_remove_book(book):           
    query = QSqlQuery('DROP FROM BOOKS WHERE ISBN = {isbn}'.format(isbn = book.get('ISBN')))
    if (query.lastError().isValid()):
        print("Error while removing: ", book.get('title'))
        print(query.lastError())    
        
        
def get_report(reportType):
    pass


def transfer_sale(book, publisher):
    query = QSqlQuery('SELECT price, sale_percent FROM BOOKS WHERE ISBN = {isbn}'.format(isbn=book.get('ISBN')))
    if (query.lastError().isValid()):
        print("Error while transferring sales for", book.get('title'))
        print(query.lastError())
    while (query.next()):
        amountTransfer = query.value(0) * (query.value(1)/100)
    print("{book_title} by Publisher {pub_title} sold".format(book_title=book.get('title'), pub_title=publisher.get('pub_name')))
    print('{money:.2f}$ transferred to A/C: {account}'.format(money=amountTransfer, account=publisher.get('account_num')))
 
    
def check_threshold(book):
    query = QSqlQuery('SELECT count(*) FROM ORDERS WHERE ISBN = {isbn}'.format(isbn=book.get('ISBN')))
    if (query.lastError().isValid()):
        print("Error while checking threshold for", book.get('title'))
        print(query.lastError())
    while (query.next()):
       saleCount = query.value(0)
    if (book.get('quantity') < THRESHOLD_VALUE):
        print ('Email sent to {publisher} to order {sales} {book_name} books'.format(publisher=book.get('pub_name'),
                                                                                     sales=saleCount, book_name=book.get('title')))
