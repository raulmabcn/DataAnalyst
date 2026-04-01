-- RESET --------------------------------
-- DROP DATABASE IF EXISTS sprint4;
-- --------------------------------------

CREATE DATABASE sprint4;
USE sprint4;

-- BEGIN Creation of tables and relations between tables:

CREATE TABLE IF NOT EXISTS company (
	id				VARCHAR(15),
	name			VARCHAR(255),
	phone			VARCHAR(15),
	email			VARCHAR(100),
	country			VARCHAR(100),
	website			VARCHAR(255),
	PRIMARY KEY		(id)
);

CREATE TABLE IF NOT EXISTS credit_card (
	id				VARCHAR(20), 
	user_id			INT,
	iban			VARCHAR(50), 
	pan				VARCHAR(25), 
	pin				VARCHAR(10), 
	cvv				VARCHAR(10), 
	track1			VARCHAR(80),
	track2			VARCHAR(40),
	expiring_date	CHAR(8),
	PRIMARY KEY		(id)
);

CREATE TABLE IF NOT EXISTS user (
	id 				INT,
	name			VARCHAR(100),
	surname			VARCHAR(100),
	phone			VARCHAR(150),
	email			VARCHAR(150),
	birth_date		VARCHAR(100),
	country			VARCHAR(150),
	city			VARCHAR(150),
	postal_code		VARCHAR(100),
	address			VARCHAR(255),
	region			VARCHAR(20),
	PRIMARY KEY		(id)
);

CREATE TABLE IF NOT EXISTS transaction (
	id				VARCHAR(255),
	credit_card_id	VARCHAR(20),
	company_id		VARCHAR(15),
	user_id			INT,
	amount			DECIMAL(10, 2),
	product_ids		VARCHAR(100),
	declined		BOOLEAN,
	timestamp		TIMESTAMP,
	lat				FLOAT,
	longitude		FLOAT,
	PRIMARY KEY		(id),
	FOREIGN KEY		(credit_card_id)	REFERENCES credit_card(id),
	FOREIGN KEY		(company_id)		REFERENCES company(id),
	FOREIGN KEY		(user_id)			REFERENCES user(id)
);

-- END Creation of tables and relation between tables.

-- BEGIN Load data:
-- Company data from companies.csv
-- Csv fields:		company_id,	company_name,	phone,	email,	country,	website
-- Table fields:	id, 		name, 			phone, 	email,	country,	website

LOAD DATA INFILE 'D:\\DataAnalyst\\Specialization\\DatabaseCreation\\Data\\companies.csv' 
INTO TABLE company
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Credit card data from credit_cards.csv
-- Csv fields:		id, user_id, iban, pan,	pin, cvv, track1, track2, expiring_date
-- Table fields:	id, user_id, iban, pan,	pin, cvv, track1, track2, espiring_date

LOAD DATA INFILE 'D:\\DataAnalyst\\Specialization\\DatabaseCreation\\Data\\credit_cards.csv' 
INTO TABLE credit_card
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- User data from american_users.csv and european_users.csv
-- Csv fields:		id, name, surname, phone, email, birth_date, country, city, postal_code, address
-- Table fields:	id, name, surname, phone, email, birth_date, country, city, postal_code, address, region

LOAD DATA INFILE 'D:\\DataAnalyst\\Specialization\\DatabaseCreation\\Data\\american_users.csv' 
INTO TABLE user
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
( id, name, surname, phone, email, birth_date, country, city, postal_code, address )
SET region = "NORTH_AMERICA";

LOAD DATA INFILE 'D:\\DataAnalyst\\Specialization\\DatabaseCreation\\Data\\european_users.csv' 
INTO TABLE user
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
( id, name, surname, phone, email, birth_date, country, city, postal_code, address )
SET region = "EUROPE";


-- Transaction data from transactions.csv
-- Csv fields:		id,	card_id,		business_id,	timestamp, amount, declined, product_ids, user_id, lat, longitude
-- Table fields:	id,	credit_card_id, company_id, 	timestamp, amount, declined, product_ids, user_id, lat, longitude

LOAD DATA INFILE 'D:\\DataAnalyst\\Specialization\\DatabaseCreation\\Data\\transactions.csv' 
INTO TABLE transaction
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
( id, credit_card_id, company_id, timestamp, amount, declined, product_ids, user_id, lat, longitude );

-- END Load data.

-- Nivel 1 -----------------------------------------------------------
-- Ejercicio 1
-- Realiza una subconsulta que muestre todos los usuarios con más de 80 transacciones utilizando como mínimo 2 tablas:

SELECT id, name, surname
FROM user
WHERE id IN (
	SELECT user_id
	FROM transaction
	WHERE declined = 0
	GROUP BY user_id
	HAVING COUNT(1) > 80
);

-- Ejercicio 2
-- Muestra la media de cantidad por IBAN de las tarjetas de crédito en la compañía Donec Ltd, utiliza al menos 2 tablas. 

SELECT cc.iban, ROUND(AVG(t.amount),2) AS avg_amount
FROM transaction t
INNER JOIN company c ON t.company_id = c.id
INNER JOIN credit_card cc ON t.credit_card_id = cc.id
WHERE c.name = 'Donec Ltd'
GROUP BY cc.iban;


-- Nivel 2 -----------------------------------------------------------
-- Crea una nueva tabla que refleje el estado de las tarjetas de crédito basado en si las tres ultimas transacciones han estado
-- declinadas, entonces es inactivo, si al menos una no es rechazada entonces es actiu. 


CREATE TABLE credit_card_status 
( 
	id				VARCHAR(20),
	status			VARCHAR(8) NOT NULL,
	PRIMARY KEY		(id),
	FOREIGN KEY		(id)	REFERENCES credit_card(id)
);

INSERT INTO credit_card_status (id, status)
	SELECT credit_card_id AS id,  
	CASE
		WHEN SUM(declined) = 3 THEN 'inactive'
		ELSE 'active'
	END AS status
	FROM (
		SELECT credit_card_id, declined, timestamp,
			   ROW_NUMBER() OVER (
				   PARTITION BY credit_card_id
				   ORDER BY timestamp DESC
			   ) AS rn
		FROM transaction
	) t
	WHERE rn <= 3
	GROUP BY credit_card_id;


-- Ejercicio 1
-- Cuantas tarjetas estan activas? 

SELECT COUNT(1) AS n_active_credit_card
FROM credit_card_status
WHERE status = 'active';


-- Nivel 3 -----------------------------------------------------------
-- Crea una tabla con la cual podamos unir los datos del nuevo fichero products.csv con la base de datos creada,
-- teniendo en cuenta que desde transaction tienes product_ids.

CREATE TABLE product (
	id				INT,
	name			VARCHAR(100),
	price			DECIMAL(10,2),
	color			VARCHAR(10),
	weight			DECIMAL(5,1),
	warehouse_id	VARCHAR(10),
	PRIMARY KEY		(id)
);

-- Product data from products_nivel3.csv
-- Csv fields:		id,	product_name, price, colour, weight, warehouse_id
-- Table fields:	id,	name,		  price, colour, weight, warehouse_id

LOAD DATA INFILE 'D:\\DataAnalyst\\Specialization\\DatabaseCreation\\Data\\products_nivel3.csv' 
INTO TABLE product
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
( id, name, @val1, color, weight, warehouse_id )
SET price = SUBSTRING( @val1, 2); -- Remove the prefix $ from the column values. 


CREATE TABLE transaction_product (
	id					INT AUTO_INCREMENT,
	transaction_id		VARCHAR(255),
	product_id			INT,
	PRIMARY KEY			(id),
	FOREIGN KEY			(transaction_id)	REFERENCES transaction(id),
	FOREIGN KEY			(product_id)		REFERENCES product(id)
);

INSERT INTO transaction_product (transaction_id, product_id) 
	SELECT id AS transaction_id, tp.product_id AS product_id
	FROM transaction AS t
	JOIN JSON_TABLE(
		CONCAT('["', REPLACE(t.product_ids, ',', '","'), '"]'),
		'$[*]' COLUMNS (product_id INT PATH '$')
	) tp;

-- Ejercicio 1
-- Necesitamos conocer el número de veces que se ha vendido cada producto. 

SELECT tp.product_id, COUNT(1) AS n_sales
FROM transaction AS t
INNER JOIN transaction_product AS tp ON tp.transaction_id = t.id
WHERE t.declined = 0
GROUP BY tp.product_id;
