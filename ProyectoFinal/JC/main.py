import pygame
import sys
import os
import Busca_minitas_aña
import colores
import tictactoe
import casas


FONT = 'couriernew'
WIDTH, HEIGHT = 1100, 700
LINE_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

def draw_state(screen, xx, yy, ruta, nameimagen):
    margin = 20
    spacing = 10

    cell_width = (WIDTH - margin * 2 - spacing * 2) // 3
    cell_height = (HEIGHT - margin * 2 - spacing * 2) // 2

    x, y = xx, yy
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x - 25, y - 25, 150, 150))
    mouse = pygame.mouse.get_pos()
    if x+100 >= mouse[0] >= x and y+100 >= mouse[1] >= y:
        image1 = pygame.image.load(os.path.join(ruta, nameimagen)).convert_alpha()
        image1 = pygame.transform.scale(image1, (150, 150))
        screen.blit(image1, (x - 25, y - 25))
    else:
        image1 = pygame.image.load(os.path.join(ruta, nameimagen)).convert_alpha()
        image1 = pygame.transform.scale(image1, (100, 100))
        screen.blit(image1, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Juegos con IA")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 225 >= mouse[0] >= 75 and 225 >= mouse[1] >= 75:
                    running = False
                    screen.fill((255, 255, 255))
                    Busca_minitas_aña.run_game()
                if False:
                # if 250 + 200 >= mouse[0] >= 250 and 190 + 50 >= mouse[1] >= 190:
                    running = False
                    screen.fill((255, 255, 255))
                    # albedo = True
                    # run_game()

        # draw_menu(screen)
        draw_state(screen)
        pygame.display.update()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((BLACK))
pygame.display.set_caption("Juegos con IA")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if 200 >= mouse[0] >= 60 and 390 >= mouse[1] >= 249:
                running = False
                screen.fill((255, 255, 255))
                Busca_minitas_aña.run_game_busca_minas()

            if 350 >= mouse[0] >= 250 and 390 >= mouse[1] >= 249:
                running = False
                screen.fill((255, 255, 255))
                colores.run_game_colors()

            if 510 >= mouse[0] >= 410 and 390 >= mouse[1] >= 249:
                running = False
                screen.fill((255, 255, 255))
                casas.run_game_casas()
                #colores.run_game_colors()

            if 650 >= mouse[0] >= 580 and 390 >= mouse[1] >= 249:
                running = False
                screen.fill((255, 255, 255))
                tictactoe.run_game_tictactoe()

            if False:
                # if 250 + 200 >= mouse[0] >= 250 and 190 + 50 >= mouse[1] >= 190:
                running = False
                screen.fill((255, 255, 255))
                    # albedo = True
                    # run_game()


    draw_state(screen, 80, 259, 'Assets/images', 'mine.png')
    draw_state(screen, 250, 259, 'Assets/images', 'colres.jpg')
    draw_state(screen, 420, 259, 'Assets/images', 'casas.jpg')
    draw_state(screen, 590, 259, 'Assets/images', 'tictactoe.png')
    pygame.display.update()
