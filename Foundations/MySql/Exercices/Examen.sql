/*
	Prova SQL
    Nom alumne: Raúl Martínez 	
    Data: 11/02/2026
*/

USE sakila;

# 1. Mostra quants exemplars de cada pel·lícula tenim a l’inventari. (0.5p)

SELECT f.film_id, f.title, COUNT( f.film_id ) AS n_films -- Muestro el film_id, por si hubiera dos peliculas con el mismo título.
FROM inventory AS i
INNER JOIN film AS f ON i.film_id = f.film_id
GROUP BY f.film_id, f.title;

# 2. Mostra el nom de l’actor/actriu i la quantitat de pel·lícules en les que
# ha participat. Només volem mostrar aquells actors/actrius que han
# participat a 35 pel·lícules o més. (1p)

SELECT a.first_name, a.last_name, fa.n_films
FROM actor AS a
INNER JOIN (
	SELECT actor_id, COUNT( film_id ) AS n_films
	FROM film_actor
	GROUP BY actor_id
	HAVING COUNT( film_id ) > 34
) AS fa ON a.actor_id = fa.actor_id;


# 3. Mostra el nom de les pel·lícules que contenen la paraula “LOVE” al
# seu títol i que són de la categoria “Classics” o “Sci-Fi”. (1,25p)

SELECT f.title
FROM film AS f
INNER JOIN film_category AS fc ON f.film_id = fc.film_id
INNER JOIN category AS c ON fc.category_id = c.category_id
WHERE c.name IN( "Classics", "Sci-Fi" ) 
	AND f.title LIKE "%LOVE%"; 
    
 /* Considero que se quieren los titulos que contienen LOVE si se quisiera que fuera la palabra EXACTA "LOVE" y no LOVER, LOVELY, etc...
  f.title LIKE "%LOVE" se tendría que cambiar por la siguiente expresión (o mejor usar una expresión regular)
 ( f.title LIKE "LOVE %" OR f.title LIKE "% LOVE" OR f.title LIKE "% LOVE %" ); */


# 4. Troba les pel·lícules que d’acció que no existeixen a l’inventari. (1,5p)

SELECT f.title
FROM film AS f
INNER JOIN film_category AS fc ON fc.film_id = f.film_id
INNER JOIN category AS c ON fc.category_id = c.category_id
LEFT JOIN inventory AS i ON f.film_id = i.film_id
WHERE c.name = "Action" 
	AND i.film_id is NULL;
    

#5. Quina botiga té un inventari més gran de pel·lícules de comèdia i esports? (1,5p)

/* Entido que se quiere la tienda con más peliculas (que no títulos diferentes) de comedia + deportes.*/

SELECT i.store_id
FROM inventory AS i
INNER JOIN film_category AS fc ON fc.film_id = i.film_id
INNER JOIN category AS c ON fc.category_id = c.category_id
WHERE c.name IN ( "Comedy", "Sports" )
GROUP BY i.store_id
ORDER BY COUNT(i.film_id) DESC
LIMIT 1;


# 6. Mostra el nom dels actors i actrius que han fet la pel·lícula de Drama més curta. (1,25p)

SELECT a.first_name, a.last_name
FROM actor AS a
INNER JOIN film_actor AS fa ON a.actor_id = fa.actor_id
WHERE fa.film_id = (
		SELECT f.film_id
		FROM film AS f
		INNER JOIN film_category AS fc ON f.film_id = fc.film_id
		INNER JOIN category AS c ON fc.category_id = c.category_id
		WHERE c.name = "Drama"
		ORDER BY f.length ASC
        LIMIT 1);


# 7. Mostra les categories de les pel·lícules que compleixen el següent: 
# la mitja de “rental rate” de la categoria és menor a la mitja de “rental
# rate” general de totes les pel·lícules. Per tot aquest càlcul, no has
# d’incloure les pel·lícules amb un “rental rate” menor a 1. (1,5p)

SELECT c.name AS category_name
FROM category AS c
INNER JOIN (
	SELECT fc.category_id, AVG(rental_rate) AS categ_r_rate
	FROM film AS f
	INNER JOIN film_category AS fc ON f.film_id = fc.film_id
	WHERE rental_rate >= 1
	GROUP BY fc.category_id
	HAVING categ_r_rate < (
		SELECT AVG(rental_rate) AS general_r_rate
		FROM film 
		WHERE rental_rate >= 1
	) ) as cr ON cr.category_id = c.category_id;


# 8. Mostra el nom de la pel·lícula i la quantitat d’actors/actrius de la
# pel·lícula que més (actors i actrius) tingui de cada categoria. Si hi ha
# empat de dos o més pel·lícules de la mateixa categoria en la seva
# quantitat d’actors/actrius, les has de mostrar totes. (1.5p)

SELECT f.title, f_n_actors.n_actors, categ_max_actors.category_id -- Muestro el id de categoria para poder distinguir a que categoria pertenece cada película 
FROM film AS f
INNER JOIN (
	SELECT fc.category_id, fc.film_id, COUNT( fa.actor_id ) as n_actors
	FROM film_actor AS fa
	INNER JOIN film_category AS fc ON fa.film_id = fc.film_id
	GROUP BY fc.category_id, fc.film_id
) AS f_n_actors ON f_n_actors.film_id = f.film_id
INNER JOIN (
	SELECT category_id, MAX( n_actors ) max_n_actors
	FROM (
		SELECT fc.category_id, fc.film_id, COUNT( fa.actor_id ) as n_actors
		FROM film_actor AS fa
		INNER JOIN film_category AS fc ON fa.film_id = fc.film_id
		GROUP BY fc.category_id, fc.film_id
	) aux 
	GROUP BY category_id
) AS categ_max_actors ON categ_max_actors.category_id = f_n_actors.category_id
AND categ_max_actors.max_n_actors = f_n_actors.n_actors;





