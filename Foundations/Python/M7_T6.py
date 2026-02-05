""" Demana dos números a l’usuari i crea una funció que retorni True 
si el primer número és més gran que el segon, i False en cas contrari.  """


def compare_numbers( first, second ):
    return( first > second )

first_number = input( "Introdueix un número: " )
second_number = input( "Introdueix un altre número: " )

print( compare_numbers( first_number,second_number ) )
