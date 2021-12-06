/*insert into publisher*/
insert into publishers(pub_name, address, email, account_num, phone_num)

/*insert into books*/

insert into books(ISBN, title, author, pub_name, genre, num_pages, price, quantity, sale_percent)

/*insert into users*/
insert into users(username, password, billing_info, shipping_info)

/*insert into orders*/
insert into orders(order_id, username, ISBN, order_date, quantity)
