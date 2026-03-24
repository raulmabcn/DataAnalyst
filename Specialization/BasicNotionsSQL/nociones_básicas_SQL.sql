-- Nociones básicas SQL

   -- Creamos la base de datos
    CREATE DATABASE IF NOT EXISTS transactions;
    USE transactions;

    -- Creamos la tabla company
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
    
-- ---------------------------------------------------------------------------------------------------------------
-- ---------------------------------------------------------------------------------------------------------------
-- Insertamos los datos desde dades_introduir_sprint2.sql
-- ---------------------------------------------------------------------------------------------------------------
-- ---------------------------------------------------------------------------------------------------------------


-- Nivel 1 ------------------------------------------------------------------------------------------------------
-- Ejercicio 2 --------------------------------------------------------

-- Utilizando JOIN realizarás las siguientes consultas ----------------
-- Listado de los países que están generando ventas.

SELECT DISTINCT c.country
FROM company AS c 
INNER JOIN transaction AS t ON t.company_id = c.id;

-- Desde cuántos países se generan las ventas.

SELECT COUNT(DISTINCT c.country)
FROM company AS c 
INNER JOIN transaction AS t ON t.company_id = c.id;

-- Identifica la compañía con la media más grande de ventas.

SELECT c.id, c.company_name, AVG(t.amount) AS avg_sales
FROM company AS c
INNER JOIN transaction AS t ON t.company_id = c.id
GROUP BY c.id, c.company_name
ORDER BY avg(t.amount) DESC
LIMIT 1;

-- Ejercicio 3 --------------------------------------------------------
-- Utilizando solo subconsultas (sin utilizar JOIN) --------------

-- Muestra todas las transacciones realizadas por empresas de Alemania.

SELECT *
FROM transaction
WHERE company_id IN ( 
	SELECT id
    FROM company
    WHERE country = 'Germany'
);

-- Lista las empresas que han realizado transacciones por un amount superior a la media de todas las transacciones.

SELECT company_name
FROM company 
WHERE id IN ( 
	SELECT company_id
	FROM transaction
    WHERE amount > ( SELECT AVG(amount) FROM transaction ) 
);

-- Eliminarán del sistema las empresas que no tienen transacciones registradas, entrega el listado de estas empresas.

SELECT c.id
FROM company c
WHERE NOT EXISTS (
    SELECT 1
    FROM transaction t
    WHERE t.company_id = c.id
);

-- Nivel 2 ------------------------------------------------------------------------------------------------------

-- Ejercicio 1 --------------------------------------------------------
-- Identifica los cinco días que se generó la cantidad más grande de ingresos a la empresa por ventas. 
-- Muestra la fecha de cada transacción junto con el total de las ventas.

-- Los 5 días que más ingresos tienen sin tener en cuenta la empresa.

SELECT DATE(timestamp) AS date_transaction, SUM(amount) AS total_sales
FROM transaction 
GROUP BY DATE(timestamp)
ORDER BY SUM(amount) DESC
LIMIT 5;

-- Los 5 días (como máximo) que más ingresos tienen por empresa.

SELECT *
FROM (
    SELECT company_id, DATE(timestamp) AS date_transaction, SUM(amount) AS total_sales,
           ROW_NUMBER() OVER (
               PARTITION BY company_id
               ORDER BY SUM(amount) DESC
           ) AS rn
    FROM transaction
    GROUP BY company_id, DATE(timestamp)
) t
WHERE rn <= 5
ORDER BY company_id, rn;

-- Ejercicio 2 --------------------------------------------------------
-- ¿Cuál es la media de ventas por país? Presenta los resultados ordenados de mayor a menor medio.

SELECT c.country, AVG(t.amount) AS avg_sales
FROM company AS c
INNER JOIN transaction AS t ON c.id = t.company_id
GROUP BY c.country
ORDER BY AVG(t.amount) DESC;

-- Ejercicio 3 --------------------------------------------------------
-- En tu empresa, se plantea un nuevo proyecto para lanzar algunas campañas publicitarias para hacer competencia a la compañía "Non Institute". 
-- Para lo cual, te piden la lista de todas las transacciones realizadas por empresas que están situadas en el mismo país que esta compañía.

-- (Muestra el listado aplicando JOIN y subconsultas.)

SELECT t.*
FROM company AS c
INNER JOIN transaction AS t ON c.id = t.company_id
WHERE c.country = (
	SELECT country 
    FROM company 
    WHERE company_name = "Non Institute" 
);

-- (Muestra el listado aplicando solo subconsultas.)

SELECT *
FROM transaction
WHERE company_id IN (
	SELECT id
    FROM company
    WHERE country IN (
		SELECT country 
        FROM company
        WHERE company_name = "Non Institute"
	)
);

-- Nivel 3 ------------------------------------------------------------------------------------------------------

-- Ejercicio 1 --------------------------------------------------------
-- Presenta el nombre, teléfono, país, fecha y amount, de aquellas empresas que realizaron transacciones con un valor comprendido entre 350 y 400 euros 
-- y en alguna de estas fechas: 29 de abril del 2015, 20 de julio del 2018 y 13 de marzo del 2024. Ordena los resultados de mayor a menor cantidad.

SELECT c.company_name, c.phone, c.country, DATE(t.timestamp) AS date, t.amount
FROM company AS c
INNER JOIN transaction AS t ON t.company_id = c.id
WHERE DATE(t.timestamp) IN ('2015-04-29','2018-07-20','2024-03-13')
AND t.amount BETWEEN 350 AND 400
ORDER BY t.amount DESC;

-- Ejercicio 2 --------------------------------------------------------
-- Necesitamos optimizar la asignación de los recursos y dependerá de la capacidad operativa que se requiera, 
-- por lo cual te piden la información sobre la cantidad de transacciones que realicen las empresas, 
-- pero el departamento de recursos humanos es exigente y quiere un listado de las empresas donde especifiques 
-- si tienen más de 400 transacciones o menos.

SELECT c.*, t.n_transactions
FROM company AS c
INNER JOIN (
SELECT
	company_id,
	CASE 
		WHEN COUNT(id) >= 400 THEN '400 o més'
        ELSE 'menys de 400'
	END AS n_transactions
FROM transaction
GROUP BY company_id
) AS t ON c.id = t.company_id;



