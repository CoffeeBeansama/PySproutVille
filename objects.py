import pygame as pg
from tile import Tile
from abc import abstractmethod
from settings import *
from timeManager import TimeManager


class InteractableObjects(Tile):
    def __init__(self,image,pos,group):
        super().__init__(image,pos,group)

        self.interacted = False

    @abstractmethod
    def interact(self):
        pass

    @abstractmethod
    def disengage(self):
        pass


class ChestObject(pg.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.type = "object"
        self.spriteIndex = 1
        self.image = chestSprites[self.spriteIndex]
        self.animationTime = 1 / 20
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

    def OpenAnimation(self):
        self.image = chestSprites[5]

    def CloseAnimation(self):
        self.image = chestSprites[1]


class ChestTile(InteractableObjects):
    def __init__(self,pos,group,chestObject,player,image=testSprites["Wall"]):
        super().__init__(image,pos,group)


        self.type = "chest"
        self.player = player
        self.rect = image.get_rect(topleft=pos)
        self.chestObject = chestObject

    def interact(self):
        keys = pg.key.get_pressed()
        playerInventory = self.player.inventory
        if keys[pg.K_x]:
            if not self.interacted:
                self.chestObject.OpenAnimation()
                playerInventory.sellItems()
                self.interacted = True
            else:
                return

    def disengage(self):
        self.interacted = False
        self.chestObject.CloseAnimation()


class BedTile(InteractableObjects):
    def __init__(self,group,timeManager,pos=(848,800),image=testSprites["Wall"]):
        super().__init__(image,pos,group)

        self.timeManager = timeManager
        self.type = "object"
        self.rect = image.get_rect(topleft=pos)

    def interact(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_x]:
            if not self.interacted:
                self.timeManager.newDay()
                self.interacted = True

    def disengage(self):
        self.interacted = False