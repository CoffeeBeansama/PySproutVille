import pygame as pg
from settings import *
from objects import PickAbleItems
from support import loadSprite

class PlantTile(PickAbleItems):
    def __init__(self, pos, group, data,pickupitemSprites,timeManager,soilTile):
        super().__init__(pos,group,data)

        self.type = "Plants"

        self.pickupitems = pickupitemSprites

        self.data = data

        size = (tileSize,tileSize)
        self.image = loadSprite(self.data["PhaseOneSprite"],size).convert_alpha()
    
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-20, -20)

        self.timeManager = timeManager
        self.watered = False

        self.currentPhase = 1

        self.phases = {
            1: loadSprite(self.data["PhaseOneSprite"],size).convert_alpha(),
            2: loadSprite(self.data["PhaseTwoSprite"],size).convert_alpha(),
            3: loadSprite(self.data["PhaseThreeSprite"],size).convert_alpha(),
            4: loadSprite(self.data["CropSprite"],size).convert_alpha(),
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
        getCurrentSprite = self.phases.get(self.currentPhase,self.phases[1])
        self.image = getCurrentSprite


    def NextPhase(self):
        if self.currentSoil.watered:
            self.currentPhase += 1
            if self.currentPhase >= len(self.phases):
                self.add(self.pickupitems)
                self.currentSoil.planted = False
            getCurrentSprite = self.phases.get(self.currentPhase,self.data["CropSprite"])
            self.image = getCurrentSprite










