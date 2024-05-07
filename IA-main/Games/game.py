from gui import GuiView
from model import Model
#from minimaxAlphaBetaAgent import MinimaxAlphaBetaAgent
from controller import Controller

def main():
    gui = GuiView()
    model = Model()
    #agen = minimaxAlphaBetaAgent()
    controller = Controller(model, gui)
    controller.run_state()

main()