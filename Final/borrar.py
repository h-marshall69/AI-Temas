import random
from logic import *

COLOR_BASE = ['R', 'Y', 'G', 'B']
COLOR_FINAL = ['Y', 'B', 'R', 'G']
symbols = []
INTENTOS_MAXIMOS = 10


def random_color(color_ar):
    # Crear una copia de la lista para no modificar la original
    color_ar_copy = color_ar[:]
    
    for i, color in enumerate(color_ar_copy):
        if color == '_':
            # Asignar un color aleatorio que no esté ya presente en la lista
            available_colors = [c for c in COLOR_BASE if c not in color_ar_copy]
            if available_colors:
                random_color = random.choice(available_colors)
                color_ar_copy[i] = random_color
    
    return color_ar_copy 

def random_color1():
    
    return random.choices(COLOR_BASE, k=4)

def verificar_intentos(combinacion, intento):
    pociciones = 0

    for i, color in enumerate(combinacion):
        if color == intento[i]:
            pociciones += 1

    return pociciones



def update_knowledge(knowledge, symbols, combinacion, resultado):
    ten = set()
    if verificar_intentos(resultado, combinacion) > 0:
        
        for i, color in enumerate(combinacion):
            if color == resultado[i]:
                knowledge.add(Symbol(f"{color}{i}"))
            else:
                knowledge.add(Not(Symbol(f"{color}{i}")))
                ten.add(f"{color}{i}")

    else:
        for i, color in enumerate(combinacion):
            if color != resultado[i]:
                knowledge.add(Not(Symbol(f"{color}{i}")))
                ten.add(f"{color}{i}")
    
    updated_symbols = symbols - ten
    return updated_symbols

 

def run_game():
    
    
    intentos_realizados = 0
    knowledge = And()

    color_ar = ["_" for _ in range(len(COLOR_BASE))]
    #random1 = random_color(color_ar)
    random1 = random_color1()

    while verificar_intentos(COLOR_FINAL, random1) != 0:
        #random1 = random_color(color_ar)
        random1 = random_color1()
        #color_ar = ["_" for _ in range(len(COLOR_BASE))]

    #symbols = [f"{color}{i}" for  color in COLOR_BASE for i in range(len(COLOR_BASE))]
    symbols = {f"{color}{i}" for color in COLOR_BASE for i in range(len(COLOR_BASE))}

    running = True

    while running and (intentos_realizados< INTENTOS_MAXIMOS):
        #random2 = random_color(color_ar)
        random2 = random_color1()
        symbols = update_knowledge(knowledge, symbols, random2, COLOR_FINAL)
        if color_ar != COLOR_FINAL:
            print(intentos_realizados,    "         ==============")
            for symbol in symbols:
                if model_check(knowledge, Symbol(symbol)):
                    if color_ar[int(symbol[1])] == '_':
                        color_ar[int(symbol[1])] = symbol[0]
                    print(f"True: {symbol}")
                else:
                    print(f"False: {symbol}")
            intentos_realizados += 1
        else:
            running = False
 
    print(color_ar)
run_game()