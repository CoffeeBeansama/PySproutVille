import pygame as pg
from settings import soilSprites

class SoilTile(pg.sprite.Sprite):
    def __init__(self, pos, group,planted,indexId):
        super().__init__(group)

        self.type = "Soil"
        self.untiledSprite = soilSprites["untiledSprite"].convert_alpha()
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
            "Untilted" : soilSprites["untiledSprite"],
            "Tilted": soilSprites["tiledSprite"],
            "Watered": soilSprites["WateredSprite"]
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
        getCurrentSprite = self.state.get(self.currentState, soilSprites["untiledSprite"].convert_alpha())
        self.image = getCurrentSprite.convert_alpha()
        return

    def update(self):
        self.currentState = "Tilted" if self.planted else "Untilted"
        self.watered = False
        getCurrentSprite = self.state.get(self.currentState)
        self.image = getCurrentSprite.convert_alpha()
        return
