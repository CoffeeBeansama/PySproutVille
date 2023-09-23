import pygame as pg
from random import random
from settings import *
from objects import PickAbleItems
from timer import Timer

class Tree(pg.sprite.Sprite):
    def __init__(self, pos, group, visibleSprites, pickUpSprites, appleList,appleIndex):
        super().__init__(group)

        self.type = "tree"
        self.image = testSprites["Wall"].convert_alpha()

        self.pickUpSprites = pickUpSprites
        self.visibleSprites = visibleSprites

        self.pos = pos
        self.maxLives = 3
        self.lives = 3

        self.appleList = appleList
        self.appleIndex = appleIndex

        self.rect = self.image.get_rect(topleft=pos)

        self.colliderRect = self.image.get_rect(topleft=(pos[0],pos[1] - 10))
        self.hitbox = self.colliderRect.inflate(-15, 8)

        y = pos[1]

        self.dropZoneY = y + tileSize + 5

        self.fruit = None

        self.reset()

        self.producedWood = False


    def reset(self):

        self.fruit = None

        x = self.pos[0]
        y = self.pos[1]


        applePos = y + tileSize + 5
        newApple = AppleFruit((x , (y - tileSize)), self.visibleSprites, itemData["Apple"],
                                 (x, applePos), self.pickUpSprites, self,self.appleIndex,self.appleList)

        self.lives = self.maxLives
        self.producedWood = False
        self.fruit = newApple
        self.appleList.append(self.fruit)


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
        self.image = testSprites["Wall"].convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, -5)

class TreeBase(pg.sprite.Sprite):
    def __init__(self, pos, group,visibleSprites, pickUpSprites, appleList,appleIndex):
        super().__init__(group)
        self.type = "Plants"
        self.group = group
        self.pos = pos
        self.pickUpSprites = pickUpSprites
        self.visibleSprites = visibleSprites

        self.appleList = appleList
        self.appleIndex = appleIndex

        self.data = {
            "Base" : loadSprite(f"{spritePath}Tree/base.png",(tileSize,tileSize)),
            "Right":{
                "Position" : (pos[0] + tileSize, pos[1]),
                "Sprite" : loadSprite(f"{spritePath}Tree/right.png", (tileSize, tileSize)),
            },
            "UpperLeft": {
                "Position": (pos[0],pos[1] - tileSize),
                "Sprite" : loadSprite(f"{spritePath}Tree/upperLeft.png", (tileSize, tileSize)),
            },
            "UpperRight": {
                "Position": (pos[0] + tileSize,pos[1] - tileSize),
                "Sprite": loadSprite(f"{spritePath}Tree/upperRight.png", (tileSize, tileSize))
            }
        }

        self.dropZoneY = pos[1] + (tileSize + 5)

        self.image = self.data["Base"].convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, -5)

        self.treeParts = []
        self.createTreeParts()

        self.maxLives = 3
        self.lives = 3

        self.reset()

    def createTreeParts(self):
        for index,data in enumerate(self.data):
            if data != "Base":
                part = TreeParts(self.data[data]["Position"],self.data[data]["Sprite"],self.group)
                self.treeParts.append(part)

    def reset(self):

        self.fruit = []

        x = self.pos[0]
        y = self.pos[1]


        applePos = y + tileSize + 5
        appleLeft = AppleFruit((x , (y - tileSize)), self.visibleSprites, itemData["Apple"],
                          (x, applePos), self.pickUpSprites, self,self.appleIndex,self.appleList)
        appleRight = AppleFruit((x + tileSize, (y - tileSize)), self.visibleSprites, itemData["Apple"],
                                     (x + tileSize, applePos), self.pickUpSprites, self, self.appleIndex, self.appleList)

        self.fruit.append(appleLeft)
        self.fruit.append(appleRight)

        self.lives = self.maxLives
        self.producedWood = False

        for apples in self.fruit:
            self.appleList.append(apples)





class TreeParts(pg.sprite.Sprite):
    def __init__(self, pos, image,group):
        super().__init__(group)
        self.type = "Plants"
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, -5)



class AppleFruit(pg.sprite.Sprite):
    def __init__(self, pos, group, data, finalPos, pickUpSprites, tree,appleIndex,appleList):
        super().__init__(group)

        self.type = "Apple"

        self.finalPos = finalPos
        self.tree = tree
        self.data = data

        self.pickUpSprites = pickUpSprites
        self.IndexId = appleIndex
        self.appleList = appleList


        self.image = self.data["PhaseOneSprite"].convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)


        self.currentPhase = 1

        self.phases = {
            1: self.data["PhaseOneSprite"],
            2: self.data["PhaseTwoSprite"],
            3: self.data["PhaseThreeSprite"]
        }

        self.group = group


    def growth(self):

        prob = random()


        self.currentPhase += 1

        getCurrentPhase = self.phases.get(self.currentPhase, self.data["PhaseOneSprite"].convert_alpha())
        self.image = getCurrentPhase.convert_alpha()
        if self.currentPhase >= len(self.phases):
            AppleItem(self.finalPos,[self.group],itemData["Apple"],self.pickUpSprites)
            self.tree.reset()
            self.kill()


    def loadState(self):
        getCurrentPhase = self.phases.get(self.currentPhase, self.data["PhaseOneSprite"].convert_alpha())
        self.image = getCurrentPhase.convert_alpha()
        return

class AppleItem(PickAbleItems):
    def __init__(self, pos, group, data, pickUpSprites):
        super().__init__(pos, group, data)

        self.type = "Apple"

        self.image = itemData["Apple"]["PhaseThreeSprite"].convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)

        self.pickUpSprites = pickUpSprites
        self.add(self.pickUpSprites)



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