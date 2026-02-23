""" La nostra empresa es dedica a realitzar anàlisis de dades hospitalaries, 
i un client ens ha sol·licitat una eina per identificar dades bàsiques dels hospitals 
de cada comunitat autònoma de forma automàtica.

Per això, cal crear una funció que rebi dos paràmetres:

▪ Un DataFrame amb informació d’hospitals (com el del fitxer hospitals.csv).
▪ El nom d’una comunitat autònoma (com a cadena de text).

La funció ha de retornar un diccionari amb les següents dades relacionades amb la comunitat autónoma indicada:

▪ Quantitat d’hospitals que hi ha a la comunitat autònoma
▪ Quantitat d’hospitals que hi ha a la comunitat autónoma que tenen més del 50% d’ocupació
▪ Indice_satifaccion màxim de la comunitat autónoma
▪ Indice_satifaccion mínim de la comunitat autònoma
▪ Total de llits a la comunitat autónoma
▪ Mitjana de l’index de satisfacció dels hospitals de la comunitat autònoma

Finalment, carrega el fitxer adjunt amb aquesta instrucció: 
data = pd.read_csv("arxiu csv", sep = ";", encoding = "latin-1") 
i executa la funció per a diverses comunitats autònomes i mostra els resultats obtinguts. """

import pandas as pd
from pathlib import Path


def count_hospitals(df_comunity):
    return int( df_comunity["hospital_id"].count() )

def count_hospitals_with_ocupation(df_comunity, ocupation = 50):
    return int( df_comunity[ df_comunity["porcentaje_ocupacion"] > ocupation ]["hospital_id"].count() )
 
def get_max_satisfaction_index(df_comunity):
    return float( df_comunity["indice_satisfaccion"].max() )

def get_min_satisfaction_index(df_comunity):
    return float( df_comunity["indice_satisfaccion"].min() ) 

def get_mean_satisfaction_index(df_comunity, n_decimals = 1):
    return round( float( df_comunity["indice_satisfaccion"].mean() ), n_decimals )

def get_total_beds(df_comunity):
    return int( df_comunity["num_camas"].sum() )

def filter_df_by_comunity(df, comunity):
    return df[ df["comunidad_autonoma"] == comunity ]

def launch_comunity_analisys( df, comunity ):

    analisys = {}
    df_comunity = filter_df_by_comunity( df, comunity )
    
    analisys['count']               = count_hospitals(df_comunity)
    analisys['count_50%_occup']     = count_hospitals_with_ocupation(df_comunity)
    analisys['max_satisf_index']    = get_max_satisfaction_index(df_comunity)
    analisys['min_satisf_index']    = get_min_satisfaction_index(df_comunity)
    analisys['total_beds']          = get_total_beds(df_comunity)
    analisys['mean_satisf_index']   = get_mean_satisfaction_index(df_comunity)
 
    return analisys

def print_analisys( analisys, comunity ):
        
    print( comunity.center(80,'_') + "\n" )
    print( analisys , "\n")
    print( "".center(80,'_') + "\n" )


def load_data_file():

    # Fixed path for testing 
    #file = ".\\Samples\\hospitals.csv"
    file = input( "Ruta del fichero de datos desde " + str(Path.cwd()) +": " )

    p = Path(file)

    while not p.exists() :
        print( "Fichero no existe, por favor, verifica la ruta y el nombre del fichero: " )
        file = input( "Ruta del fichero de datos desde " + str(Path.cwd()) +": " )
        p = Path(file)

    file_path = p.resolve()
     
    return pd.read_csv( file_path , sep = ";", encoding = "latin-1")

def process_data_frame( df ):

    comunities = df["comunidad_autonoma"].unique()

    print( "Lista de comunidades disponibles para analizar:")
    print( comunities )

    comunity = input( "Si quiere analizar una comunidad en concreto introduzca su nombre, para analizar todas, pulse enter: " )

    if comunity == '':
        for c in comunities:
            print_analisys( launch_comunity_analisys( df, c ), c )
            
    else: 
        print_analisys(launch_comunity_analisys( df, comunity ), comunity)


#########################################################################################################################



df = load_data_file()
process_data_frame(df)








