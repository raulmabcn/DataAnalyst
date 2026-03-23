-- Nivell 1 ------------------------------------------------------------------------------------------------------
-- Exercici 2 --------------------------------------------------------
-- Utilitzant JOIN realitzaràs les següents consultes ----------------

-- Llistat dels països que estan fent compres.

SELECT DISTINCT c.country
FROM company AS c 
INNER JOIN transaction AS t ON t.company_id = c.id;

-- Des de quants països es realitzen les compres.

SELECT COUNT(DISTINCT c.country)
FROM company AS c 
INNER JOIN transaction AS t ON t.company_id = c.id;

-- Identifica la companyia amb la mitjana més gran de vendes.

SELECT c.id, c.company_name, AVG(t.amount) AS avg_sales
FROM company AS c
INNER JOIN transaction AS t ON t.company_id = c.id
GROUP BY c.id, c.company_name
ORDER BY avg(t.amount) DESC
LIMIT 1;

-- Exercici 3 --------------------------------------------------------
-- (Utilitzant només subconsultes (sense utilitzar JOIN)--------------

-- Mostra totes les transaccions realitzades per empreses d'Alemanya.

SELECT *
FROM transaction
WHERE company_id IN ( 
	SELECT id
    FROM company
    WHERE country = 'Germany'
);

-- Llista les empreses que han realitzat transaccions per un amount superior a la mitjana de totes les transaccions.

SELECT company_name
FROM company 
WHERE id IN ( 
	SELECT company_id
	FROM transaction
    WHERE amount > ( SELECT AVG(amount) FROM transaction ) 
);

-- Eliminaran del sistema les empreses que no tenen transaccions registrades, entrega el llistat d'aquestes empreses.

SELECT c.id
FROM company c
WHERE NOT EXISTS (
    SELECT 1
    FROM transaction t
    WHERE t.company_id = c.id
);

-- Nivell 2 ------------------------------------------------------------------------------------------------------

-- Exercici 1 --------------------------------------------------------
-- Identifica els cinc dies que es va generar la quantitat més gran d'ingressos a l'empresa per vendes. 
-- Mostra la data de cada transacció juntament amb el total de les vendes.

-- Els 5 dies que mes ingresos tenen sense tenit en compte la empresa.
SELECT DATE(timestamp) AS date_transaction, SUM(amount) AS total_sales
FROM transaction 
GROUP BY DATE(timestamp)
ORDER BY SUM(amount) DESC
LIMIT 5;

-- Dies amb mes ingresos per empresa, limitat a 5 resultats máxim per empresa
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

-- Exercici 2 --------------------------------------------------------
-- Quina és la mitjana de vendes per país? Presenta els resultats ordenats de major a menor mitjà.

SELECT c.country, AVG(t.amount) AS avg_sales
FROM company AS c
INNER JOIN transaction AS t ON c.id = t.company_id
GROUP BY c.country
ORDER BY AVG(t.amount) DESC;

-- Exercici 3 --------------------------------------------------------
-- En la teva empresa, es planteja un nou projecte per a llançar algunes campanyes publicitàries per a fer competència a la companyia "Non Institute". 
-- Per a això, et demanen la llista de totes les transaccions realitzades per empreses que estan situades en el mateix país que aquesta companyia.

-- (Mostra el llistat aplicant JOIN i subconsultes.)

SELECT t.*
FROM company AS c
INNER JOIN transaction AS t ON c.id = t.company_id
WHERE c.country = (
	SELECT country 
    FROM company 
    WHERE company_name = "Non Institute" 
);

-- (Mostra el llistat aplicant solament subconsultes.)

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

-- Nivell 3 ------------------------------------------------------------------------------------------------------

-- Exercici 1 --------------------------------------------------------
-- Presenta el nom, telèfon, país, data i amount, d'aquelles empreses que van realitzar transaccions amb un valor comprès entre 100 i 200 euros 
-- i en alguna d'aquestes dates: 29 d'abril del 2021, 20 de juliol del 2021 i 13 de març del 2022. Ordena els resultats de major a menor quantitat.

SELECT c.company_name, c.phone, c.country, DATE(t.timestamp) AS date, t.amount
FROM company AS c
INNER JOIN transaction AS t ON t.company_id = c.id
WHERE DATE(t.timestamp) IN ('2021-04-29','2021-07-20','2022-03-13')
AND t.amount BETWEEN 100 AND 200
ORDER BY t.amount DESC;

/*
SELECT c.company_name, c.phone, c.country, DATE(t.timestamp) AS date, t.amount
FROM company AS c
INNER JOIN transaction AS t ON t.company_id = c.id
WHERE (( t.timestamp >= '2021-04-29 00:00:00' AND t.timestamp < '2021-04-30 00:00:00' ) 
OR ( t.timestamp >= '2021-07-20 00:00:00' AND t.timestamp < '2021-07-21 00:00:00' )
OR ( t.timestamp >= '2022-03-13 00:00:00' AND t.timestamp < '2022-03-14 00:00:00' ))
AND t.amount BETWEEN 100 AND 200
ORDER BY t.amount DESC;
*/

-- Exercici 2 --------------------------------------------------------
-- Necessitem optimitzar l'assignació dels recursos i dependrà de la capacitat operativa que es requereixi, 
-- per la qual cosa et demanen la informació sobre la quantitat de transaccions que realitzen les empreses, 
-- però el departament de recursos humans és exigent i vol un llistat de les empreses on especifiquis si tenen més de 4 transaccions o menys.


SELECT c.*, t.n_transactions
FROM company AS c
INNER JOIN (
SELECT
	company_id,
	CASE 
		WHEN COUNT(id) >= 4 THEN '4 o més'
        ELSE 'menys de 4'
	END AS n_transactions
FROM transaction
GROUP BY company_id
) AS t ON c.id = t.company_id;

/*
SELECT c.*, t.n_transactions
FROM company AS c
INNER JOIN (
	SELECT company_id, '4 o més' AS n_transactions
	FROM transaction
	GROUP BY company_id
	HAVING COUNT(id) >= 4 
	UNION 
	SELECT company_id, 'menys de 4' AS n_transactions
	FROM transaction
	GROUP BY company_id
	HAVING COUNT(id) < 4 
) AS t ON c.id = t.company_id;
*/




