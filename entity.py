import pygame as pg

class Entity(pg.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)