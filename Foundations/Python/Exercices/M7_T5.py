""" Crea una funció que rebi un text i retorni el text en majúscules. 
Demana un text a l’usuari i mostra el resultat amb la funció.  """


def upper_case( text ):
    return text.upper()

user_text = input("Escriu un text: " )
print( upper_case( user_text ) )