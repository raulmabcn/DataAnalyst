USE hospitales;

--    1.Mostra totes les dades de la taula "pacientes".
SELECT *
FROM pacientes;

--    2.Mostra el "nombre", "comunidad_autonoma", "provincia" i "localidad" de la taula "hospitales".
SELECT nombre, comunidad_autonoma, provincia, localidad
FROM hospitales;

--    3.Mostra els noms dels hospitals i el seu "presupuesto_anual_millones" ordenats pel seu "indice_satisfaccion" de major a menor.
SELECT nombre, presupuesto_anual_millones
FROM hospitales
ORDER BY indice_satisfaccion DESC;

--    4.Mostra el top10 dels hospitals de la consulta anterior.
SELECT nombre, presupuesto_anual_millones
FROM hospitales
ORDER BY indice_satisfaccion DESC
LIMIT 10;

--    5.Mostra quines són les "provincia" úniques que hi ha a la taula "hospitales".
SELECT DISTINCT provincia
FROM hospitales;


--    6.Mostra totes les especialitats mèdiques que hi ha.
SELECT DISTINCT especialidad
FROM especialidades;
