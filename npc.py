import pygame as pg
from support import loadSprite
from settings import *
from objects import InteractableObjects

class Merchant(InteractableObjects):
    def __init__(self,group,interactableSprites,dialogue):
        super().__init__(group)

        self.type = "Merchant"
        self.dialogueId = "Merchant"
        self.startingPos = (800, 795)

        self.spritePath = "Sprites/Merchant.png"

        self.dialogueSystem = dialogue
        self.image = pg.image.load(self.spritePath).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.startingPos)
        self.hitbox = self.rect.inflate(-40,-40)

        self.interactRect = self.image.get_rect(topleft=(self.startingPos[0], self.startingPos[1] + tileSize))
        self.interactHitbox = self.interactRect.inflate(-40,-40)

        self.interactableSprites = interactableSprites
        self.add(self.interactableSprites)


    def interact(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_x]:
            if not self.interacted:
                self.dialogueSystem.speaker = self.dialogueId
                self.interacted = True
            else:
                return

    def disengage(self):
        self.interacted = False