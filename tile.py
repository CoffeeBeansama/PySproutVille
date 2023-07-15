import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self,image,pos,group):
        super().__init__(group)

        self.image = pg.image.load(image)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)


