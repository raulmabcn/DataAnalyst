USE biblioteca;

-- 1)Quin és el nom de l'empleat (o dels empleats) i la seva posició, amb el mínim any de contractació?
SELECT nombre, posicion
FROM empleados
WHERE año_contratacion = (
	SELECT MIN( año_contratacion )
	FROM empleados
);

-- 2) Mostra el nom de la categoria i el nom del llibre (o llibres), dels llibres amb l'any de publicació més recent de cada categoria.

SELECT c.nombre, l.titulo, l.año_publicacion
FROM libros AS l
INNER JOIN categorias AS c ON l.categoria_id = c.categoria_id
INNER JOIN ( 
	SELECT categoria_id, MAX( año_publicacion ) AS año_reciente
	FROM libros
	GROUP by categoria_id
) AS ac ON ac.categoria_id = c.categoria_id 
	AND ac.año_reciente = l.año_publicacion
ORDER BY l.categoria_id;

-- 3) Mostra els llibres que tenen més còpies que la mitjana del nombre de còpies dels llibres de la seva categoria.

SELECT l.titulo
FROM libros AS l
INNER JOIN (
	SELECT categoria_id, AVG( cantidad_copias ) AS avg_copias
	FROM libros
	GROUP BY ( categoria_id )
) as avg_cat ON avg_cat.categoria_id = l.categoria_id 
WHERE l.cantidad_copias > avg_cat.avg_copias;

-- 4) Quin és el nom del llibre i del seu autor, del llibre que té un import més gran en multes (comptant la suma de totes les multes de cada llibre)?

-- Versión order + limit:

SELECT l.titulo, a.nombre
FROM autores AS a
INNER JOIN (
	SELECT l.autor_id, l.titulo, SUM( m.importe ) AS total_importe
	FROM libros AS l
	INNER JOIN prestamos AS p ON l.libro_id = p.libro_id
	INNER JOIN multas AS m ON m.prestamo_id = p.prestamo_id
	GROUP BY l.libro_id, l.autor_id, l.titulo
	ORDER BY total_importe DESC
	LIMIT 1
) AS l ON a.autor_id = l.autor_id;

-- Versión having + max:

SELECT l.titulo, a.nombre, SUM(m.importe) as importe
FROM libros AS l
INNER JOIN autores AS a ON l.autor_id = a.autor_id
INNER JOIN prestamos AS p ON l.libro_id = p.libro_id
INNER JOIN multas AS m ON m.prestamo_id = p.prestamo_id
GROUP BY l.libro_id, l.titulo, a.nombre
HAVING SUM( m.importe ) = ( 
	SELECT MAX(lm.importe) as max_importe
	FROM ( 
		SELECT l.libro_id, SUM(m.importe) as importe
		FROM libros AS l
		INNER JOIN prestamos AS p ON l.libro_id = p.libro_id
		INNER JOIN multas AS m ON m.prestamo_id = p.prestamo_id
		GROUP BY l.libro_id
		) as lm
);




