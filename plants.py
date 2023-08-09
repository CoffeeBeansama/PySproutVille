import pygame as pg
from settings import *
from enum import Enum
from abc import ABC, abstractmethod


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

    def update(self):
        self.watered = False
        self.image = self.tiledSprite


class PlantTile(pg.sprite.Sprite):
    def __init__(self, pos, group, data,soil,level):
        super().__init__(group)

        self.type = "Plants"

        self.data = data
        self.level = level

        self.image = self.data["PhaseOneSprite"]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.soil = soil

        self.currentPhase = 1

        self.phases = {
            1: self.PhaseOne,
            2: self.PhaseTwo,
            3: self.PhaseThree,
            4: self.PhaseFour,
            5: self.ProduceCrop
        }

    def NextPhase(self):
        soil = self.soil
        if soil.tilted is True and soil.watered is True and soil.currentPlant is not None:
            soil.update()

            self.currentPhase += 1
            if self.currentPhase <= len(self.phases):
                getCurrentPhase = self.phases.get(self.currentPhase)
                getCurrentPhase()
            else:
                return

    def PhaseOne(self):
        self.image = self.data["PhaseOneSprite"]


    def PhaseTwo(self):
        self.image = self.data["PhaseTwoSprite"]
        self.add(self.level.pickAbleItemSprites)
        self.soil.currentPlant = None

    def PhaseThree(self):
        self.image = self.data["PhaseThreeSprite"]

    def PhaseFour(self):
        self.image = self.data["PhaseFourSprite"]

    def ProduceCrop(self):
        self.image = self.data["CropSprite"]
        self.add(self.level.pickAbleItemSprites)
        self.soil.currentPlant = None



