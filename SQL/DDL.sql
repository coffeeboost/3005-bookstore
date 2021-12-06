/*
create publisher table
*/
CREATE TABLE PUBLISHERS
(
	pub_name	varchar(70),
	address		varchar(200),
	email		varchar(50),
	account_num	numeric(12, 0) UNIQUE,
	phone_num	numeric(10, 0) UNIQUE,
	PRIMARY KEY (pub_name)
);

/*
create books table
*/
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

/*
create users table
*/
CREATE TABLE USERS
(
	username		varchar(10),
	password		varchar(12),
	billing_info	varchar(40),
	shipping_info	varchar(40),
	PRIMARY KEY (username)
);

/*
create orders table
*/
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
