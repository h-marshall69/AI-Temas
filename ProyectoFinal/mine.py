import pygame
# Colors used
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (127, 127, 127)
# Sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30
# Sets the starting number of squares
NSQUARES = 10
# Sets the margin between each cell
MARGIN = 5
MENU_SIZE = 40
LEFT_CLICK = 1
RIGHT_CLICK = 3

class Cell:
    def __init__(self, x, y, main):
        self.x = x
        self.y = y
        self.is_visible = False
        self.has_bomb = False
        self.bomb_count = 0
        self.text = ""
        self.test = False
        self.has_flag = False
        self.main = main

    def show_text(self):
        if self.is_visible:
            if self.bomb_count == 0:
                self.text = self.main.font.render("", True, BLACK)
            else:
                self.text = self.main.font.render(str(self.bomb_count), True, BLACK)
            self.main.screen.blit(self.text, (self.x * (WIDTH + MARGIN) + 12, self.y * (HEIGHT + MARGIN) + 10 + MENU_SIZE))


class Mine:
    def __init__(self, main):
        self.game_over = False
        self.main = main
        self.init_game()

    def init_game(self, nsquares_x = NSQUARES, nsquares_y = NSQUARES):
        self.squares_x = nsquares_x
        self.squares_y = nsquares_y
        self.grid = [[Cell(x, y, self.main) for x in range(self.squares_x)] for y in range(self.squares_y)]

    def draw_game(self):
        self.main.screen.blit(self.main.background, (0, 0))

        # Draw the grid
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                color = WHITE
                if self.grid[row][column].is_visible:
                     color = RED if self.grid[row][column].has_bomb else GRAY  
                elif self.grid[row][column].has_flag:
                    color = BLUE
                self.main.pygame.draw.rect(self.main.screen,color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN + MENU_SIZE,
                                WIDTH,
                                HEIGHT])
                self.grid[row][column].show_text()

    def draw_menu(self):
        #self.main.screen.fill(COLOR_FONDO)
        self.main.screen.blit(self.main.background, (0, 0))

        font = self.main.pygame.font.Font(self.main.FONT, 80)
        introText = font.render("Minesweeper", True, 'white')
        self.main.screen.blit(introText, (0, 0))

        mouse = self.main.pygame.mouse.get_pos()
        if 190 >= mouse[0] >= 90 and 90 >= mouse[1] >= 50:
            font = self.main.pygame.font.SysFont(self.main.FONT, 80, bold=True)
            introText = font.render("Back->", True, BLACK)
            self.main.screen.blit(introText, (85, 45))
            font = self.main.pygame.font.SysFont(self.main.FONT, 70, bold=True)
            introText = font.render("Play->", True, BLACK)
            self.main.screen.blit(introText, (90, 100))
        elif 190 >= mouse[0] >= 90 and 140 >= mouse[1] >= 100:
            font = self.main.pygame.font.SysFont(self.main.FONT, 70, bold=True)
            introText = font.render("Back->", True, BLACK)
            self.main.screen.blit(introText, (90, 50))
            font = self.main.pygame.font.SysFont(self.main.FONT, 80, bold=True)
            introText = font.render("Play->", True, BLACK)
            self.main.screen.blit(introText, (85, 95))
        else:
            font = self.main.pygame.font.SysFont(self.main.FONT, 70, bold=True)
            introText = font.render("Back->", True, BLACK)
            self.main.screen.blit(introText, (90, 50))
            introText = font.render("Play->", True, BLACK)
            self.main.screen.blit(introText, (90, 100))


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
                    elif 190 >= mouse[0] >= 90 and 140 >= mouse[1] >= 100:
                        #running = False
                        self.init_game()
                        self.run_game_easy()

            self.main.screen.blit(self.main.background, (0, 0))
            self.draw_menu()
            self.main.pygame.display.flip()