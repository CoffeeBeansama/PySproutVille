import pygame as pg
import sys
from settings import *
from level import Level
from debug import debug


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WIDTH,HEIGHT))

        pg.display.set_caption("SproutVille")

        self.clock = pg.time.Clock()
        self.level = Level(self)



    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.level.saveload.saveGameState()
                    pg.quit()
                    sys.exit()

            self.screen.fill("black")
            self.level.update()
            pg.display.update()
            self.clock.tick(FPS)


            #debug(self.clock.get_fps())
            #day and night cycle is the bottleneck!!

game = Game()
game.run()