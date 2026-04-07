USE transactions;

/*
-- BEGIN RESET ---------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS transaction;
DROP TABLE IF EXISTS company;

DROP TABLE IF EXISTS credit_card;
DROP TABLE IF EXISTS data_user;

DROP VIEW IF EXISTS informetecnico;
DROP VIEW IF EXISTS vistamarketing;

CREATE TABLE IF NOT EXISTS company (
	id VARCHAR(15) PRIMARY KEY,
	company_name VARCHAR(255),
	phone VARCHAR(15),
	email VARCHAR(100),
	country VARCHAR(100),
	website VARCHAR(255)
);

-- Creamos la tabla transaction
CREATE TABLE IF NOT EXISTS transaction (
	id VARCHAR(255) PRIMARY KEY,
	credit_card_id VARCHAR(15) REFERENCES credit_card(id),
	company_id VARCHAR(20), 
	user_id INT REFERENCES user(id),
	lat FLOAT,
	longitude FLOAT,
	timestamp TIMESTAMP,
	amount DECIMAL(10, 2),
	declined BOOLEAN,
	FOREIGN KEY (company_id) REFERENCES company(id) 
);


-- -------------------------------------------------------------------------------------
-- Ejecutamos el script dades_introduir_sprint2.sql 
-- -------------------------------------------------------------------------------------
-- END RESET ---------------------------------------------------------------------------------------------
*/

-- Nivel 1

-- Ejercicio 1
-- Tu tarea es diseñar y crear una tabla llamada "credit_card" que almacene detalles cruciales sobre las tarjetas de crédito. 
-- La nueva tabla tiene que ser capaz de identificar de manera única cada tarjeta y establecer una relación adecuada con las otras dos 
-- tablas("transaction" y "company"). Después de crear la tabla será necesario que ingreses la información del documento denominado 
-- "datos_introducir_sprint3_credit". Recuerda mostrar el diagrama y realizar una breve descripción de este.


CREATE TABLE IF NOT EXISTS credit_card (
	id VARCHAR(15) PRIMARY KEY, 
    iban VARCHAR(50) NOT NULL, 
    pan VARCHAR(25) NOT NULL, 
    pin CHAR(4) NOT NULL, 
    cvv CHAR(3) NOT NULL, 
    expiring_date CHAR(8) NOT NULL
);

-- -------------------------------------------------------------------------------------
-- Ejecutamos el script datos_introducir_sprint3_credit 
-- -------------------------------------------------------------------------------------

ALTER TABLE transaction
ADD CONSTRAINT fk_transaction_credit_card
FOREIGN KEY (credit_card_id)
REFERENCES credit_card( id );


-- Ejercicio 2
-- El departamento de Recursos Humanos ha identificado un error en el número de cuenta asociado a la tarjeta de crédito con ID CcU-2938. 
-- La información que tiene que mostrarse para este registro es: TR323456312213576817699999. Recuerda mostrar que el cambio se realizó.

SELECT * FROM credit_card WHERE id = 'CcU-2938';
UPDATE credit_card 
SET iban = 'TR323456312213576817699999' 
WHERE id = 'CcU-2938';
SELECT * FROM credit_card WHERE id = 'CcU-2938';

-- Ejercicio 3
-- En la tabla "transaction" ingresa una nueva transacción con la siguiente información:

INSERT INTO transaction 
( id, credit_card_id, company_id, user_id, lat, longitude, amount, declined )
VALUES( '108B1D1D-5B23-A76C-55EF-C568E49A99DD', 'CcU-9999', 'b-9999', 9999, 829.999, -117.999, 111.11, 0 );

INSERT INTO company (id) VALUES ('b-9999');
INSERT INTO credit_card VALUES ('CcU-9999','for testing','for testing','test','tes','xx/xx/xx');

INSERT INTO transaction 
( id, credit_card_id, company_id, user_id, lat, longitude, amount, declined )
VALUES( '108B1D1D-5B23-A76C-55EF-C568E49A99DD', 'CcU-9999', 'b-9999', 9999, 829.999, -117.999, 111.11, 0 );

-- Ejercicio 4
-- Desde recursos humanos te solicitan eliminar la columna "pan" de la tabla credit_card. Recuerda mostrar el cambio realizado.

ALTER TABLE credit_card
DROP COLUMN pan;

DESCRIBE credit_card;

-- Nivel 2

-- Ejercicio 1
-- Elimina de la mesa transaction el registro con ID 000447FE-B650-4DCF-85DE-C7ED0EE1CAAD de la base de datos.

DELETE FROM transaction WHERE id = '000447FE-B650-4DCF-85DE-C7ED0EE1CAAD';

-- Ejercicio 2
-- La sección de marketing desea tener acceso a información específica para realizar análisis y estrategias efectivas. 
-- Se ha solicitado crear una vista que proporcione detalles clave sobre las compañías y sus transacciones. 
-- Será necesaria que crees una vista llamada VistaMarketing que contenga la siguiente información: 
-- Nombre de la compañía. Teléfono de contacto. País de residencia. Media de compra realizado por cada compañía. 
-- Presenta la vista creada, ordenando los datos de mayor a menor media de compra.


CREATE OR REPLACE VIEW VistaMarketing AS
SELECT c.company_name, c.phone, c.country, t.avg_buy
FROM company AS c
INNER JOIN (
	SELECT company_id, AVG(amount) as avg_buy
	FROM transaction
    WHERE declined = 0
	GROUP BY company_id
) AS t ON c.id = t.company_id
ORDER BY t.avg_buy DESC;


-- Versión alternativa, prefiero la anterior por el uso de los indices y no utilizar el GROUP BY con campos no necesarios.

/* 
SELECT c.company_name, c.phone, c.country, AVG(t.amount) AS avg_buy
FROM company AS c
INNER JOIN transaction AS t ON t.company_id = c.id
WHERE t.declined = 0
GROUP BY c.id, c.company_name, c.phone, c.country
ORDER BY avg_buy DESC;
*/


SELECT * FROM vistamarketing;


-- Ejercicio 3
-- Filtra la vista VistaMarketing para mostrar solo las compañías que tienen su país de residencia "Germany"

SELECT * 
FROM vistamarketing 
WHERE country = 'Germany';


-- Nivel 3

-- Ejercicio 1
-- La setmana vinent tindràs una nova reunió amb els gerents de màrqueting. Un company del teu equip va realitzar modificacions en la base de dades,
-- però no recorda com les va realitzar. 
-- Et demana que l'ajudis a deixar els comandos executats per a obtenir el següent diagrama:

CREATE TABLE IF NOT EXISTS user (
	id CHAR(10) PRIMARY KEY,
	name VARCHAR(100),
	surname VARCHAR(100),
	phone VARCHAR(150),
	email VARCHAR(150),
	birth_date VARCHAR(100),
	country VARCHAR(150),
	city VARCHAR(150),
	postal_code VARCHAR(100),
	address VARCHAR(255)    
);

-- -------------------------------------------------------------------------------------
-- Ejecutamos el script datos_introducir_sprint3_credit 
-- -------------------------------------------------------------------------------------


ALTER TABLE company DROP COLUMN website;
ALTER TABLE credit_card 
	MODIFY COLUMN id VARCHAR(20) NOT NULL,
    MODIFY COLUMN pin VARCHAR(4) NOT NULL,
    MODIFY COLUMN cvv INT NOT NULL,
    MODIFY COLUMN expiring_date VARCHAR(20) NOT NULL,
    ADD COLUMN fecha_actual DATE DEFAULT NULL;
    
ALTER TABLE transaction 
	MODIFY COLUMN credit_card_id VARCHAR(20) NOT NULL;

RENAME TABLE user TO data_user;
ALTER TABLE data_user
	DROP PRIMARY KEY, 	
	MODIFY COLUMN id INT PRIMARY KEY,
    RENAME COLUMN email TO personal_email;
   
ALTER TABLE transaction
ADD CONSTRAINT fk_transaction_data_user
FOREIGN KEY (user_id)
REFERENCES data_user(id);
    
    
-- Ejercicio 2
-- La empresa también os pide crear una vista llamada "InformeTecnico" que contenga la siguiente información:
-- 		ID de la transacción
-- 		Nombre del usuario/aria
-- 		Apellido del usuario/aria
-- 		IBAN de la tarjeta de crédito usada.
-- 		Nombre de la compañía de la transacción realizada.
-- Aseguraos de incluir información relevante de las tablas que conoceréis y utilizáis alias para cambiar de nombre columnas según haga falta.
-- Muestra los resultados de la vista, ordena los resultados de forma descendente en función de la variable ID de transacción.

CREATE OR REPLACE VIEW InformeTecnico AS
SELECT 	
		t.id AS id_transaction, 
		du.name AS user_name, 
        du.surname AS user_surname, 
        cc.iban AS credit_card_iban, 
        c.company_name 
FROM transaction AS t
INNER JOIN company AS c ON c.id = t.company_id
INNER JOIN credit_card AS cc ON cc.id = t.credit_card_id
INNER JOIN data_user AS du ON du.id = t.user_id
WHERE t.declined = 0
ORDER BY t.id DESC;

SELECT * FROM InformeTecnico;


    

    



