import pygame as pg
from settings import *


class Tile(pg.sprite.Sprite):
    def __init__(self,image,pos,group):
        super().__init__(group)

        self.image = image

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

class InteractableObjects(Tile):
    def __init__(self,image,pos,group):
        super().__init__(image,pos,group)

class Chest(InteractableObjects):
    def __init__(self,image,pos,group):
        super().__init__(image,pos,group)


class PlantTile(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)

        self.type = "object"
        self.untiledSprite = plantTileSprites["Soil"]["untiledSprite"].convert()
        self.tiledSprite = plantTileSprites["Soil"]["tiledSprite"].convert()
        self.image = self.untiledSprite
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)





