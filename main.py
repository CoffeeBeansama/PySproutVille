import pygame as pg
import sys
from settings import *


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WIDTH,HEIGHT))

        pg.display.set_caption("PyPacman")
        self.clock = pg.time.Clock()

    def run(self):

        while True:
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            pg.display.update()
            self.clock.tick(FPS)



game = Game()
game.run()