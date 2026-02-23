""" La nostra empresa está colaborant amb el colectiu de metges per veure quina càrrega de treball están patint. 
La idea es veure quins metges han de donar suport a més pacients i quins sembla que tenen menys persones a càrrec.
Per fer-ho, ens han proporcionat un conjunt de dades (hospitals.csv) 
que conté informació detallada sobre els hospitals del país.

Crea una funció en Python que rebi com a paràmetres:
▪ Un DataFrame amb dades d’hospitals.
▪ El nombre n d’hospitals que es volen obtenir com a resultat.

La funció ha de calcular, per a cada hospital la càrrega de treball dels metges, utilitzant la següent fórmula: 
              
              càrrega treball metge = num_llits /num_metges * percentatge ocupació

La funció ha de retornar els n hospitals amb més càrrega de treball per metge.
Executa la funció per obtenir 10 hospitals i després per obtenir-ne 20. """
import pandas as pd
from pathlib import Path

def load_data_file():

    # Fixed path for testing 
    
    file = ".\\Samples\\hospitals.csv"
    #file = input( "Ruta del fichero de datos desde " + str(Path.cwd()) +": " )

    p = Path(file)

    while not p.exists() :
        print( "Fichero no existe, por favor, verifica la ruta y el nombre del fichero: " )
        file = input( "Ruta del fichero de datos desde " + str(Path.cwd()) +": " )
        p = Path(file)

    file_path = p.resolve()
     
    return pd.read_csv( file_path , sep = ";", encoding = "latin-1")


def print_analisys( analisys):

    print(analisys)
    return

def launch_hospitals_analisys( df, n_hospitals ):
    
    df["carga_trabajo_medico"] = df["num_camas"] / df["num_medicos"] * df["porcentaje_ocupacion"]

    return df.sort_values("carga_trabajo_medico", ascending = False).head(n_hospitals)

def process_data_frame( df ):

    n_total_hospitals = df["hospital_id"].count()
    n_default_hospitals = 10

    n_hospitals = input( "Número de hospitales entre los " + str(n_total_hospitals) + ", que quiere analizar, por defecto "+str(n_default_hospitals)+": " )
    
    n_hospitals = int( n_hospitals ) if ( n_hospitals.isdecimal() ) else n_default_hospitals 
    
    print_analisys( launch_hospitals_analisys( df, n_hospitals ) )
            


####################################################################################
df = load_data_file()
process_data_frame( df )
