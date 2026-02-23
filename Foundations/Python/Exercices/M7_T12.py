import pandas as pd

df = pd.read_csv( "Samples\\udemy_courses.csv" )

# 1. Exploració de dades:
# Quantes columnes té el CSV, i quants registres?

n_filas, n_columnas = df.shape
print( "Número de columnas: ", n_columnas )
print( "Número de registros: ", n_filas )

# Quantes columnes de tipus enter té? I quantes de tipus decimal?

print( "Número de columnas de tipo entero: ", len(df.select_dtypes( include = "int64" )) )
print( "Número de columans de tipo decimal: ", len(df.select_dtypes( include = "float64" )) )

# Quin és el nombre de reviews màxim? I el de subcribers?

print( "Número máximo de reviews: ", df["num_reviews"].max() ) 
print( "Número máximo de num_subscribers: ", df["num_subscribers"].max() ) 

# Quina és la mitjana del ràting?

print( "Media del rating: ", df["rating"].mean() ) 

# Com has trobat totes aquestes respostes?
# Con los metodos incluidos en la clase DataFrame #

##################################################################################################################
# 2. Filtres:

# Selecciona els cursos que tenen més de 100.000 subscriptors, més d’un 4,7 de valoració i més de 90.000 ressenyes.
df_filtro_uno_v = df[ ( df["num_subscribers"] > 100000 ) & (df["rating"] > 4.7) & (df["num_reviews"] > 90000 ) ]
df_filtro_uno_q = df.query( "num_subscribers > 100000 and rating > 4.7 and num_reviews > 90000" )

print(df_filtro_uno_v)
print(df_filtro_uno_q)


# Selecciona els cursos que tenen un "instructional level" de principiants i que són de la categoria "Development".

df_filtro_dos_v = df[ (df["instructional_level"] == "Beginner Level") & (df["category"] == "Development") ]
df_filtro_dos_q = df.query( "instructional_level == 'Beginner Level' and category == 'Development'" ) 

print(df_filtro_dos_v)
print(df_filtro_dos_q)

####################################################################################################################
# 3. Agrupacions:

# Mostra el nombre de cursos per categoria.

print( "Número de cursos por : ",df.groupby("category")["id"].count())


# Mostra la mitjana de valoració per "instructional level" i “is_paid”.
print( "Media del rating por : ", df.groupby(["instructional_level","is_paid"])["rating"].mean() )

####################################################################################################################
#4. Modificació de columnes

# Afegir una columna nova al DataFrame anomenada “CursGran” que tingui com a valor True si la quantitat 
# de subscriptors és més de 50.000 i False sinó.

df["CursGran"] = df["num_subscribers"] > 50000

# Crea un dataframe que NO contingui les últimes 6 columnes del dataframe original. 
# Aquest nou dataframe guarda’l a una variable anomenada info_general.

info_general = df.iloc[:,0:-6]

print(df.info())
print( info_general.info() )

