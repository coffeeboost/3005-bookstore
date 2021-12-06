/*
checks if user exists
*/
SELECT username, password FROM USERS WHERE username = ?
/*
search books where genre matches x
*/
SELECT ISBN, title, author, pub_name, genre, num_pages, price FROM books WHERE ?=?
/*
select all orders
*/
SELECT order_id FROM ORDERS
/*
decrease number of books by amount bought
*/
UPDATE BOOKS SET quantity = quantity - ? WHERE ISBN = ?
/*
find book with isbn
*/
SELECT ISBN, title, author, pub_name, genre, num_pages, price, quantity FROM BOOKS WHERE ISBN =?
/*
find publisher of book with isbn
*/
SELECT BOOKS.pub_name, account_num from BOOKS NATURAL JOIN PUBLISHERS WHERE BOOKS.ISBN = ?
/*
get order information from order id
*/
SELECT BOOKS.ISBN, BOOKS.title, ORDERS.order_id, ORDERS.quantity FROM ORDERS JOIN BOOKS WHERE ORDERS.order_id = ? AND BOOKS.ISBN=ORDERS.ISBN
/*
delete publisher with name
*/
DELETE FROM PUBLISHER WHERE pub_name=?
/*
delete book with isbn
*/
DELETE FROM BOOKS WHERE ISBN = ?
/*
generate genre report
*/
SELECT DISTINCT genre, order_date FROM BOOKS JOIN ORDERS ON (ORDERS.ISBN) WHERE BOOKS.ISBN = ORDERS.ISBN
/*
generate genre report
*/
SELECT genre, price, ORDERS.quantity FROM BOOKS JOIN ORDERS on (ORDERS.ISBN) WHERE BOOKS.ISBN = ORDERS.ISBN
/*
generate author report
*/
SELECT DISTINCT author, order_date FROM BOOKS JOIN ORDERS ON (ORDERS.ISBN) WHERE BOOKS.ISBN = ORDERS.ISBN
/*
generate author report
*/
SELECT author, price, ORDERS.quantity FROM BOOKS JOIN ORDERS on (ORDERS.ISBN) WHERE BOOKS.ISBN = ORDERS.ISBN
/*
similar book query, match book based on genre
*/
SELECT ISBN, title, author, pub_name, genre, num_pages, price FROM BOOKS WHERE genre = ?
/*
generate publisher report
*/
SELECT DISTINCT pub_name, order_date FROM BOOKS JOIN ORDERS ON (ORDERS.ISBN) WHERE BOOKS.ISBN = ORDERS.ISBN
/*
generate publisher report
*/
SELECT pub_name, price, ORDERS.quantity FROM BOOKS JOIN ORDERS on (ORDERS.ISBN) WHERE BOOKS.ISBN = ORDERS.ISBN
/*
used in checkout, help calculate transfer amount
*/
SELECT price, sale_percent FROM BOOKS WHERE ISBN = ?
/*
used in check threshold
*/
SELECT quantity, order_date FROM ORDERS WHERE ISBN = ?
