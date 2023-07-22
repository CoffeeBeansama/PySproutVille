import pygame as pg
from abc import ABC,abstractmethod
from settings import *


class Item(ABC):
    def __init__(self,uiSprite):

        self.equipment = False

        self.uiPath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/"

        self.defaultUiSprite = uiSprite
        self.selectedUiSprite = f"{self.defaultUiSprite}Selected"

        self.defaultSlotImage = pg.transform.scale(pg.image.load(f"{self.uiPath}{self.defaultUiSprite}.png"), slotScale)
        self.selectedUiSpriteSlotImage = pg.transform.scale(pg.image.load(f"{self.uiPath}{self.selectedUiSprite}.png"),slotScale)


class Equipment(Item):
    def __init__(self,uiSprite):
        super().__init__(uiSprite)
        self.equipment = True

    @abstractmethod
    def playerState(self):
        pass


class Hoe(Equipment):
    def __init__(self,uiSprite):
        super().__init__(uiSprite)

    def playerState(self):
        return "Hoe"


class Axe(Equipment):
    def __init__(self,uiSprite):
        super().__init__(uiSprite)

    def playerState(self):
        return "Axe"


class WateringCan(Equipment):
    def __init__(self,uiSprite):
        super().__init__(uiSprite)

    def playerState(self):
        return "WateringCan"


