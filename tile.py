import pygame as pg
from timer import Timer
from settings import *


class Tile(pg.sprite.Sprite):
    def __init__(self,image,pos,group):
        super().__init__(group)
        self.type = "object"
        self.image = image

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-2,-3)

class RoofTile(Tile):
    def __init__(self,image,pos,group,playerSprite,roofTileList):
        super().__init__(image,pos,group)

        self.timer = Timer(300)
        self.imgAlpha = 255
        self.playerSprite = playerSprite
        self.roofTileList = roofTileList



    def checkInsideHouseCollision(self):
        for sprites in self.playerSprite:
            if pg.sprite.spritecollide(sprites, self.roofTileList, False):
                self.insideHouse()
            else:
                self.outsideHouse()


    def insideHouse(self):
            for sprite in self.roofTileList:
                if self.imgAlpha <= 40:
                    return
                self.imgAlpha -= 0.50
                sprite.image.set_alpha(self.imgAlpha)

    def outsideHouse(self):
        for sprite in self.roofTileList:
            if self.imgAlpha >= 255:
                return
            self.imgAlpha += 0.50
            sprite.image.set_alpha(self.imgAlpha)


    def update(self):
        self.timer.update()
        self.checkInsideHouseCollision()








