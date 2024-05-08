# Colores
BLANCO = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_FONDO = (30, 144, 255)
FONT = 'couriernew'

# Dimensiones de la pantalla
WIDTH, HEIGHT = 650, 650

# Dimensiones y posición de los cuadrados
CUADRADO_SIZE = 100
CUADRADO_MARGIN = 20
NUM_CUADRADOS = 6

class House:
    def __init__(self, main):
        self.game_over = False
        self.main = main

    def draw_menu(self):
        self.main.screen.fill(COLOR_FONDO)

        font = self.main.pygame.font.SysFont(FONT, 40, bold=True)
        introText = font.render("HOUSE", True, BLACK)
        self.main.screen.blit(introText, (0, 0))

        
        mouse = self.main.pygame.mouse.get_pos()
        if 190 >= mouse[0] >= 90 and 90 >= mouse[1] >= 50:
            font = self.main.pygame.font.SysFont(FONT, 50, bold=True)
            introText = font.render("Back->", True, BLACK)
            self.main.screen.blit(introText, (85, 45))
        else:
            font = self.main.pygame.font.SysFont(FONT, 40, bold=True)
            introText = font.render("Back->", True, BLACK)

            self.main.screen.blit(introText, (90, 50))

    def run_game(self):
        running = True
        while running:
            for event in self.main.pygame.event.get():
                if event.type == self.main.pygame.QUIT:
                    self.main.pygame.quit()
                    running = False
                    sys.exit()
                if event.type == self.main.pygame.MOUSEBUTTONDOWN:
                    mouse = self.main.pygame.mouse.get_pos()
                    if 190 >= mouse[0] >= 90 and 90 >= mouse[1] >= 50:
                        self.main.__init__()
                        self.main.run_main()

            self.main.screen.fill(COLOR_FONDO)
            self.draw_menu()
            self.main.pygame.display.flip()