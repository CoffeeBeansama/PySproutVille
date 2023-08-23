import pygame as pg
from settings import *
from support import *


class Ui:
    def __init__(self,player):
        self.screen = pg.display.get_surface()
        self.player = player

        self.staticUi = StaticUI()
        self.dynamicUi = DynamicUI(self.player)
        self.dialogueSystem = DialogueSystem(self.player)

    def display(self):
        self.staticUi.display()
        self.dynamicUi.display()
        self.dialogueSystem.display()


class DialogueSystem:
    def __init__(self,player):

        self.screen = pg.display.get_surface()
        self.player = player
        self.fontSpritePath = "Font/SpriteSheet/WhitePeaberry/Alphabet/"
        self.letterSprites = None

        self.letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!","SPACE"]

        self.importFontSprites()

    def importFontSprites(self):
        self.letterSprites = {

        }
        for i in self.letters:
            self.letterSprites[str(i)] = loadSprite(f"{self.fontSpritePath}{i}.png", (32, 32)).convert_alpha()

    def display(self):
        pass


class StaticUI:
    def __init__(self):
        self.screen = pg.display.get_surface()

        self.faceContainerBackground = uiSprites["FaceContainer"].convert_alpha()
        self.faceContainerBackgroundPos = (10, 10)
        self.faceContainerBackgroundRect = self.faceContainerBackground.get_rect()

        self.coinHeartBackGround = uiSprites["HeartCoinContainer"].convert_alpha()
        self.coinHeartBackGroundPos = (120, 10)

        self.staticUi = {
            "FaceContainer": [self.faceContainerBackground, self.faceContainerBackgroundPos],
            "CoinHeartContainer": [self.coinHeartBackGround, self.coinHeartBackGroundPos],

        }


    def display(self):
        for keys, values in enumerate(self.staticUi.values()):
            self.screen.blit(values[0], values[1])


class DynamicUI:
    def __init__(self,player):
        self.screen = pg.display.get_surface()

        self.player = player
        self.faceSpritePos = (30, 30)
        self.faceSpriteScale = (62,62)


        self.playerLives = self.player.lives
        self.frameIndex = 0
        self.fullHeartSprite = uiSprites["FullHeart"].convert_alpha()
        self.emptyHeartSprite = uiSprites["EmptyHeart"].convert_alpha()

        self.animationTime = 1 / 16

        self.font = pg.font.Font("Font/PeaberryBase.ttf", 26)
        self.fontColor = (144, 98, 93)
        self.coinCounterLocation = (160, 102)
        self.coinText = None

        self.animationStates = None
        self.importPlayerMoodSprites()

        self.heartList = []
        self.heartPosX = 133
        self.heartPosY = 19
        self.createHearts()


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
            self.frameIndex = 0 if self.player.mood != "Happy" else len(animation) -1

        self.faceSprite = pg.transform.scale(animation[int(self.frameIndex)],self.faceSpriteScale).convert_alpha()

    def createHearts(self):

        self.hearts = {
            1: [self.fullHeartSprite,(self.heartPosX,self.heartPosY)],
            2: [self.fullHeartSprite, (self.heartPosX + 30, self.heartPosY)],
            3: [self.fullHeartSprite, (self.heartPosX + 60, self.heartPosY)]
        }

        for i in self.hearts.values():
            self.heartList.append(i)

    def decreasePlayerHeart(self):
        self.playerLives = self.player.lives

        if self.player.lives > 0:
            self.hearts[self.player.lives][0] = self.fullHeartSprite
            self.hearts[self.player.lives + 1][0] = self.emptyHeartSprite
        else:
            self.hearts[1][0] = self.emptyHeartSprite

    def resetPlayerHeart(self):
        if self.player.laidToBed:
            for i in range(1,4):
                self.hearts[i][0] = self.fullHeartSprite


    def display(self):

        for key,values in enumerate(self.hearts.values()):
            self.screen.blit(values[0],values[1])

        self.coinText = self.font.render(str(self.player.coins), True, self.fontColor)
        self.screen.blit(self.coinText, self.coinCounterLocation)
        self.resetPlayerHeart()
        self.animateFace()
        self.screen.blit(self.faceSprite, self.faceSpritePos)






