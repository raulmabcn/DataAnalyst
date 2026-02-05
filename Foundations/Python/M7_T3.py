""" Crea un programa que pregunti a l'usuari quantes hores dorm de mitjana. 
Si dorm menys de 6 hores, el programa ha d'imprimir a la pantalla "Dorms poc", '
'si és més gran o igual a 6 hores, el programa ha d'imprimir a la pantalla "Dorms molt". """

""" Modifica el programa anterior i fes que la resposta segons les hores segueixi aquest algoritme:

Si el nombre és negatiu, el programa ha d'imprimir: "Un nombre negatiu d'hores no és possible."
Si el nombre està entre 0 i 4 (ambdós inclosos), el programa ha d'imprimir: "Dorms molt poc, això pot ser perjudicial per a la salut."
Si el nombre està entre 5 i 8 (ambdós inclosos), el programa ha d'imprimir: "Dorms una quantitat adequada per cuidar la teva salut."
Si el nombre és superior a 8, el programa ha d'imprimir: "Dorms molt! Potser és hora de plantejar-te si és necessari."
 """

average_hours_sleep = int( input('Quantes hores dorm de mitjana? ') )

if average_hours_sleep < 0:
    print("Un nombre negatiu d'hores no és possible.")
elif average_hours_sleep <= 4:
    print("Dorms molt poc, això pot ser perjudicial per a la salut.")
elif average_hours_sleep <= 8:
    print("Dorms una quantitat adequada per cuidar la teva salut.")
else:
    print("Dorms molt! Potser és hora de plantejar-te si és necessari.")