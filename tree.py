import pygame as pg
from random import randint
from settings import *
from objects import PickAbleItems

class Tree(pg.sprite.Sprite):
    def __init__(self,pos,group,appleFruitGroup,timeManager,pickUpSprites):
        super().__init__(group)
        self.type = "tree"
        self.image = testSprites["Wall"]

        self.pickUpSprites = pickUpSprites
        self.timeManager = timeManager

        self.lives = 3

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15,0)

        x = pos[0]
        y = pos[1]

        randomX = randint(-3,3)
        randomY = randint(-3,3)
        appleFruitFinalPosY = y + tileSize + 5

        TreeLeaves((x, y - tileSize), [group])

        self.apple = Apple((x + randomX, (y - tileSize) + randomY), appleFruitGroup,itemData["Apple"], (x, appleFruitFinalPosY), self.pickUpSprites,self.timeManager)
        self.timeManager.plantList.append(self.apple)

    def chopped(self):
        self.lives -= 1
        if self.lives <= 0:
            print("this")


class TreeLeaves(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.type = "Plants"
        self.image = testSprites["Wall"]

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15,-5)


class Apple(PickAbleItems):
    def __init__(self,pos,group,data,finalPos,pickUpSprites,timeManager):
        super().__init__(pos,group,data)

        self.type = "Apple"

        self.finalPos = finalPos

        self.timeManager = timeManager

        self.pickUpSprites = pickUpSprites
        self.PhaseOne()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

        self.currentPhase = 1

        self.phases = {
            1: self.PhaseOne,
            2: self.PhaseTwo,
            3: self.PhaseThree,

        }

    def NextPhase(self):
        self.currentPhase += 1
        if self.currentPhase <= len(self.phases):
            getCurrentPhase = self.phases.get(self.currentPhase, self.PhaseOne)
            getCurrentPhase()
        else:
            return

    def PhaseOne(self):
        self.image = self.data["PhaseOneSprite"].convert_alpha()

    def PhaseTwo(self):
        self.image = self.data["PhaseTwoSprite"].convert_alpha()

    def PhaseThree(self):
        self.ProduceCrop()

    def ProduceCrop(self):
        self.image = self.data["PhaseThreeSprite"].convert_alpha()
        self.rect.centery = self.finalPos[1]
        self.hitbox.centery = self.finalPos[1]

        self.add(self.pickUpSprites)

