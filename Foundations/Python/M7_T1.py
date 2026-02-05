""" Crea 4 variables: 
a una assigna-li el teu color preferit, 
a una altra el teu esport preferit, 
a una altra el teu lloc de naixement i 
a una altra el valor true si tens mascotes o false si no en tens. """

favorite_color = 'Blue'
favorite_sport = 'Skate'
birth_place = 'Barcelona'
pet_owner = False

""" Imprimeix aquestes 4 variables juntament amb la frase: 
"El meu color preferit és: X, el meu esport preferit és: Y, vaig néixer a: Z. Tinc mascotes? W", 
on X, Y, Z i W són els valors de les variables que has creat abans. """

print( "El meu color preferit és: "+ favorite_color +", el meu esport preferit és: "+ favorite_sport +", vaig néixer a: "+birth_place+". Tinc mascotes? " + str(pet_owner) )

""" Demana 3 dades més mitjançant 3 prompts i 
pinta una frase amb els 3 valors que has demanat 
(pots inventar la temàtica de les dades que demanis)  """

horoscope =  input("Quin és el teu horòscop?")
favorite_film = input("Quina és la teva pel·lícula favorita?")
favorite_food = input("Quin és el teu menjar favorit?")

print("El teu horòscop és: " + horoscope + ", la teva pel·lícula favorita és: " + favorite_film + "  i el teu menjar favorit és: " + favorite_food + ".")
