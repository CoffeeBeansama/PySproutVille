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


class Equipment(Item):
    def __init__(self,name,pos,group):
        super().__init__(name,pos,group)
        self.equipment = True

    @abstractmethod
    def playerState(self):
        pass


class Apple(Item):
    def __init__(self,name,pos,group):
        super().__init__(name,pos,group)
        self.pickAble = True



class Hoe(Equipment):
    def __init__(self,name,pos,group):
        super().__init__(name,pos,group)

    def playerState(self):
        return "Hoe"


class Axe(Equipment):
    def __init__(self,name,pos,group):
        super().__init__(name,pos,group)

    def playerState(self):
        return "Axe"


class WateringCan(Equipment):
    def __init__(self,name,pos,group):
        super().__init__(name,pos,group)

    def playerState(self):
        return "WateringCan"


