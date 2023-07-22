import pygame as pg
from abc import ABC,abstractmethod
from settings import *


class Item(ABC):
    def __init__(self):
        self.uiPath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/"


class Equipment(Item):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def playerState(self):
        pass


class Hoe(Equipment):
    def __init__(self):
        super().__init__()

        self.defaultUiSprite = slotSprites[1]
        self.selectedUiSprite = slotSprites[5]

        self.defaultSlotImage = pg.transform.scale(pg.image.load(f"{self.uiPath}{self.defaultUiSprite}.png"), slotScale)
        self.selectedUiSpriteSlotImage = pg.transform.scale(pg.image.load(f"{self.uiPath}{self.selectedUiSprite}.png"),
                                                            slotScale)

    def playerState(self):
        return "Hoe"


class Axe(Equipment):
    def __init__(self):
        super().__init__()

        self.defaultUiSprite = slotSprites[2]
        self.selectedUiSprite = slotSprites[6]

        self.defaultSlotImage = pg.transform.scale(pg.image.load(f"{self.uiPath}{self.defaultUiSprite}.png"), slotScale)
        self.selectedUiSpriteSlotImage = pg.transform.scale(pg.image.load(f"{self.uiPath}{self.selectedUiSprite}.png"),
                                                            slotScale)

    def playerState(self):
        return "Axe"


class WateringCan(Equipment):
    def __init__(self):
        super().__init__()

        self.defaultUiSprite = slotSprites[3]
        self.selectedUiSprite = slotSprites[7]

        self.defaultSlotImage = pg.transform.scale(pg.image.load(f"{self.uiPath}{self.defaultUiSprite}.png"), slotScale)
        self.selectedUiSpriteSlotImage = pg.transform.scale(pg.image.load(f"{self.uiPath}{self.selectedUiSprite}.png"),
                                                            slotScale)

    def playerState(self):
        return "WateringCan"


