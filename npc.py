import pygame as pg
from support import loadSprite
from settings import *
from objects import InteractableObjects

class Merchant(InteractableObjects):
    def __init__(self,group,interactableSprites,dialogue,dynamicUi):
        super().__init__(group)

        self.type = "npc"
        self.dialogueId = "Merchant"
        self.startingPos = (800, 795)

        self.spritePath = "Sprites/Merchant.png"

        self.dialogueSystem = dialogue
        self.dynamicUi = dynamicUi
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
                self.dialogueSystem.startDialogue(self.dialogueId)
                self.interacted = True
            else:
                return

    def disengage(self):
        self.interacted = False

class Chicken(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)

        self.type = "npc"
        self.imagePath = "Sprites/Chicken/Idle/0.png"
        self.image = pg.image.load(self.imagePath).convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

    def update(self):
        pass