import pygame as pg
from settings import *
from tile import *
from player import Player

class Level:
    def __init__(self,main):
        self.main = main

        self.screen = pg.display.get_surface()
        self.visibleSprites = pg.sprite.Group()
        self.collisionSprites = pg.sprite.Group()
        self.ground = pg.image.load("Map/level.png")
        self.createMap()


    def createMap(self):
        for rowIndex,row in enumerate(map):
            for columnIndex,column in enumerate(row):
                x = columnIndex * tileSize
                y = rowIndex * tileSize

                if column == "W":
                    pass
                    #Tile(testSprites["Wall"],(x,y),[self.visibleSprites,self.collisionSprites])

        self.player = Player(testSprites["Player"],[self.visibleSprites],self.collisionSprites,self)


    def update(self):
        
        self.screen.blit(pg.transform.scale(self.ground,(1700,1700)),(0,0))
        self.visibleSprites.draw(self.screen)
        self.player.update()