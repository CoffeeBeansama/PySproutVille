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

class Chest(InteractableObjects):
    def __init__(self,image,pos,group):
        super().__init__(image,pos,group)

    def interact(self):
        pass

class Bed(InteractableObjects):
    def __init__(self,group,level,pos=(848,800),image=testSprites["Wall"]):
        super().__init__(image,pos,group)

        self.level = level
        self.type = "object"
        self.rect = image.get_rect(topleft=pos)

    def interact(self):
        self.level.timeManager.newDay()

