""" Crea una funció que rebi per paràmetre el nombre de colors que l’usuari vol introduir. A continuació:
Demana els colors un per un amb un missatge del tipus: "Introdueix el color 1", "Introdueix el color 2", etc.
Desa cada color en una llista.
Quan tots els colors hagin estat introduïts, mostra la llista completa.
Finalment, abans de cridar la funció, es demana a l’usuari quants colors vol introduir.  """



def ask_for_colors( n_colors ):
    color_list = []
    
    for i in range( 1, n_colors + 1 ):
        color_list.append( input( "Introdueix el color " + str(i) + ": " ) )
    
    return color_list


n_colors = int( input( "Quants colors vols introduir? " ) )
print( ask_for_colors( n_colors ) )
