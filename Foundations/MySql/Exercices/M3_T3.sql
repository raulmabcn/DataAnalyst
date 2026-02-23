USE hospitales;

-- 1) Mostra la quantitat de pacients que hi ha a la taula "pacientes".
SELECT COUNT(*) as n_pacientes
FROM pacientes;

-- 2) Mostra la quantitat de pacients que té cada "hospital_id" de la taula "pacientes".
SELECT hospital_id, COUNT(*) as n_pacientes
FROM pacientes
GROUP BY hospital_id;

-- 3) Mostra el "numero_dias_ingreso" màxim de cada "hospital_id" de la taula "pacientes".
SELECT hospital_id, MAX(numero_dias_ingreso) as max_n_dias_ingreso
FROM pacientes
GROUP BY hospital_id;

-- 4) Mostra el "indice_satisfaccion" mig de cada comunitat autònoma i província de la taula "hospitals".
SELECT comunidad_autonoma, provincia, AVG(indice_satisfaccion) as media_satisfaccion
FROM hospitales
group by comunidad_autonoma, provincia;

-- 5) Mostra el "num_camas" total de cada comunitat autònoma.
SELECT comunidad_autonoma, SUM(num_camas) as total_n_camas
FROM hospitales
GROUP BY comunidad_autonoma;

-- 6) Mostra el "porcentaje_ocupacion" més petit de cada província de cada comunitat autònoma.
SELECT provincia, comunidad_autonoma, MIN(porcentaje_ocupacion)  as min_porcentaje_ocupacion
FROM hospitales
GROUP BY provincia, comunidad_autonoma;


-- 7) Mostra quantes províncies i localitats té cada comunitat autònoma.
SELECT comunidad_autonoma, COUNT(DISTINCT provincia) as n_provincias, COUNT(DISTINCT localidad) as n_localidades
FROM hospitales
GROUP BY comunidad_autonoma;


-- 8) Mostra les comunitats autònomes que tenen menys de 5 hospitals.
SELECT comunidad_autonoma
FROM hospitales
GROUP BY comunidad_autonoma
HAVING COUNT(hospital_id) < 5;


/* 9) Mostra la quantitat d'hospitals per "especialidad" i per "fija". 
És a dir, quants hospitals tenen una especialitat en funció de si és fixa o no.*/
SELECT especialidad, fija, count(hospital_id) as n_hospitales
FROM especialidades
GROUP BY especialidad, fija
ORDER BY especialidad;






