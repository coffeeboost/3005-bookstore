from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                           QSqlRelationalTableModel)

PUBLISHERS_SQL = """
CREATE TABLE PUBLISHERS
(
	pub_name	varchar(70),
	address		varchar(200),
	email		varchar(50),
	account_num	numeric(12, 0) UNIQUE,
	phone_num	numeric(10, 0) UNIQUE,
	PRIMARY KEY (pub_name)
);
"""

BOOKS_SQL ="""
CREATE TABLE BOOKS
(
	ISBN		integer check (ISBN >= 1000000000000 and ISBN <= 9999999999999),
	title		varchar(60),
	author		varchar(60),
	pub_name	varchar(70),
	genre		varchar(20),
	num_pages	numeric(3, 0),
	price		numeric(4, 2),
    quantity	integer check (quantity > 0 and quantity < 99),
	sale_percent numeric (2, 0) check (sale_percent < 45),
	PRIMARY KEY (ISBN),
	FOREIGN KEY (pub_name) REFERENCES PUBLISHERS
		on delete cascade
);
"""
USERS_SQL = """
CREATE TABLE USERS
(
	username		varchar(10),
	password		varchar(12),
	billing_info	varchar(40),
	shipping_info	varchar(40),
	PRIMARY KEY (username)
);
"""

ORDERS_SQL = """
CREATE TABLE ORDERS
(
	order_id	integer check(order_id >= 1000000000 and order_id <= 9999999999),
	username	varchar(10),
	ISBN		integer check (ISBN >= 1000000000000 and ISBN <= 9999999999999),
	order_date	date,
    quantity    integer, 
	PRIMARY KEY (order_id, username, ISBN, order_date),
	FOREIGN KEY (ISBN) references BOOKS
	FOREIGN KEY (username) references USERS
);
"""

INSERT_PUBLISHERS_SQL = """
insert into publishers(pub_name, address, email, account_num, phone_num)
values(?, ?, ?, ?, ?)
"""
INSERT_BOOKS_SQL = """
insert into books(ISBN, title, author, pub_name, genre, num_pages, price, quantity, sale_percent)
values(?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
INSERT_USERS_SQL = """
insert into users(username, password, billing_info, shipping_info)
values(?, ?, ?, ?)
"""
INSERT_ORDERS_SQL = """
insert into orders(order_id, username, ISBN, order_date, quantity)
values(?, ?, ?, ?, ?)
"""


def add_publisher(q, pub_name, address, email, account_num, phone_num):
    """
    add_publisher prepares a query to add a new publisher to the database.

    :param q: the current query being prepared
    :param pub_name: the name of the publisher
    :param address: the address of the publisher
    :param email: the email of the publisher
    :param account_num: the account number of the publisher
    :param phone_num: the phone number of the publisher
    :return: {
                error = True/False
                data = Error message/Success message 
             }
    """
    
    q.addBindValue(pub_name)
    q.addBindValue(address)
    q.addBindValue(email)
    q.addBindValue(account_num)
    q.addBindValue(phone_num)
    q.exec()
    if (q.lastError().isValid()):
        print("Error while inserting: ", pub_name)
        print(q.lastError())
        return dict(error=True, data="Error while inserting {publisher}. Details: {details}".format(publisher=pub_name, details=q.lastError().text()))
    return dict(error=False, data="{pub} has been added successfully".format(pub=pub_name))


def add_book(q, isbn, title, author, pub_name, genre, num_pages, price, quantity, sale_percent):
    """
    add_book prepares a query to add a new book to the database.

    :param q: the current query being prepared
    :param isbn: the isbn of the book
    :param title: the title of the book
    :param author: the author of the book
    :param pub_name: the publisher name of the book
    :param genre: the genre of the book
    :param num_pages: the number of pages of the book
    :param price: the price of the book
    :param quantity: the quantity of the book
    :param sale_percent: the percent of sale that will go to publisher when this book is sold
    :return: {
                error = True/False
                data = Error message/Success message 
             }
    """
    
    q.addBindValue(isbn)
    q.addBindValue(title)
    q.addBindValue(author)
    q.addBindValue(pub_name)
    q.addBindValue(genre)
    q.addBindValue(num_pages)
    q.addBindValue(price)
    q.addBindValue(quantity)
    q.addBindValue(sale_percent)
    q.exec()
    if (q.lastError().isValid()):
        print("Error while inserting: ", title)
        print(q.lastError())
        return dict(error=True, data="Error while inserting {book}. Details: {details}".format(book=title, details=q.lastError().text()))
    return dict(error=False, data="{title} has been added successfully".format(title=title))
  
  
def add_user(q, username, password, billing_info, shipping_info):
    """
    add_user prepares a query to add a new user to the database.

    :param q: the current query being prepared
    :param username: the username of the user
    :param password: the password of the user
    :param billing_info: the billing information of the user
    :param shipping_info: the shipping information of the user
    :return: {
                error = True/False
                data = Error message/Success message 
             }
    """
    
    q.addBindValue(username)
    q.addBindValue(password)
    q.addBindValue(billing_info)
    q.addBindValue(shipping_info)
    q.exec()
    if (q.lastError().isValid()):
        print("Error while inserting: ", username)
        print(q.lastError())
        return dict(error=True, data="Error while inserting {uname}. Details: {details}".format(uname=username, details=q.lastError().text()))
    return dict(error=False, data="{uname} has been added successfully".format(uname=username))


def add_order(q, order_id, username, ISBN, order_date, quantity):
    """
    add_order prepares a query to add a new order to the database.

    :param q: the current query being prepared
    :param order_id: the order_id associated with this order
    :param username: the username of the user that checked out
    :param ISBN: the ISBN of the this particular book 
    :param order_date: the date of the order
    :param quantity: the number of times this book was sold during this instance of checkout
    :return: None
    """
    
    q.addBindValue(order_id)
    q.addBindValue(username)
    q.addBindValue(ISBN)
    q.addBindValue(order_date)
    q.addBindValue(quantity)
    q.exec()

def check(func, *args):
    """
    check does error checking

    :return: None
    """
    
    if not func(*args):
        raise ValueError(func.__self__.lastError())
        

def init_db():
    """
    init_db initializes the database with dummy data

    :return: None
    """
    
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(":memory:")

    check(db.open)

    q = QSqlQuery()
    q.exec("PRAGMA foreign_keys = ON;")
    check(q.exec, PUBLISHERS_SQL)
    check(q.exec, BOOKS_SQL)
    check(q.exec, USERS_SQL)
    check(q.exec, ORDERS_SQL)

    check(q.prepare, INSERT_PUBLISHERS_SQL)
    add_publisher(q, 'Knopf', '1745 Broadway, New York, NY 10019', 'knopfpublicity@randomhouse.com', 101142396013, 6138904762)
    add_publisher(q, 'Celadon Books', '120 Broadway, New York, NY 10271', 'contact@celadonbooks.com', 101142396011, 6138904381)
    add_publisher(q, 'Broadway Books', '1714 NE Broadway, Portland, OR 97232', 'bookbroads@broadwaybooks.net', 101142396462, 6132304381)
    add_publisher(q, 'Macmillan Australia', 'Level 25, 1 Market Street, SYDNEY NSW 2000', 'pan.reception@macmillan.com.au', 101142775462, 613237998)
    add_publisher(q, 'Crown', '222 Rosewood Drive, Danvers, MA 01923', 'RHAcademic@penguinrandomhouse.com', 104571775462, 6135567998)
    add_publisher(q, 'HarperCollins Publishers', '195 Broadway, New York, NY 10007', 'hello@harpercollins.com', 128571775462, 6131267008)
    add_publisher(q, 'Little Brown Book Group', 'Carmelite House, 50 Victoria Embankment, London, EC4Y 0DZ', 'enquiries@hachette.co.uk', 128571295462, 6131219108)


    check(q.prepare, INSERT_BOOKS_SQL)
    add_book(q, 9781472134950, 'No Quarter Given', 'Neil Broadfoot', 'Little Brown Book Group', 'Mystery-Thriller', 304, 65.99, 10, 10)
    add_book(q, 9780804188975, 'The Grownup', 'Gillian Flynn', 'Crown', 'Thriller', 240, 54.99, 10, 12)
    add_book(q, 9780380731862, 'Shutter Island', 'Dennis Lehane', 'HarperCollins Publishers', 'Thriller', 369, 39.99, 10, 12)
    add_book(q, 9781101904220, 'Dark Matter', 'Blake Crouch', 'Crown', 'Thriller', 342, 29.99, 10, 15)
    add_book(q, 9781250105608, 'The Dry', 'Jane Harper', 'Macmillan Australia', 'Mystery', 336, 49.99, 10, 25)
    add_book(q, 9780307269751, 'The Girl with the Dragon Tattoo', 'Stieg Larsson', 'Knopf', 'Mystery-Thriller', 480, 59.99, 10, 10)
    add_book(q, 9781250301697, 'The Silent Patient', 'Alex Michaelides', 'Celadon Books', 'Fiction', 325, 34.99, 10, 17)
    add_book(q, 9780307588364, 'Gone Girl', 'Gillian Flynn', 'Broadway Books', 'Thriller', 415, 24.99, 10, 30)
    add_book(q, 9781101947807, 'Send For Me', 'Lauren Fox', 'Knopf', 'Historical Fiction', 272, 10.99, 10, 15)
    add_book(q, 9781476746586, 'All The Light We Cannot See', 'Anthony Doerr', 'Broadway Books', 'Historical Fiction', 531, 29.99, 10, 10)


    check(q.prepare, INSERT_USERS_SQL)
    add_user(q, 'rm_9248', 'abc', 'Ottawa, ON, K1V6Z2', 'Ottawa, ON, K1V6Z2')
    add_user(q, 'gordontang', 'deg', 'Toronto, ON, L4T9Y9', 'Toronto, ON, L4T9Y9')
    add_user(q, 'tatakae', 'kill', 'Berlin, Germany, 10115', 'Berlin, Germany, 10115')


    check(q.prepare, INSERT_ORDERS_SQL)
    add_order(q, 1000000001, 'rm_9248', 9780804188975, '2021-11-18', 1)
    add_order(q, 1000000002, 'rm_9248', 9781101947807, '2021-11-18', 2)
    add_order(q, 1000000003, 'gordontang', 9781101947807, '2020-12-18', 4)
    add_order(q, 1000000004, 'gordontang', 9780307269751, '2019-12-18', 4)
    

init_db()
