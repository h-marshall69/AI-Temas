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

class Color:
    def __init__(self, model):
        self.game_over = False
        self.model = model

    def draw_menu(self):
        self.model.screen.fill(COLOR_FONDO)

        font = self.model.pygame.font.SysFont(FONT, 40, bold=True)
        introText = font.render("COLOR", True, BLACK)
        self.model.screen.blit(introText, (0, 0))

        
        mouse = self.model.pygame.mouse.get_pos()
        if 190 >= mouse[0] >= 90 and 90 >= mouse[1] >= 50:
            font = self.model.pygame.font.SysFont(FONT, 50, bold=True)
            introText = font.render("Back->", True, BLACK)
            self.model.screen.blit(introText, (85, 45))
        else:
            font = self.model.pygame.font.SysFont(FONT, 40, bold=True)
            introText = font.render("Back->", True, BLACK)

            self.model.screen.blit(introText, (90, 50))

    def run_game(self):
        running = True
        while running:
            for event in self.model.pygame.event.get():
                if event.type == self.model.pygame.QUIT:
                    self.model.pygame.quit()
                    running = False
                    sys.exit()
                if event.type == self.model.pygame.MOUSEBUTTONDOWN:
                    mouse = self.model.pygame.mouse.get_pos()
                    if 190 >= mouse[0] >= 90 and 90 >= mouse[1] >= 50:
                        self.model.__init__()
                        self.model.run_model()

            self.model.screen.fill(COLOR_FONDO)
            self.draw_menu()
            self.model.pygame.display.flip()