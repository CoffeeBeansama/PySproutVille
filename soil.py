import pygame as pg
from settings import spritePath,tileSize
from support import loadSprite

class SoilTile(pg.sprite.Sprite):
    def __init__(self, pos, group,planted,indexId):
        super().__init__(group)

        self.type = "Soil"
        
        self.soilSprites = {
            "untiledSprite": loadSprite(f"{spritePath}untiledDirt.png",(tileSize,tileSize)).convert_alpha(),
            "tiledSprite": loadSprite(f"{spritePath}tiledDirt.png",(tileSize,tileSize)).convert_alpha(),
            "WateredSprite": loadSprite(f"{spritePath}WateredTiledDirt.png",(tileSize,tileSize)).convert_alpha(),
        }

        self.untiledSprite = self.soilSprites["untiledSprite"]
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
            "Untilted" : self.soilSprites["untiledSprite"],
            "Tilted": self.soilSprites["tiledSprite"],
            "Watered": self.soilSprites["WateredSprite"]
        }


    def tiltSoil(self):
        if not self.watered:
            self.currentState = "Tilted"
            getCurrentSprite = self.state.get(self.currentState)
            self.image = getCurrentSprite
            return

    def waterSoil(self):
        if self.currentState == "Tilted":
            self.watered = True
            self.currentState = "Watered"
            getCurrentSprite = self.state.get(self.currentState)
            self.image = getCurrentSprite
            return

    def loadState(self):
        getCurrentSprite = self.state.get(self.currentState, self.soilSprites["untiledSprite"])
        self.image = getCurrentSprite
        return

    def update(self):
        self.currentState = "Tilted" if self.planted else "Untilted"
        self.watered = False
        getCurrentSprite = self.state.get(self.currentState)
        self.image = getCurrentSprite
        return
