USE transactions;

-- Nivel 1
/*
-- Ejercicio 1
-- Tu tarea es diseñar y crear una tabla llamada "credit_card" que almacene detalles cruciales sobre las tarjetas de crédito. 
-- La nueva mesa tiene que ser capaz de identificar de manera única cada tarjeta y establecer una relación adecuada con las otras dos 
-- tablas("transaction" y "company"). Después de crear la tabla será necesario que ingreses la información del documento denominado 
-- "datos_introducir_sprint3_credit". Recuerda mostrar el diagrama y realizar una breve descripción de este.

DROP TABLE IF EXISTS credit_card;
CREATE TABLE IF NOT EXISTS credit_card (
	id VARCHAR(15) PRIMARY KEY, 
    iban VARCHAR(35) NOT NULL, 
    pan VARCHAR(25) NOT NULL, 
    pin SMALLINT NOT NULL, 
    cvv SMALLINT NOT NULL, 
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

-- Ejercicio 4
-- Desde recursos humanos te solicitan eliminar la columna "pan" de la tabla credit_card. Recuerda mostrar el cambio realizado.

ALTER TABLE credit_card
DROP COLUMN pan;

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
SELECT c.company_name, c.phone, c.country, AVG(t.amount) AS avg_buy
FROM company AS c
INNER JOIN transaction AS t ON t.company_id = c.id
WHERE t.declined = 0
GROUP BY c.id, c.company_name, c.phone, c.country
ORDER BY avg_buy DESC;

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

*/

ALTER TABLE company DROP COLUMN website;
ALTER TABLE credit_card 
	CHANGE COLUMN id id VARCHAR(20),
    CHANGE COLUMN iban iban VARCHAR(50),
    CHANGE COLUMN pin pin VARCHAR(4),
    CHANGE COLUMN cvv cvv INT,
    CHANGE COLUMN expiring_date expiring_date VARCHAR(20),
    ADD COLUMN fecha_actual DATE DEFAULT NULL;
    
ALTER TABLE transaction 
	CHANGE COLUMN credit_card_id credir_card_id VARCHAR(20);

RENAME TABLE user TO data_user;
ALTER TABLE data_user
	CHANGE COLUMN id id INT,
    RENAME COLUMN email TO personal_email;
    

    



