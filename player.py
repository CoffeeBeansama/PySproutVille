import pygame as pg
from entity import Entity


class Player(Entity):
    def __init__(self,image,group,collidable_sprites,level):
        super().__init__(group)

        self.level = level
        self.startingPos = (100,100)

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.startingPos)
        self.hitbox = self.rect.inflate(0, 0)

        self.collisionSprites = collidable_sprites


