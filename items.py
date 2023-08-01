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





class Apple(Item):
    def __init__(self,name,pos,group):
        super().__init__(name,pos,group)
        self.pickAble = True



