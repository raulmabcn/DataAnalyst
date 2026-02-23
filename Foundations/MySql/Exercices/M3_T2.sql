USE hospitales;

-- 1) Mostra totes les dades dels pacients que comencen per "Ad", de la taula "pacientes".
SELECT *
FROM pacientes
WHERE nombre LIKE 'Ad%';

-- 2) De la consulta anterior, mostra les "edad" úniques.
SELECT DISTINCT edad
FROM pacientes
WHERE nombre LIKE 'Ad%';

-- 3) Mostra el "nombre", el camp "ingreso" i el "numero_dias_ingreso" dels pacients que tenen menys de 10 anys de "edad".
SELECT nombre, ingreso, numero_dias_ingreso
FROM pacientes
WHERE edad < 10;

-- 4) Mostra els pacients dels "hospital_id" 3, 25, 78 i 155.
SELECT *
FROM pacientes
WHERE hospital_id IN (3,25,78,155);

-- 5) Mostra totes les dades dels hospitals que tenen entre 100 i 120 "num_camas".
SELECT *
FROM hospitales
WHERE num_camas BETWEEN 100 AND 120;

-- 6) Mostra els noms dels hospitals que estan a Barcelona - Catalunya.
SELECT nombre
FROM hospitales
WHERE provincia = 'Barcelona'
	AND comunidad_autonoma = 'Cataluña';
    
-- 7) Mostra els 3 hospitals amb més "indice_satisfaccion" del grup d'hospitals de Madrid i Andalusia.
SELECT *
FROM hospitales
WHERE comunidad_autonoma IN ('Comunidad de Madrid','Andalucia')
ORDER BY indice_satisfaccion DESC
LIMIT 3;

-- 8) Mostra els hospitals que comencen per lletra "C" i terminen per lletra "a".
SELECT * 
FROM hospitales
WHERE nombre LIKE 'C%a';

-- 9) Mostra les especialitats que són fixes.
SELECT DISTINCT especialidad 
FROM especialidades
WHERE fija = 'S';

