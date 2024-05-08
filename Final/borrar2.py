import random
from logic import *

COLORS = ['R', 'Y', 'G', 'B']
COLORF = ['Y', 'B', 'R', 'G']
INTENTOS_MAXIMOS = 10

def generar_combinacion_aleatoria():
    return random.choices(COLORS, k=4)

def verificar_posiciones_correctas(combinacion_secreta, intento):
    return sum(color_secreto == color_intento for color_secreto, color_intento in zip(combinacion_secreta, intento))

def generar_conjunto_simbolos(combinacion):
    return [f"{color}{i}" for i, color in enumerate(combinacion)]

def actualizar_conocimiento(knowledge, combinacion, resultado):
    if resultado > 0:
        for i, color in enumerate(combinacion):
            if color == COLORF[i]:
                knowledge.add(Symbol(f"{color}{i}"))
            else:
                knowledge.add(Not(Symbol(f"{color}{i}")))
    else:
        for i, color in enumerate(combinacion):
            if color != COLORF[i]:
                knowledge.add(Not(Symbol(f"{color}{i}")))

def jugar_mastermind():
    conocimiento = And()
    intentos_realizados = 0

    while intentos_realizados < INTENTOS_MAXIMOS:
        combinacion_aleatoria = generar_combinacion_aleatoria()
        posiciones_correctas = verificar_posiciones_correctas(COLORF, combinacion_aleatoria)
        conjunto_simbolos = generar_conjunto_simbolos(combinacion_aleatoria)
        actualizar_conocimiento(conocimiento, combinacion_aleatoria, posiciones_correctas)
        print("=================")
        for symbol in conjunto_simbolos:
            if model_check(conocimiento, Symbol(symbol)):
                print(f"True: {symbol}")
            else:
                print(f"False: {symbol}")

        intentos_realizados += 1

jugar_mastermind()
