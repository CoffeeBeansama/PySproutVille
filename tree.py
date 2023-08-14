import pygame as pg
from random import randint
from settings import *


class TreeTrunk(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.type = "tree"
        self.image = testSprites["Wall"]

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15,0)


    def chopped(self):
        print("chopped!")
class TreeLeaves(pg.sprite.Sprite):
    def __init__(self,pos,group,appleFruitGroup):
        super().__init__(group)
        self.type = "tree"
        self.image = testSprites["Wall"]

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15,-5)

        randomX = randint(pos[0] - 3, pos[0] + 3)
        randomY = randint(pos[1] - 4, pos[1] + 5)
        randomAppleOffset = (randomX, randomY)

        RipeApple(itemData["Apple"]["PhaseOneSprite"].convert_alpha(),randomAppleOffset,appleFruitGroup)

class RipeApple(pg.sprite.Sprite):
    def __init__(self,image,pos,group):
        super().__init__(group)
        self.type = "tree"
        self.image = image


        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15,-5)

        self.currentPhase = 1

        self.phases = {
            1: self.PhaseOne,
            2: self.PhaseTwo,
            3: self.PhaseThree,
        }

    def NextPhase(self):
        pass

    def PhaseOne(self):
        pass

    def PhaseTwo(self):
        pass

    def PhaseThree(self):
        self.ProduceCrop()

    def ProduceCrop(self):
        pass