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

        self.touched = False

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
        oldDataName = self.data['name']
        newDataName = oldDataName.replace("Seed", "Crop")
        self.data = itemData[newDataName]
        self.image = self.data["CropSprite"]
        self.add(self.level.pickAbleItemSprites)
        self.soil.currentPlant = None

    def PhaseThree(self):
        self.image = self.data["PhaseThreeSprite"]

    def PhaseFour(self):
        self.image = self.data["PhaseFourSprite"]

    def ProduceCrop(self):
        oldDataName = self.data['name']
        newDataName = oldDataName.replace("Seed", "Crop")
        self.data = itemData[newDataName]
        self.image = self.data["CropSprite"]
        self.add(self.level.pickAbleItemSprites)
        self.soil.currentPlant = None

    def playerCollision(self,plantList):
        print("this")
        self.currentTime = pg.time.get_ticks()

        white = (255, 255, 255)
        coloredImage = pg.Surface(self.image.get_size()).convert_alpha()
        coloredImage.fill(white)
        self.image.blit(coloredImage, (0, 0), special_flags=pg.BLEND_MAX)

        if not self.touched:
            self.startTick = pg.time.get_ticks()
            self.touched = True

        if self.currentTime - self.startTick > 500:
            plantList.remove(self)
            self.kill()



