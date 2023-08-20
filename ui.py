import pygame as pg
from settings import *
from support import *

class Ui:
    def __init__(self,player):

        self.screen = pg.display.get_surface()

        self.player = player

        self.faceContainerBackground = uiSprites["FaceContainer"].convert_alpha()
        self.faceContainerBackgroundPos = (10,10)
        self.faceContainerBackgroundRect = self.faceContainerBackground.get_rect()

        self.coinHeartBackGround = uiSprites["HeartCoinContainer"].convert_alpha()
        self.coinHeartBackGroundPos = (120,10)

        self.faceSprite = uiSprites["DefaultFace"].convert_alpha()
        self.faceSpritePos = (30,30)

        self.font = pg.font.Font("Font/ThaleahFat.ttf",42)
        self.fontColor = (0,0,0)
        self.coinCounterLocation = (160,95)
        self.coinText = None

        self.frameIndex = 0
        self.animationTime = 1/16

        self.staticUi = {
            "FaceContainer": [self.faceContainerBackground,self.faceContainerBackgroundPos],
            "CoinHeartContainer": [self.coinHeartBackGround,self.coinHeartBackGroundPos],

        }

        self.importPlayerMoodSprites()

    def importPlayerMoodSprites(self):
        faceUISprite = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/face/"

        self.animationStates = {
            "Idle": [],
            "Happy": [],
            "Sleepy": []
        }

        for animation in self.animationStates.keys():
            full_path = faceUISprite + animation
            self.animationStates[animation] = import_folder(full_path)

    def animateFace(self):
        animation = self.animationStates[self.player.mood]

        self.frameIndex += self.animationTime

        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        self.faceSprite = animation[int(self.frameIndex)].convert_alpha()
        self.faceSprite = pg.transform.scale(self.faceSprite,(62,62))

    def display(self):
        for keys,values in enumerate(self.staticUi.values()):
            self.screen.blit(values[0],values[1])

        self.coinText = self.font.render(str(self.player.coins), True, self.fontColor)
        self.screen.blit(self.coinText, self.coinCounterLocation)

        self.animateFace()
        self.screen.blit(self.faceSprite,self.faceSpritePos)

