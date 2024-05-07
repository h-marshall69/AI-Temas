from gui import GuiView
from model import Model
from mine import Mine
#from minimaxAlphaBetaAgent import MinimaxAlphaBetaAgent
import pygame

CELL_SIZE = 40

class Controller:
    def __init__(self, model, gui):
        self.model = model
        self.gui = gui
        self.quit = False
        self.game_over = False
        #self.mine = Mine

    #def run_state_main(self):
    def run_state(self):
        running = True
        while running:
            for event in self.gui.pygame.event.get():
                if event.type == self.gui.pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                    break

                if event.type == self.gui.pygame.MOUSEBUTTONDOWN:
                    mouse = self.gui.pygame.mouse.get_pos()
                    if 225 >= mouse[0] >= 75 and 225 >= mouse[1] >= 75:
                        running = False
                        self.gui.screen.fill((255, 255, 255))
                        #self.run_mine_sweeper()
                        self.mine = Mine(0, self.gui)
                        self.mine.run_mine_sweeper()

                    if False:
                    #if 250 + 200 >= mouse[0] >= 250 and 190 + 50 >= mouse[1] >= 190:
                        running = False
                        self.gui.screen.fill((255, 255, 255))
                        #self.albedo = True
                        self.run_game()

            #self.gui.draw_menu()
            self.gui.draw_state()
            self.gui.pygame.display.update()


