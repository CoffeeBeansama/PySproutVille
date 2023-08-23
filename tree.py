import pygame as pg
from random import randint
from settings import *
from objects import PickAbleItems

class Tree(pg.sprite.Sprite):
    def __init__(self,pos,group,visibleSprites,pickUpSprites,timeManager):
        super().__init__(group)
        self.type = "tree"
        self.image = testSprites["Wall"]

        self.pickUpSprites = pickUpSprites
        self.visibleSprites = visibleSprites

        self.pos = pos
        self.maxLives = 3
        self.lives = 3

        self.timeManager = timeManager

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15,0)

        x = pos[0]
        y = pos[1]

        randomX = randint(-3,3)
        randomY = randint(-3,3)
        self.dropZoneY = y + tileSize + 5

        TreeLeaves((x, y - tileSize), [group])
        apple = Apple((x + randomX, (y - tileSize) + randomY), visibleSprites,itemData["Apple"], (x, self.dropZoneY), self.pickUpSprites,self)
        self.fruit = apple
        self.timeManager.plantList.append(self)

        self.producedWood = False

    def NextPhase(self):
        self.fruit.growth() if self.fruit is not None else self.reset()

    def reset(self):
        x = self.pos[0]
        y = self.pos[1]

        randomX = randint(-3,3)
        randomY = randint(-3,3)
        applePos = y + tileSize + 5

        newApple = Apple((x + randomX, (y - tileSize) + randomY), self.visibleSprites, itemData["Apple"],
                         (x, applePos), self.pickUpSprites, self)

        self.fruit = newApple

        self.lives = self.maxLives
        self.producedWood = False



    def chopped(self):
        x = self.pos[0]
        self.lives -= 1
        if self.lives <= 0 and not self.producedWood:
            Wood((x,self.dropZoneY),self.visibleSprites,itemData["Wood"],self.pickUpSprites,self)

            self.producedWood = True


class TreeLeaves(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.type = "Plants"
        self.image = testSprites["Wall"]

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15,-5)

class Apple(PickAbleItems):
    def __init__(self,pos,group,data,finalPos,pickUpSprites,tree):
        super().__init__(pos,group,data)

        self.type = "Apple"

        self.finalPos = finalPos
        self.tree = tree

        self.pickUpSprites = pickUpSprites
        self.PhaseOne()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10,-10)

        self.currentPhase = 1

        self.phases = {
            1: self.PhaseOne,
            2: self.PhaseTwo,
            3: self.PhaseThree,

        }

    def growth(self):
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
        self.tree.fruit = None


class Wood(PickAbleItems):
    def __init__(self,pos,group,data,pickUpSprites,tree):
        super().__init__(pos,group,data)

        self.type = "Wood"

        self.tree = tree
        self.data = data
        self.image = self.data["CropSprite"].convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
        self.hitbox.centery = pos[1]
        self.pickUpSprites = pickUpSprites
        self.add(self.pickUpSprites)
