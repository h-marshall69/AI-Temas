import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Definir dimensiones de la pantalla
ANCHO = 600
ALTO = 400

# Clase para el botón de selección de colores
class BotonColor:
    def __init__(self, color, x, y):
        self.color = color
        self.radius = 20
        self.x = x
        self.y = y

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (self.x, self.y), self.radius)


# Clase principal del juego
class Mastermind:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Mastermind")

        self.botones_colores = [
            BotonColor(ROJO, 50, 50),  # Modificar las coordenadas para colocarlos en la parte superior
            BotonColor(AMARILLO, 100, 50),
            BotonColor(VERDE, 150, 50),
            BotonColor(AZUL, 200, 50)
        ]

        self.codigo = [random.choice([ROJO, AMARILLO, VERDE, AZUL]) for _ in range(4)]
        self.intentos = []
        self.combinacion = []

    def ejecutar(self):
        juego_activo = True

        while juego_activo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    juego_activo = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for boton in self.botones_colores:
                        distancia_centro = ((x - boton.x) ** 2 + (y - boton.y) ** 2) ** 0.5
                        if distancia_centro <= boton.radius:
                            if len(self.combinacion) < 4:
                                self.combinacion.append(boton.color) 
                            else:
                                self.intentos.append(self.combinacion)
                                self.combinacion = []

            self.pantalla.fill(BLANCO)

            for boton in self.botones_colores:
                boton.dibujar(self.pantalla)

            for idx, combinacion in enumerate(self.intentos):
                for i, color in enumerate(combinacion):
                    pygame.draw.circle(self.pantalla, color, (50 + i * 50, (100 + idx * 50)), 20) 
                
                font = pygame.font.Font(None, 24)  # Fuente para el número
                texto = font.render(str(self.verificar_combinacion(combinacion)), True, NEGRO)
                texto_rect = texto.get_rect(midleft=(250, (100 + idx * 50)))
                self.pantalla.blit(texto, texto_rect)

            for i, color in enumerate(self.codigo):
                pygame.draw.circle(self.pantalla, color, (50 + i * 50, 350), 20)

            pygame.display.flip()

    def verificar_combinacion(self, intentos):
        resultado = [0, 0, 0, 0]
        for i, combinacion in enumerate(intentos):
            if combinacion == self.codigo[i]:
                resultado[i] = 1

        sum = 0
        for res in resultado:
            if res == 1:
                sum += 1

        return sum

def run_game_colors():
    juego = Mastermind()
    juego.ejecutar()

pygame.quit()
