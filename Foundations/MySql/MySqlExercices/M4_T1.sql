USE biblioteca;

    -- 1.Mostra el nom del llibre i el nom de l'autor dels llibres que són d'abans del 1927.
  
    SELECT l.titulo, a.nombre
    FROM libros AS l 
    LEFT JOIN autores AS a
    ON l.autor_id = a.autor_id
    WHERE l.año_publicacion < 1927
    ORDER BY l.autor_id;
    
    -- 2.Sobre la pregunta anterior, quin és l'autor amb més llibres publicats abans de 1927?
    
    SELECT a.nombre
    FROM autores AS a 
    INNER JOIN libros AS l
    ON a.autor_id = l.autor_id
    WHERE l.año_publicacion < 1927
    GROUP BY a.autor_id, a.nombre
    ORDER BY COUNT(l.libro_id) DESC
    LIMIT 1;
    
    -- 3.Mostra el nom dels llibres i la quantitat de vegades que han estat retornats amb retard. També s'ha de mostrar la mitjana dels dies de retard.
    
	SELECT l.titulo, 
    COUNT( IF( p.dias_retraso = 0, NULL, p.dias_retraso ) ) AS dias_retraso, 
	IFNULL( AVG( IF( p.dias_retraso = 0, NULL, p.dias_retraso ) ), 0) AS media_dias_retraso
    FROM libros AS l
    INNER JOIN prestamos AS p
    ON l.libro_id = p.libro_id 
    GROUP BY l.libro_id, l.titulo;   
        
    
    -- 4.Mostra la quantitat d'usuaris que no han realitzat cap préstec.
    
	SELECT u.usuario_id
	FROM USUARIOS AS u
	WHERE NOT EXISTS(
		SELECT p.usuario_id 
		FROM prestamos AS p 
		WHERE p.usuario_id = u.usuario_id
	);
    
    SELECT COUNT(*)
    FROM usuarios AS u
    LEFT JOIN prestamos AS p ON u.usuario_id = p.usuario_id
    WHERE p.usuario_id is NULL;
    
    -- 5.Mostra el nom dels 3 usuaris que han fet més préstecs.
    
    SELECT u.nombre, COUNT(p.prestamo_id) AS n_prestamos
    FROM prestamos AS p
    INNER JOIN usuarios AS u
    ON p.usuario_id = u.usuario_id
    GROUP BY u.usuario_id, u.nombre 
    ORDER BY n_prestamos DESC
    LIMIT 3;
    
    -- 6.Mostra el nom i l'ID dels usuaris estrangers i que han hagut de pagar una multa per retard en la devolució del préstec superior a 10 euros.
    
    SELECT DISTINCT u.usuario_id, u.nombre
    FROM usuarios AS u
    INNER JOIN prestamos AS p ON p.usuario_id = u.usuario_id
    INNER JOIN multas AS m ON m.prestamo_id = p.prestamo_id
    WHERE u.nacionalidad = 'extranjera' AND m.importe > 10 AND m.pagada = 1;
    
    -- 7.Mostra l'autor nascut després de 1980 que ha generat més préstecs en usuaris espanyols. A més, només s'han de comptabilitzar els préstecs finalitzats (ok o amb retard).
    
    SELECT a.nombre
    FROM autores AS a
    INNER JOIN libros AS l ON a.autor_id = l.autor_id  
    INNER JOIN prestamos AS p ON p.libro_id = l.libro_id  
    INNER JOIN usuarios AS u ON u.usuario_id = p.usuario_id 
    WHERE a.año_nacimiento > 1980
    AND p.estado_prestamo IN ( 'finalizado ok', 'finalizado con retraso' )
    AND u.nacionalidad = 'española'
    GROUP BY a.autor_id, a.nombre
    ORDER BY COUNT(p.prestamo_id) DESC
    LIMIT 1;
    
    -- 8.Quina és la categoria de llibres que més demanen en préstec les persones que tenen targeta de fidelitat?
    
    SELECT c.categoria_id, c.nombre
    FROM categorias AS c
    INNER JOIN libros AS l ON c.categoria_id = l.categoria_id
    INNER JOIN prestamos AS p ON l.libro_id = p.libro_id
    INNER JOIN usuarios AS u ON p.usuario_id = u.usuario_id 
    WHERE u.tarjeta_fidelidad = 'SI'
    GROUP BY c.categoria_id,c.nombre
    ORDER BY COUNT(p.prestamo_id) DESC
    LIMIT 1;
