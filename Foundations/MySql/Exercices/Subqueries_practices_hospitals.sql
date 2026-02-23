USE hospitales;

-- 1 . Mostra el nom del hospital amb més pressupost de cada comunitat autònoma.

SELECT h.nombre, h.comunidad_autonoma, h.presupuesto_anual_millones
FROM hospitales AS h
WHERE h.presupuesto_anual_millones = ( 
 SELECT MAX(hs.presupuesto_anual_millones) 
 FROM hospitales AS hs 
 WHERE hs.comunidad_autonoma = h.comunidad_autonoma
);

-- 2. Mostra el nom de l'hospital i el nom del pacient que te menys edat de cada hospital.

SELECT h.hospital_id, h.nombre, p.nombre, p.edad
FROM hospitales AS h
INNER JOIN pacientes AS p ON h.hospital_id = p.hospital_id
AND p.edad = ( 
	SELECT MIN(ps.edad) 
	FROM pacientes AS ps
	WHERE ps.hospital_id = p.hospital_id 
)
ORDER BY h.nombre;

SELECT h.hospital_id, h.nombre, p.nombre, p.edad
FROM hospitales h
JOIN (
    SELECT hospital_id, MIN(edad) AS min_edad
    FROM pacientes
    GROUP BY hospital_id
) t ON t.hospital_id = h.hospital_id
JOIN pacientes p
  ON p.hospital_id = t.hospital_id
 AND p.edad = t.min_edad
ORDER BY h.nombre;

-- 3. Mostra els hospitals que estàn per sobre de la mitja de "indice_satisfaccion" de cada comunidad autònoma.

SELECT h.nombre, h.comunidad_autonoma, h.indice_satisfaccion
FROM hospitales AS h
INNER JOIN (
	SELECT hs.comunidad_autonoma, AVG(hs.indice_satisfaccion) AS avg_satis_comunidad
	FROM hospitales AS hs
	GROUP BY hs.comunidad_autonoma
) AS ca ON h.comunidad_autonoma = ca.comunidad_autonoma  AND h.indice_satisfaccion > ca.avg_satis_comunidad;

