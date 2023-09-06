import pygame as pg
from random import randint
from settings import *
from objects import PickAbleItems


class Tree(pg.sprite.Sprite):
    def __init__(self, pos, group, visibleSprites, pickUpSprites, appleList):
        super().__init__(group)

        self.type = "tree"
        self.image = testSprites["Wall"]

        self.pickUpSprites = pickUpSprites
        self.visibleSprites = visibleSprites

        self.pos = pos
        self.maxLives = 3
        self.lives = 3

        self.appleList = appleList

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, 0)

        y = pos[1]

        self.dropZoneY = y + tileSize + 5

        self.fruit = None

        self.reset()

        self.producedWood = False


    def reset(self):
        x = self.pos[0]
        y = self.pos[1]

        if self.fruit is None:
            applePos = y + tileSize + 5
            newApple = Apple((x , (y - tileSize)), self.visibleSprites, itemData["Apple"],
                             (x, applePos), self.pickUpSprites, self)

            self.lives = self.maxLives
            self.producedWood = False
            self.appleList.append(newApple)
            self.fruit = newApple


    def chopped(self):
        x = self.pos[0]
        self.lives -= 1
        if self.lives <= 0 and not self.producedWood:
            Wood((x, self.dropZoneY), self.visibleSprites, itemData["Wood"], self.pickUpSprites, self)

            self.producedWood = True


class TreeLeaves(pg.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.type = "Plants"
        self.image = testSprites["Wall"]

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, -5)


class Apple(PickAbleItems):
    def __init__(self, pos, group, data, finalPos, pickUpSprites, tree):
        super().__init__(pos, group, data)

        self.type = "Apple"

        self.finalPos = finalPos
        self.tree = tree

        self.pickUpSprites = pickUpSprites

        self.image = self.data["PhaseOneSprite"].convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)


        self.currentPhase = 1

        self.phases = {
            1: self.data["PhaseOneSprite"],
            2: self.data["PhaseTwoSprite"],
            3: self.data["PhaseThreeSprite"],

        }

    def growth(self):


        self.currentPhase += 1

        getCurrentPhase = self.phases.get(self.currentPhase, self.data["PhaseThreeSprite"])
        self.image = getCurrentPhase.convert_alpha()

        if self.currentPhase >= len(self.phases):
            self.rect.centery = self.finalPos[1]
            self.hitbox.centery = self.finalPos[1]
            self.add(self.pickUpSprites)
            self.tree.fruit = None
            self.tree.reset()



class Wood(PickAbleItems):
    def __init__(self, pos, group, data, pickUpSprites, tree):
        super().__init__(pos, group, data)

        self.type = "Wood"

        self.tree = tree
        self.data = data
        self.image = self.data["CropSprite"].convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)
        self.hitbox.centery = pos[1]
        self.pickUpSprites = pickUpSprites
        self.add(self.pickUpSprites)