from itertools import permutations
#import termcolor
from logic import *

personas = ['Gildery', 'Minerva']
casas = ['Grifindor', 'Ravenclaw']

#gildery es ravenclaw
#minerva de grifindor

permutaciones = permutations(casas)
soluciones_set = set()

for perm in permutaciones:
    for i in range(len(personas)):
        soluciones_set.add(f"{personas[i]}_a_{perm[i]} = Symbol('{personas[i]} pertenece a {perm[i]}')")

soluciones = list(soluciones_set)

for solucion in soluciones:
    print(solucion)

for solucion in soluciones:
    exec(solucion)

symbols = [eval(solucion.split('=')[0].strip()) for solucion in soluciones]

def check_knowledge(knowledge):
    solutions = ""
    for symbol in symbols:
        if (model_check(knowledge, symbol)):
            solutions = solutions + " " + (f"{symbol}: correcto") + "\n"
        elif not model_check(knowledge, Not(symbol)):
            solutions = solutions + " " + (f"{symbol}: maybe")  + "\n"

    return solutions
            #print("js")

#knoledge = And(Or(*symbols)) Minerva_a_Grifindor
knowledge = And(
    Or(Gildery_a_Ravenclaw, Gildery_a_Grifindor),Or (Minerva_a_Ravenclaw,Minerva_a_Grifindor))

knowledge.add(And(Or(Gildery_a_Grifindor, Minerva_a_Grifindor)))

#knowledge.add(Not(Gildery_a_Grifindor))


def buscareso(negacion):
    # Obtener el valor de la variable según su nombre
    return (globals().get(negacion))

def negar(neg):
    knowledge.add(Not(buscareso(neg)))

def dudarambos(duda1, duda2):
    knowledge.add(Or(duda1),(duda2))

def escribir_personas():
    perzzz = ""
    for persona in personas:
        perzzz = perzzz + "\n" + persona
    return perzzz

# Verificar el conocimiento
#check_knowledge(knoledge)
#check_knowledge(knoledge)
def cheroka():
    print(check_knowledge(knowledge))
    return(check_knowledge(knowledge))
#print(escribir_personas())




#examplesssssss
# Gildery_a_Grifindor
cheroka()