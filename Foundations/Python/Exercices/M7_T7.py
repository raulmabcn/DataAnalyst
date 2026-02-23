""" Crea una llista amb tres llibres inicials "El Quixot", "Hamlet" i "La metamorfosi".
Afegeix al final de la llista dos llibres més: "1984" i "Ulisses". Torna a imprimir la llista per veure els canvis.
Elimina "Hamlet" de la llista. Imprimeix la llista actualitzada.
Afegeix el llibre "Orgull i prejudici" a la tercera posició de la llista. Torna a imprimir la llista.

Genera un diccionari amb els llibres de la llista resultant i el seu any de publicació:
El Quixot: 1605
La metamorfosi: 1915
1984: 1949
Ulisses: 1922
Orgull i prejudici: 1813
Imprimeix l'any de publicació d'Ulisses.
Afegeix al diccionari els teus dos llibres preferits amb el seu any de publicació.
Imprimeix el diccionari resultant. """


books_list = ["El Quixot", "Hamlet", "La metamorfosi"]

books_list.append( "1984" )
books_list.append( "Ulisses" )
print( books_list )

books_list.remove( "Hamlet" )
print( books_list )

books_list.insert( 2, "Orgull i prejudici" )
print( books_list )


# books_dictionary_list = [ 
#     { "title": "El Quixot", "year": 1605},
#     { "title": "La metamorfosi", "year": 1915},
#     { "title": "1984", "year": 1949},
#     { "title": "Ulisses", "year": 1922},
#     { "title": "Orgull i prejudici:", "year": 1813}
# ]

# print( books_dictionary_list[3]["year"])

# books_dictionary_list.append( {"title" : "Kokoro", "year":2014 } ) 
# books_dictionary_list.append( {"title" : "La tienda de los deseos", "year":2025 } ) 

# print( books_dictionary_list )


books_dictionary = { 
    "El Quixot" : 1605,
    "La metamorfosi" : 1915,
    "1984" : 1949,
    "Ulisses" : 1922,
    "Orgull i prejudici" : 1813
    }

print( books_dictionary["Ulisses"] )

books_dictionary["Kokoro"] = 2014
books_dictionary["La tienda de los deseos"] = 2025

print( books_dictionary )
