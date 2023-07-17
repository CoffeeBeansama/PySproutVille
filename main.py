import pygame as pg
import sys
from settings import *
from level import Level


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WIDTH,HEIGHT))

        pg.display.set_caption("PyHarvestVille")

        self.clock = pg.time.Clock()
        self.level = Level(self)

    def run(self):

        while True:
            for event in pg.event.get():

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.level.player.getEItemEquipped()
                    if event.key == pg.K_SPACE:
                        self.level.player.useItemEquipped()
                    if event.key == pg.K_TAB:
                        self.level.renderInventory()

                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.screen.fill("black")
            self.level.update()
            pg.display.update()

            self.clock.tick(FPS)



game = Game()
game.run()