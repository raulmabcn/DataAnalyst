USE hospitales;

--    » 1. Mostra el nom dels hospitals i los pacients extranjers que hi ha a la localitat de Toledo.

SELECT h.nombre, p.nombre
FROM hospitales AS h
INNER JOIN pacientes AS p ON p.hospital_id = h.hospital_id AND p.nacionalidad = 'Extranjera'
WHERE h.localidad = 'Toledo'
ORDER BY h.nombre;

--    » 2. Mostra el nom dels hospitals i la quantitat d'especialitats que hi ha als hospitals de la consulta anterior.
SELECT h.nombre, COUNT( DISTINCT(e.especialidad) ) AS n_especialidades
FROM hospitales AS h
INNER JOIN pacientes AS p ON p.hospital_id = h.hospital_id AND p.nacionalidad = 'Extranjera'
INNER JOIN especialidades AS e ON e.hospital_id = h.hospital_id 
WHERE h.localidad = 'Toledo'
GROUP BY (h.nombre)
ORDER BY h.nombre;
	
--    » 3. Mostra el nom de l’hospital i les especialitats que té l’hospital amb identificador 105.

SELECT h.nombre, e.especialidad
FROM hospitales AS h
INNER JOIN especialidades AS e ON h.hospital_id = e.hospital_id AND h.hospital_id = 105;

--    » 4. Digues quants hospitals tenen dades a la taula "hospitales", però no tenen dades a la taula de "pacientes".
/*
SELECT COUNT(*)
FROM hospitales AS h
WHERE NOT EXISTS ( SELECT 1 FROM pacientes AS p WHERE p.hospital_id = h.hospital_id );
*/

SELECT COUNT(*)
FROM hospitales h
LEFT JOIN pacientes p ON p.hospital_id = h.hospital_id
WHERE p.hospital_id IS NULL;

--    » 5. Mostra el nom de l'hospital que té menys especialitats fixes.

WITH cte AS (
	SELECT h.hospital_id, h.nombre, COUNT(especialidad) AS n_esp_fija
	FROM hospitales AS h
	LEFT JOIN especialidades AS e ON h.hospital_id = e.hospital_id AND e.fija = 'S'
	GROUP BY h.hospital_id, h.nombre
)
SELECT nombre
FROM cte
WHERE n_esp_fija = (SELECT MIN(n_esp_fija) FROM cte);

--    » 6. Mostra el nom i el nombre total de visites de l'hospital amb identificador 45.

SELECT nombre, (
	SELECT SUM(numero_visitas)
	FROM pacientes AS p
	WHERE hospital_id = 45
) AS n_visitas
FROM hospitales
WHERE hospital_id = 45;

SELECT h.hospital_id , h.nombre, sum(p.numero_visitas) 
FROM hospitales h 
INNER JOIN pacientes p on h.hospital_id = p.hospital_id
WHERE h.hospital_id=45
GROUP BY 1,2;

--    » 7. Mostra el nom de l'hospital, el nom dels seus pacients estrangers i el nombre de visites, així com les especialitats que NO són fixes. Totes aquestes dades de l'hospital amb identificador 45.

SELECT h.nombre, p.nombre, p.numero_visitas, e.especialidad
FROM hospitales AS h
INNER JOIN pacientes AS p ON h.hospital_id = p.hospital_id AND p.nacionalidad = 'Extranjera'
INNER JOIN especialidades AS e ON e.hospital_id = h.hospital_id AND e.fija = 'N'
WHERE h.hospital_id = 45;


--   » 8. Suma el "numero_visitas" de la consulta anterior (a mà) i compara-la amb el "numero_visitas" de la consulta núm. 6. Són iguals? Què està passant?
