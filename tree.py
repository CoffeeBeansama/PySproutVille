import pygame as pg
from random import randint
from settings import testSprites


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

        randomX = randint(-2, 2)
        randomY = randint(-2, 2)
        randomAppleOffset = ((pos[0] + randomX), (pos[1] + randomY))

        RipeApple(testSprites["AppleFruit"],randomAppleOffset,appleFruitGroup)

class RipeApple(pg.sprite.Sprite):
    def __init__(self,image,pos,group):
        super().__init__(group)
        self.type = "tree"
        self.image = image


        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15,-5)



