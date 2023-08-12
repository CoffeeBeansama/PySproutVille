import pygame as pg
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
    def __init__(self,pos,group):
        super().__init__(group)
        self.type = "tree"
        self.image = testSprites["Wall"]

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15,-5)

