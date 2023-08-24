import pygame as pg
from settings import *
from support import *
from dialogues import *


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
        self.textStartPos = [200, 500]
        self.textList = []
        self.player = player
        self.fontSpritePath = "Font/SpriteSheet/WhitePeaberry/Alphabet/"

        self.dialogueBoxSprite = uiSprites["DialogueBox"].convert_alpha()
        self.boxPos = (30,440)

        self.letterSprites = None
        self.speaker = None

        self.dialogueIndex = 1
        self.charIndex = 0

        self.xStartText = 175
        self.textXPos = self.xStartText

        self.yStartText = 500
        self.textYPos = self.yStartText
        self.textYOffset = 18

        self.maximumXTextBounds = 700

        self.ticked = False
        self.lineFinished = False

        self.importFontSprites()

    def importFontSprites(self):
        self.letterSprites = {
        }
        for i in letters:
            self.letterSprites[str(i)] = loadSprite(f"{self.fontSpritePath}{i}.png", (24, 24)).convert_alpha()

    def renderText(self, txt):
        if self.lineFinished:
            return

        if self.charIndex >= len(txt):
            self.lineFinished = True
            return

        self.checkTextOutOfBounds()

        if not self.ticked:
            self.ticked = True
            for texts in range(len(txt)):
                char = self.letterSprites[txt[self.charIndex].replace(" ", "SPACE")]
                self.textXPos += 13
                self.textList.append([char, self.textXPos,self.textYPos])
                self.charIndex += 1
                self.tickTime = pg.time.get_ticks()
                return

    def renderDialogueBox(self):
        self.screen.blit(self.dialogueBoxSprite, self.boxPos)

    def checkTextOutOfBounds(self):
        if self.textXPos > self.maximumXTextBounds:
            self.textXPos = self.xStartText
            self.textYPos += self.textYOffset

    def nextDialogue(self):
        self.charIndex = 0
        self.dialogueIndex += 1
        self.textXPos = 175
        self.textYPos = self.yStartText
        self.textList.clear()
        self.lineFinished = False

    def display(self):
        currentTime = pg.time.get_ticks()
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE] and self.lineFinished:
            self.nextDialogue()

        if keys[pg.K_x]:
            self.dialogueIndex = 1

        if self.ticked:
            if currentTime - self.tickTime > 50:
                self.ticked = False

        if self.speaker is not None:
            if self.dialogueIndex <= len(dialogues[self.speaker]):
                self.renderText(dialogues[self.speaker][self.dialogueIndex])
                self.renderDialogueBox()

        for i in self.textList:
            self.screen.blit(i[0], (i[1], i[2]))




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






