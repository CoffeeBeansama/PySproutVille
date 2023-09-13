import pygame as pg
from settings import uiSprites

class ChestInventory:
    def __init__(self,inventoryClosed):
        self.screen = pg.display.get_surface()
        self.inventoryPos = (20, 50)
        self.backGroundImage = uiSprites["ChestBackground"].convert_alpha()

        self.chestOpened = False
        self.inventoryClosed = inventoryClosed

    def displayInventory(self):
        self.chestOpened = True

    def closeInventory(self):
        self.chestOpened = False
        self.inventoryClosed()


    def display(self):
        if not self.chestOpened: return
        self.screen.blit(self.backGroundImage, self.inventoryPos)

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.closeInventory()


