import pygame as pg
from settings import *
from enum import Enum
from abc import ABC, abstractmethod
from objects import PickAbleItems

class SoilTile(pg.sprite.Sprite):
    def __init__(self, pos, group,planted,indexId):
        super().__init__(group)

        self.type = "Soil"
        self.untiledSprite = plantTileSprites["Soil"]["untiledSprite"].convert_alpha()
        self.image = self.untiledSprite
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.indexId = indexId
        self.currentPlant = None
        self.currentPhase = None
        self.tilted = False
        self.watered = False
        self.planted = planted

        self.currentState = "Untilted"
        self.state = {
            "Untilted" : plantTileSprites["Soil"]["untiledSprite"],
            "Tilted": plantTileSprites["Soil"]["tiledSprite"],
            "Watered": plantTileSprites["Soil"]["WateredSprite"]
        }


    def tiltSoil(self):
        if not self.watered:
            self.currentState = "Tilted"
            getCurrentSprite = self.state.get(self.currentState)
            self.image = getCurrentSprite.convert_alpha()
            return

    def waterSoil(self):
        if self.currentState == "Tilted":
            self.watered = True
            self.currentState = "Watered"
            getCurrentSprite = self.state.get(self.currentState)
            self.image = getCurrentSprite.convert_alpha()
            return


    def loadState(self):
        getCurrentSprite = self.state.get(self.currentState,plantTileSprites["Soil"]["untiledSprite"].convert_alpha())
        self.image = getCurrentSprite.convert_alpha()
        return

    def update(self):
        self.currentState = "Tilted" if self.planted else "Untilted"
        self.watered = False
        getCurrentSprite = self.state.get(self.currentState)
        self.image = getCurrentSprite.convert_alpha()
        return


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
        getCurrentSprite = self.phases.get(self.currentPhase,self.data["CropSprite"].convert_alpha())
        self.image = getCurrentSprite


    def NextPhase(self):
        if self.currentSoil.watered:
            self.currentPhase += 1
            if self.currentPhase >= len(self.phases):
                self.add(self.pickupitems)
                self.currentSoil.planted = False
            getCurrentSprite = self.phases.get(self.currentPhase,self.data["CropSprite"].convert_alpha())
            self.image = getCurrentSprite










