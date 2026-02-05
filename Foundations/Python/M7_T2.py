""" Crea un programa que pregunti a l'usuari quantes hores dorm de mitjana. 
Si dorm menys de 6 hores, el programa ha d'imprimir a la pantalla "Dorms poc", '
'si és més gran o igual a 6 hores, el programa ha d'imprimir a la pantalla "Dorms molt". """


average_hours_sleep = float( input('Quantes hores dorm de mitjana?') )

if average_hours_sleep < 6:
    print("Dorms poc")
else:
   print("Dorms molt")