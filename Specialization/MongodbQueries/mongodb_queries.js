// Nivel 1

// Ejercicio 1

// Muestra los 2 primeros comentarios que hay en la base de datos.

db.comments.find().sort( {date:1} ).limit(2)

// Cuántos usuarios tenemos registrados?

db.users.countDocuments();


// Cuántos cines hay en el estado de California?

db.theaters.countDocuments( { 'location.address.state': 'CA'} )


// Quien fue el primer usuario/a en registrarse?

db.users.find().sort( {_id:1} ).limit(1)


//Cuántas películas de comedia hay en nuestra base de datos?

db.movies.countDocuments({ genres: 'Comedy' })

// Ejercicio 2

// Muéstrame todos los documentos de las películas producidas en 1932, pero que el género sea drama o estén en francés.

db.movies.find({ 
		year: 1932, 
		$or: [ 
			{ genres: 'Drama' }, 
			{ languages: 'French' } 
		] 
})

// Ejercicio 3

//Muéstrame todos los documentos de películas estadounidenses que tengan entre 5 y 9 premios que fueron producidas entre 2012 y 2014.

db.movies.find({
	countries: 'USA',
	'awards.wins': {$gte:5, $lte:9 },
	year: {$gte:2012, $lte:2014 }
})


// Nivel 2

// Ejercicio 1

// Cuenta cuántos comentarios escribe un usuario/aria que utiliza "GAMEOFTHRON.ES" como dominio de correo electrónico.
// Número de comentarios totales de usuarios/as con  "GAMEOFTHRON.ES" como dominio de correo electrónico.

db.comments.countDocuments({ 
	email:{ $regex: /@GAMEOFTHRON\.ES$/, $options: 'i' }
})

// Número de comentarios de cada usuario/a con "GAMEOFTHRON.ES" como dominio de correo electrónico.

db.comments.aggregate(
	{
		$match:{ email:{ $regex: /@GAMEOFTHRON\.ES$/, $options: 'i' }}
	},
	{
		$group:{_id: "$email", count:{$sum:1}}
	}
)



// Ejercicio 2

// Cuántos cines hay en cada código postal situados dentro del estado Washington D. C. (DC)?

db.theaters.aggregate([ 
	{ $match:	{ 'location.address.state': 'DC' } },
	{ $group:	{ _id: '$location.address.zipcode',	total: {$sum: 1} } },
	{ $project: { _id:0, zipcode: '$_id', total: 1 } }
])

// Nivel 3

// Ejercicio 1

// Encuentra todas las películas dirigidas por John Landis con una puntuación IMDb (Internet Movie Database) de entre 7,5 y 8.

db.movies.find(
	{ directors: 'John Landis',	'imdb.rating':	{ $gte:7.5, $lte:8 } },
	{ title: 1, 'imdb.rating': 1 }
)


// Ejercicio 2

// Muestra en un mapa la ubicación de todos los teatros de la base de datos.

/*
Comentario: 
	Si se quieren utilizar los campos de longitud y latitud en Power BI, es necesario procesarlos en MongoDB antes de pasarlos a Power BI, 
	ya que Power BI, con el conector ODBC, no sabe tratar los subniveles del JSON y se pierde información. 
	Por ello, he decidido crear una vista con la información de theater_id, longitude y latitude para poder consumirla fácilmente desde Power BI.
*/

db.createView( "theater_geo_data", "theaters", [{ 
	$project: {
	  theater_id:	"$theaterId",
      longitude:	{ $arrayElemAt: ["$location.geo.coordinates", 0] },
      latitude:		{ $arrayElemAt: ["$location.geo.coordinates", 1] }
    }
}]);







