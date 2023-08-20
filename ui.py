import pygame as pg
from settings import *

class Ui:
    def __init__(self,player):

        self.screen = pg.display.get_surface()

        self.player = player

        self.faceContainerBackground = uiSprites["FaceContainer"].convert_alpha()
        self.faceContainerBackgroundPos = (10,10)
        self.faceContainerBackgroundRect = self.faceContainerBackground.get_rect()

        self.coinHeartBackGround = uiSprites["HeartCoinContainer"].convert_alpha()
        self.coinHeartBackGroundPos = (120,10)

        self.defaultFaceSprite = uiSprites["DefaultFace"].convert_alpha()
        self.defaultFaceSpritePos = (30,30)

        self.ui = {
            "FaceContainer": [self.faceContainerBackground,self.faceContainerBackgroundPos],
            "CoinHeartContainer": [self.coinHeartBackGround,self.coinHeartBackGroundPos],
            "DefaultFace": [self.defaultFaceSprite,self.defaultFaceSpritePos]
        }

    def display(self):
        for keys,values in enumerate(self.ui.values()):
            self.screen.blit(values[0],values[1])
