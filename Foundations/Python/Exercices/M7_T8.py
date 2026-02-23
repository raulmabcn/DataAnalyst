""" Crea una funció que:
Demani a l’usuari 3 noms de ciutats, un per un.
Comprovi si cada ciutat conté la lletra 'E' o 'e' i té més de 5 lletres.
Si la ciutat compleix aquestes condicions, afegeix-la a una llista.
Quan hagi acabat, retorna la llista completa de ciutats que compleixen els requisits. """


def check_cities( cities ):
    
    cities_list = []
    
    for city_name in cities:
        if( len( city_name ) > 5 & city_name.lower().count('e') > 0 ):
            cities_list.append(city_name)
    
    return cities_list

cities = []
cities.append( input("Introdueix el nom d'una primera ciutat: ") )
cities.append( input("Introdueix el nom d'una segona ciutat: ") )
cities.append( input("Introdueix el nom d'una tercera ciutat: ") )

print( check_cities( cities ) )

