import pygame as pg
from abc import ABC,abstractmethod
from settings import *


class Item(ABC,pg.sprite.Sprite):
    def __init__(self,name,pos,group):
        super().__init__(group)

        self.equipment = False

        self.data = itemData[name]

        self.image = itemData[name]["sprite"]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.defaultUiSprite = itemData[name]["uiSprite"]
        self.selectedUiSprite = itemData[name]["uiSpriteSelected"]


class Equipment(pg.sprite.Sprite):
    def __init__(self,group,player):
        super().__init__(group)

        self.type = "Equipment"

        self.equipment = True

        playerDirection = player.facingDirection
        self.image = pg.Surface((12,12))

        if playerDirection == "Up":
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pg.math.Vector2(0, tileSize))
        elif playerDirection == "Down":
            self.rect = self.image.get_rect(midtop=player.rect.midbottom - pg.math.Vector2(0, tileSize))
        elif playerDirection == "Left":
            self.rect = self.image.get_rect(midright=player.rect.midleft + pg.math.Vector2(tileSize, 0))
        elif playerDirection == "Right":
            self.rect = self.image.get_rect(midleft=player.rect.midright - pg.math.Vector2(tileSize, 0))




class Apple(Item):
    def __init__(self,name,pos,group):
        super().__init__(name,pos,group)
        self.pickAble = True



