"""
1. Crea una funció que, donada una frase o una paraula, 
retorni el nombre de vocals. Un cop definida, sol·licita una paraula o 
frase a l’usuari i imprimeix el nombre de vocals."""


def get_vocals_count(phrase):
    vocals = 'aeiou'
    total_vocals = 0
    if isinstance( phrase, str):
        total_vocals = sum( phrase.lower().count(c) for c in vocals )  

    return total_vocals


""" 
2. Defineix una funció que, donat un número, 
imprimeixi la seva taula de multiplicar. 
(Exemple: 1 × 1 = 1, 1 × 2 = 2, 1 × 3 = 3, ...)."""


def print_multiple_table(number):

    num = int(number)
    for c in range (11):
        print(f"{number} x {c} = {num * c}")

"""
3. Defineix una funció que, donada una frase, retorni el nombre de paraules
 úniques que conté, sense fer servir la funció len(). 
 (Pots utilitzar el mètode split() d’un string.)
"""

def count_unique_words(phrase):
    number_unique_words = 0
    phrase_dictionary = {}
    
    if isinstance( phrase, str ):
        words =  phrase.lower().split()
        for w in words:
            phrase_dictionary[w] = 1

    number_unique_words = sum( phrase_dictionary.values() )
    
    return number_unique_words

"""
4. Defineix una funció que, donada una llista de números, 
imprimeixi només els números parells. Genera una llista d’exemple i crida la funció.
"""

def print_even_numbers( list_numbers ):

    for n in list_numbers:
        if n % 2 == 0:
            print(n," ", end ='')  

    return None


"""
5. Escriu una funció que demani un text i retorni un diccionari amb les lletres que apareixen 
i la quantitat de cops que apareixen, sense fer servir funcions d’agregació com count()
"""

def get_count_characters(phrase):

    char_dir = {}
    if isinstance(phrase, str):
        phrase = phrase.lower()
        for c in phrase:     
            char_dir[c] = char_dir[c] + 1 if c in char_dir else 1

    return char_dir


"""
6. Crea una funció que demani 5 noms de plats i el seu nombre de calories. A mesura que s’introdueixen,
 guarda aquestes dades en un diccionari i retorna’l. Executa la funció i imprimeix el diccionari resultant.
"""

def get_plate_and_calories(n_plates = 5):

    menu = {}
    for n in range(n_plates):
        plato = input( f"Introduce el nombre del plato n{n+1} : " )
        menu[plato] = input( "Introduce el numero de calorias del {plato}: " )

    return menu


