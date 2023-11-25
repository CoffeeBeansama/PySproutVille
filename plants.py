import pygame as pg
from settings import *
from objects import PickAbleItems

class PlantTile(PickAbleItems):
    def __init__(self, pos, group, data,pickupitemSprites,timeManager,soilTile):
        super().__init__(pos,group,data)

        self.type = "Plants"

        self.pickupitems = pickupitemSprites

        self.data = data
        self.image = self.data["PhaseOneSprite"].convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-20, -20)

        self.timeManager = timeManager
        self.watered = False

        self.currentPhase = 1

        self.phases = {
            1: self.data["PhaseOneSprite"].convert_alpha(),
            2: self.data["PhaseTwoSprite"].convert_alpha(),
            3: self.data["PhaseThreeSprite"].convert_alpha(),
            4: self.data["CropSprite"].convert_alpha(),
        }

        self.soilTiles = soilTile
        self.currentSoil = None
        self.getSoil()


    def getSoil(self):
        for soils in self.soilTiles:
            if soils.hitbox.colliderect(self.hitbox):
                self.currentSoil = soils
        return


    def LoadPhase(self,phase):
        self.currentPhase = phase
        if self.currentPhase >= len(self.phases):
            self.add(self.pickupitems)
            self.currentSoil.planted = False
        getCurrentSprite = self.phases.get(self.currentPhase,self.data["CropSprite"])
        self.image = getCurrentSprite


    def NextPhase(self):
        if self.currentSoil.watered:
            self.currentPhase += 1
            if self.currentPhase >= len(self.phases):
                self.add(self.pickupitems)
                self.currentSoil.planted = False
            getCurrentSprite = self.phases.get(self.currentPhase,self.data["CropSprite"])
            self.image = getCurrentSprite










