from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate,
                           QSqlRelationalTableModel)
import createdb
from datetime import date, datetime
import random
import uuid
from createdb import check
import matplotlib.pyplot as plt
import numpy as np
import calendar

THRESHOLD_VALUE = 5

# {
#     error: True/False
#     data:
# }

# if retun[error]:
#     QDialog()
# else:

def register(user):
    query = QSqlQuery()
    check(query.prepare, createdb.INSERT_USERS_SQL)
    createdb.add_user(query, user.get('username'), user.get('password'), user.get('billing_info'), user.get('shipping_info'))

'''
user
{
    username: data,
    password: data
}
'''
def login(user):
    count = 0
    username = '\'' + user.get('username') + '\''
    query = QSqlQuery('SELECT username, password FROM USERS WHERE username = {name}'.format(name=username))
    if (query.lastError().isValid()):
        print("Error while logging in")
        print(query.lastError())
        return False
    while(query.next()):
        count += 1
    if (count > 0):
        return True
    return False


def search(term, searchBy):
     term = '\'' + term + '\''
     query = QSqlQuery('SELECT ISBN, title, author, pub_name, genre, num_pages, price FROM books WHERE {searching} = {term}'.format(searching=searchBy, term=term))
     if (query.lastError().isValid()):
        print("Error while searching")
        print(query.lastError())
        return
     searchResults = []
     while (query.next()):
        searchResults.append(dict(ISBN=query.value(0), title=str(query.value(1)), author=str(query.value(2)), pub_name=str(query.value(3)),
                                 genre=str(query.value(4)), num_pages=query.value(5), price=query.value(6)))
     return searchResults

'''
user
{
    username: data,
    password: data
}
CHECKOUT_CART of (book) dictionaries
book
{
    title: data,
    ISBN: data,
    quantity: data
}
order_id: uuid
'''
def checkout(user, cart):
    if not login(user):
        print("Invalid username")
        return

    if (len(cart) == 0):
        print("Nothing present in cart")
        return

    order_id=random.randint(1000000000, 9999999999)
    query = QSqlQuery()
    check(query.prepare, createdb.INSERT_ORDERS_SQL)
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    if len(str(now.year)) == 1:
        year = '0' + year
    if len(str(now.month)) == 1:
        month = '0' + month
    if len(str(now.day)) == 1:
        day = '0' + day
    dateString = year + '-' + month + '-' + day
    for i in range(len(cart)):
        query = QSqlQuery()
        check(query.prepare, createdb.INSERT_ORDERS_SQL)
        createdb.add_order(query, order_id, user.get('username'), cart[i].get('ISBN'), dateString,
                           cart[i].get('quantity'))
        query = QSqlQuery('UPDATE BOOKS SET quantity = quantity - {q} WHERE ISBN = {isbn}'.format(q=cart[i].get('quantity'),isbn=cart[i].get('ISBN')))
        if (query.lastError().isValid()):
            print("Error while changing quantity of books")
            print(query.lastError().text())
            return
        query = QSqlQuery('SELECT ISBN, title, author, pub_name, genre, num_pages, price, quantity FROM BOOKS WHERE ISBN = {isbn}'.format(isbn=cart[i].get('ISBN')))
        if (query.lastError().isValid()):
            print("Error while checking minimum threshold")
            print(query.lastError())
            return
        while(query.next()):
            book=dict(ISBN=query.value(0), title=str(query.value(1)), author=str(query.value(2)),
                  pub_name=str(query.value(3)), genre=str(query.value(4)), num_pages=query.value(5),
                  price=query.value(6), quantity=query.value(7))
            check_threshold(book)
            query2 = QSqlQuery('SELECT BOOKS.pub_name, account_num from BOOKS NATURAL JOIN PUBLISHERS WHERE BOOKS.ISBN = {isbn}'.format(isbn=cart[i].get('ISBN')))
            while(query2.next()):
                publisher=dict(pub_name=query2.value(0), account_num=query2.value(1))
                transfer_sale(book, publisher)
    print("Your Order Details")
    print("Order ID: ", order_id)
    for i in range(len(cart)):
        print("Book title", cart[i].get('title'))
        print("Book ISBN: ", cart[i].get('ISBN'))
        print("Quantity: ", cart[i].get('quantity'))
        print()


def track_order(order_id):
    query = QSqlQuery('SELECT BOOKS.ISBN, BOOKS.title, ORDERS.order_id, ORDERS.quantity FROM \
                      ORDERS JOIN BOOKS WHERE ORDERS.order_id = {oid} AND BOOKS.ISBN=ORDERS.ISBN'.format(oid=order_id))
    if (query.lastError().isValid()):
        print("Error while tracking: ", order_id)
        print(query.lastError())
        return
    orderDetails = []
    while (query.next()):
        orderDetails.append(dict(ISBN=query.value(0), title=str(query.value(1)), order_id=query.value(2), quantity=query.value(3)))
    return orderDetails


def owner_add_publisher(publisher):
    query = QSqlQuery()
    check(query.prepare, createdb.INSERT_PUBLISHERS_SQL)
    createdb.add_publisher(query, publisher.get('pub_name'), publisher.get('address'), publisher.get('email'),
                           publisher.get('account_num'), publisher.get('phone_num'))


def owner_remove_publisher(publisher):
    pubName = '\'' + publisher.get('pub_name') + '\''
    query = QSqlQuery('DROP FROM PUBLISHER WHERE pub_name = {name}'.format(name = pubName))
    if (query.lastError().isValid()):
        print("Error while removing: ", publisher.get('pub_name'))
        print(query.lastError())


def owner_add_book(book):
    query = QSqlQuery()
    check(query.prepare, createdb.INSERT_BOOKS_SQL)
    createdb.add_book(query, book.get('ISBN'), book.get('title'), book.get('author'), book.get('pub_name'), book.get('genre'), book.get('num_pages'),
                             book.get('price'), book.get('quantity'), book.get('sale_percent'))


def owner_remove_book(book):
    query = QSqlQuery('DROP FROM BOOKS WHERE ISBN = {isbn}'.format(isbn = book.get('ISBN')))
    if (query.lastError().isValid()):
        print("Error while removing: ", book.get('title'))
        print(query.lastError())


def get_report(reportType, time):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if reportType == 'genre':
        prices, genres = display_genre_report(time)
        ax.bar(genres, prices)
        ax.set_ylabel('Price')
        ax.set_xlabel('Genres')
        if time.get('type') == 'M':
            if time.get('start') == time.get('end'):
                ax.set_title('Sales per Genre in {month}'.format(month=calendar.month_name[time.get('start')]))
            else:
                ax.set_title('Sales per Genre from {smonth} to {emonth}'.format(smonth=calendar.month_name[time.get('start')],
                                                                                emonth=calendar.month_name[time.get('end')]))
        elif time.get('type') == 'Y':
            if time.get('start') == time.get('end'):
                ax.set_title('Sales per Genre in {year}'.format(year=time.get('start')))
            else:
                ax.set_title('Sales per Genre from {syear} to {eyear}'.format(syear=time.get('start'),
                                                                              eyear=time.get('end')))
        plt.show()
    elif reportType == 'author':
        prices, authors = display_author_report(time)
        ax.bar(authors, prices)
        ax.set_ylabel('Price')
        ax.set_xlabel('Authors')
        if time.get('type') == 'M':
            if time.get('start') == time.get('end'):
                ax.set_title('Sales per Author in {month}'.format(month=calendar.month_name[time.get('start')]))
            else:
                ax.set_title('Sales per Author from {smonth} to {emonth}'.format(smonth=calendar.month_name[time.get('start')],
                                                                                 emonth=calendar.month_name[time.get('end')]))
        elif time.get('type') == 'Y':
            if time.get('start') == time.get('end'):
                ax.set_title('Sales per Author in {year}'.format(year=time.get('start')))
            else:
                ax.set_title('Sales per Author from {syear} to {eyear}'.format(syear=time.get('start'),
                                                                               eyear=time.get('end')))
        plt.show()
    else:
        prices, publishers = display_pub_report(time)
        ax.bar(publishers, prices)
        ax.set_ylabel('Price')
        ax.set_xlabel('Publishers')
        if time.get('type') == 'M':
            if time.get('start') == time.get('end'):
                ax.set_title('Sales per Publisher in {month}'.format(month=calendar.month_name[time.get('start')]))
            else:
                ax.set_title('Sales per Publisher from {smonth} to {emonth}'.format(smonth=calendar.month_name[time.get('start')],
                                                                                    emonth=calendar.month_name[time.get('end')]))
        elif time.get('type') == 'Y':
            if time.get('start') == time.get('end'):
                ax.set_title('Sales per Publisher in {year}'.format(year=time.get('start')))
            else:
                ax.set_title('Sales per Publisher from {syear} to {eyear}'.format(syear=time.get('start'),
                                                                                  eyear=time.get('end')))
        plt.show()


def display_genre_report(time):
    #add time range - TODO
    genreSoldList = []
    if time.get('type') == 'M':
        startMonth = time.get('start')
        endMonth = time.get('end')
        askedMonths = list(range(startMonth, endMonth+1))
    elif time.get('type') == 'Y':
        startYear = time.get('start')
        endYear = time.get('end')
        askedYears = list(range(startYear, endYear+1))
    query = QSqlQuery('SELECT DISTINCT genre, order_date FROM BOOKS JOIN ORDERS ON (ORDERS.ISBN) \
                       WHERE BOOKS.ISBN = ORDERS.ISBN')
    if (query.lastError().isValid()):
        print("Error while retrieving genres")
        print(query.lastError())
        return
    while query.next():
        if time.get('type') == 'M':
            if int(str(query.value(1))[-5:-3]) in askedMonths:
                genreSoldList.append(str(query.value(0)))
        elif time.get('type') == 'Y':
            if int(str(query.value(1))[:4]) in askedYears:
                genreSoldList.append(str(query.value(0)))

    genreSoldPrice = np.zeros(len(genreSoldList))

    query = QSqlQuery('SELECT genre, price, ORDERS.quantity FROM BOOKS JOIN ORDERS on (ORDERS.ISBN) WHERE BOOKS.ISBN = ORDERS.ISBN')
    if (query.lastError().isValid()):
        print("Error while retrieving genre orders")
        print(query.lastError())
        return
    while (query.next()):
        for i in range(len(genreSoldList)):
            if str(query.value(0)) == genreSoldList[i]:
                genreSoldPrice[i] += query.value(1) * query.value(2)
                break

    return genreSoldPrice, genreSoldList


def display_author_report(time):
    #add time range - TODO
    authorSoldList = []
    if time.get('type') == 'M':
        startMonth = time.get('start')
        endMonth = time.get('end')
        askedMonths = list(range(startMonth, endMonth+1))
    elif time.get('type') == 'Y':
        startYear = time.get('start')
        endYear = time.get('end')
        askedYears = list(range(startYear, endYear+1))
    query = QSqlQuery('SELECT DISTINCT author FROM BOOKS JOIN ORDERS ON (ORDERS.ISBN) WHERE BOOKS.ISBN = ORDERS.ISBN')
    if (query.lastError().isValid()):
        print("Error while retrieving authors")
        print(query.lastError())
        return
    while query.next():
        if time.get('type') == 'M':
            if int(str(query.value(1))[-5:-3]) in askedMonths:
                authorSoldList.append(str(query.value(0)))
        elif time.get('type') == 'Y':
            if int(str(query.value(1))[:4]) in askedYears:
                authorSoldList.append(str(query.value(0)))

    authorSoldPrice = np.zeros(len(authorSoldList))

    query = QSqlQuery('SELECT author, price, ORDERS.quantity FROM BOOKS JOIN ORDERS on (ORDERS.ISBN) WHERE BOOKS.ISBN = ORDERS.ISBN')
    if (query.lastError().isValid()):
        print("Error while retrieving author orders")
        print(query.lastError())
        return
    while (query.next()):
        for i in range(len(authorSoldList)):
            if str(query.value(0)) == authorSoldList[i]:
                authorSoldPrice[i] += query.value(1) * query.value(2)
                break
    return authorSoldPrice, authorSoldList


def view_similar_books(book):
    count = 0
    genreSimilar = '\'' + book.get('genre') + '\''
    query = QSqlQuery('SELECT ISBN, title, author, pub_name, genre, num_pages, price FROM BOOKS WHERE genre = {g}'.format(g=genreSimilar))
    if (query.lastError().isValid()):
        print("Error while retrieving similar books")
        print(query.lastError())
        return
    similarBooks = []

    while (query.next()):
        if  count >= 3:
            break
        if query.value(0) is not None and query.value(0) != book.get('ISBN'):
            similarBooks.append(dict(ISBN=query.value(0), title=str(query.value(1)), author=str(query.value(2)), pub_name=str(query.value(3)),
                                 genre=str(query.value(4)), num_pages=query.value(5), price=query.value(6)))
        count += 1
    return similarBooks


def display_pub_report(time):
    #add time range - TODO
    pubSoldList = []
    if time.get('type') == 'M':
        startMonth = time.get('start')
        endMonth = time.get('end')
        askedMonths = list(range(startMonth, endMonth+1))
    elif time.get('type') == 'Y':
        startYear = time.get('start')
        endYear = time.get('end')
        askedYears = list(range(startYear, endYear+1))
    query = QSqlQuery('SELECT DISTINCT pub_name FROM BOOKS JOIN ORDERS ON (ORDERS.ISBN) WHERE BOOKS.ISBN = ORDERS.ISBN')
    if (query.lastError().isValid()):
        print("Error while retrieving publishers")
        print(query.lastError())
        return
    while query.next():
        if time.get('type') == 'M':
            if int(str(query.value(1))[-5:-3]) in askedMonths:
                pubSoldList.append(str(query.value(0)))
        elif time.get('type') == 'Y':
            if int(str(query.value(1))[:4]) in askedYears:
                pubSoldList.append(str(query.value(0)))

    pubSoldPrice = np.zeros(len(pubSoldList))

    query = QSqlQuery('SELECT pub_name, price, ORDERS.quantity FROM BOOKS JOIN ORDERS on (ORDERS.ISBN) WHERE BOOKS.ISBN = ORDERS.ISBN')
    if (query.lastError().isValid()):
        print("Error while retrieving publisher orders")
        print(query.lastError())
        return
    while (query.next()):
        for i in range(len(pubSoldList)):
            if str(query.value(0)) == pubSoldList[i]:
                pubSoldPrice[i] += query.value(1) * query.value(2)
                break
    return pubSoldPrice, pubSoldList


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
    # print(book)
    query = QSqlQuery('SELECT quantity, order_date FROM ORDERS WHERE ISBN = {isbn}'.format(isbn=book.get('ISBN')))
    saleCount = 0
    if (query.lastError().isValid()):
        print("Error while checking threshold for", book.get('title'))
        print(query.lastError())
        return
    checkMonth = ""
    checkYear = str(datetime.now().year)
    if datetime.now().month == 1:
        checkMonth = str(12)
    else:
        checkMonth == str(datetime.now().month-1)

    if (datetime.now().month== "1"):
      checkYear = str(datetime.now().year - 1)

    while (query.next()):
       if checkMonth == "12" and checkYear != str(query.value(1))[:4]:
           continue

       if ((str(query.value(1))[-5:-3] == checkMonth) or str(query.value(1))[-5:-3] == str(datetime.now().month)):
           if str(query.value(1))[:4] == str(datetime.now().year):
               saleCount += query.value(0)

    if (book.get('quantity') < THRESHOLD_VALUE):
        print ('Email sent to {publisher} to order {sales} {book_name} books'.format(publisher=book.get('pub_name'), sales=saleCount, book_name=book.get('title')))
# def check_threshold(book):
#     query = QSqlQuery('SELECT quantity, order_date FROM ORDERS WHERE ISBN = {isbn}'.format(isbn=book.get('ISBN')))
#     saleCount = 0
#     if (query.lastError().isValid()):
#         print("Error while checking threshold for", book.get('title'))
#         print(query.lastError())
#         return
#     while (query.next() and ((str(query.value(1))[-5:-3] == checkMonth) or str(query.value(1))[-5:-3] == datetime.now().month)):
#     # while (query.next() and str(query.value(1))[-5:-3] == str(datetime.now().month-1)):
#        saleCount += query.value(0)
#     if (book.get('quantity') < THRESHOLD_VALUE):
#         print ('Email sent to {publisher} to order {sales} {book_name} books'.format(publisher=book.get('pub_name'), sales=saleCount, book_name=book.get('title')))

#get_report('genre', dict(type='M', start=1, end=12))
#get_report('genre', dict(type='Y', start=2019, end=2021))
#checkout(dict(username='gordontang'), [dict(title='Send For Me', ISBN=9781101947807, quantity=2),
#                                       dict(title='Shutter Island', ISBN=9780380731862, quantity=5)])
#track_order(9261651560)
#login(dict(username='gordontang'))
#search('Mystery', 'genre')
#view_similar_books(dict(ISBN=9781101947807, genre='Historical Fiction'))
