import pygame as pg
from abc import ABC,abstractmethod
from settings import *


class Item(ABC):
    def __init__(self,name):

        self.equipment = False

        self.data = itemData[name]
        self.defaultUiSprite = itemData[name]["uiSprite"]
        self.selectedUiSprite = itemData[name]["uiSpriteSelected"]


class Equipment(Item):
    def __init__(self,name):
        super().__init__(name)
        self.equipment = True

    @abstractmethod
    def playerState(self):
        pass


class Hoe(Equipment):
    def __init__(self,name):
        super().__init__(name)

    def playerState(self):
        return "Hoe"


class Axe(Equipment):
    def __init__(self,name):
        super().__init__(name)

    def playerState(self):
        return "Axe"


class WateringCan(Equipment):
    def __init__(self,uiSprite):
        super().__init__(uiSprite)

    def playerState(self):
        return "WateringCan"


