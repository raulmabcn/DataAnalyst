""" Crea una funció que rebi una llista de nombres i retorni una nova llista amb només els nombres parells.
Després, crea una llista amb 10 números, i:
Imprimeix quants nombres parells hi ha.
Imprimeix quins són aquests nombres parells. """


def select_pairs( number_list ):
    
    pair_list = []
    for n in number_list:
        if ( n % 2 == 0 ) : pair_list.append( n )
    
    return pair_list


number_list = [1,2,3,4,5,6,7,8,9,10]

filter_list = select_pairs( number_list )

print( len( filter_list ) )
print( filter_list )

