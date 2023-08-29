import pygame as pg
from settings import *
from enum import Enum
from abc import ABC, abstractmethod
from objects import PickAbleItems

class SoilTile(pg.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.type = "Soil"
        self.untiledSprite = plantTileSprites["Soil"]["untiledSprite"].convert()
        self.tiledSprite = plantTileSprites["Soil"]["tiledSprite"].convert()
        self.wateredSprite = plantTileSprites["Soil"]["WateredSprite"].convert_alpha()
        self.image = self.untiledSprite
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.currentPlant = None
        self.currentPhase = None
        self.tilted = False
        self.watered = False

    def tiltSoil(self):
        if self.tilted is False:
            self.image = self.tiledSprite
            self.tilted = True
        return

    def waterSoil(self):
        if self.tilted is True and self.watered is False:
            self.image = self.wateredSprite
            self.watered = True
        return

    def update(self):
        if self.tilted is True and self.watered is True and self.currentPlant is not None:
            self.watered = False
            self.image = self.tiledSprite


class PlantTile(PickAbleItems):
    def __init__(self, pos, group, data,soil,pickupitemSprites,timeManager):
        super().__init__(pos,group,data)

        self.type = "Plants"

        self.pickupitems = pickupitemSprites

        self.data = data
        self.image = self.data["PhaseOneSprite"]

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-20, -20)

        self.timeManager = timeManager
        self.soil = soil

        self.currentPhase = 1

        self.phases = {
            1: self.data["PhaseOneSprite"].convert_alpha(),
            2: self.data["PhaseTwoSprite"].convert_alpha(),
            3: self.data["PhaseThreeSprite"].convert_alpha(),
            4: self.data["CropSprite"].convert_alpha(),
        }

    def NextPhase(self):
        soil = self.soil
        if soil.tilted is True and soil.watered is True and soil.currentPlant is not None:
            soil.update()

            self.currentPhase += 1
            if self.currentPhase >= len(self.phases):
                self.add(self.pickupitems)
                self.soil.currentPlant = None

            getCurrentSprite = self.phases.get(self.currentPhase,self.data["CropSprite"].convert_alpha())
            self.image = getCurrentSprite








