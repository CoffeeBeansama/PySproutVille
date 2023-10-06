import pygame as pg
from settings import *
from objects import InteractableObjects

class BerryBush(InteractableObjects):
    def __init__(self,pos,group,visibleSprites,pickUpSprite,timeManager,playerInventory):
        super().__init__(group)
        self.type = "bush"
        self.visibleSprites = visibleSprites
        self.pickUpSprite = pickUpSprite
        self.timeManager = timeManager
        self.playerInventory = playerInventory

        self.data = itemData["Berry"]

        self.sprites = {
            1 : loadSprite(f"{spritePath}BerryBush/1.png",(16,15)),
            2: loadSprite(f"{spritePath}BerryBush/2.png", (16,15))
        }

        self.image = self.sprites[1].convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.interactHitbox = self.rect.inflate(0, 0)
        self.hitbox = self.rect.inflate(-2,-3)
        self.phase = 1

    def NextPhase(self):
        if self.phase < 2:
            self.phase += 1
            self.image = self.sprites[self.phase].convert_alpha()

    def loadPhase(self,savedPhase):
        self.phase = savedPhase
        self.image = self.sprites[self.phase].convert_alpha()

    def interact(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_x]:
            if not self.interacted and self.phase >= 2:
                self.phase -= 1
                self.image = self.sprites[self.phase].convert_alpha()
                for i in range(3):
                    self.playerInventory.AddItem(self)
                self.interacted = True
            else:
                return

    def disengage(self):
        self.interacted = False