""" Escriu un programa que faci el següent:
Demani a l’usuari que introdueixi una frase.
Utilitza una funció que rebi aquesta frase com a argument i retorni un diccionari amb:
Les paraules que apareixen a la frase com a claus.
El nombre de vegades que apareixen com a valors.
No utilitzis la funció integrada count() per comptar les paraules.
Finalment, mostra el diccionari per pantalla. """


def phrase_analyse( phrase):

    word_list = phrase.replace(',',' ').split()
    word_dict = {}
    
    for w in word_list:
        word_dict[w] = word_dict.get( w, 0 ) + 1 

    return word_dict


phrase = input( "Introdueix una frase: " )
print( phrase_analyse( phrase ) )