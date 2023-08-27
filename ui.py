import pygame as pg
from settings import *
from support import *
from dialogues import *
from support import *
from pygame import mixer


class Ui:

    def __init__(self,player,gamePause):
        self.screen = pg.display.get_surface()
        self.player = player

        self.dynamicUi = DynamicUI(self.player)
        self.staticUi = StaticUI(self.dynamicUi)
        self.dialogueSystem = DialogueSystem(self.player,self.dynamicUi)

        self.gamePaused = gamePause

    def display(self):

        self.staticUi.display()
        self.dynamicUi.display()
        self.dialogueSystem.display()

        if self.dynamicUi.displayMerchandise:
            self.gamePaused()


class DialogueSystem:
    def __init__(self,player,dynamicUi):

        self.screen = pg.display.get_surface()
        self.dynamicUi = dynamicUi
        self.textStartPos = [200, 500]

        self.renderedText = {}

        self.textToMove = []

        self.player = player

        self.voice = mixer.Sound("SFX/Voices/voice2.wav")
        self.voice.set_volume(0.1)

        self.fontSpritePath = "Font/SpriteSheet/WhitePeaberry/Alphabet/"
        self.fontSpriteColor = (144, 98, 93)
        self.font = pg.font.Font("Font/PeaberryBase.ttf", 16)
        self.fontColor = (0, 0, 0)

        self.dialogueBoxSprite = uiSprites["DialogueBox"].convert_alpha()
        self.boxPos = (30,440)

        self.letterSprites = None
        self.speaker = None
        self.lastSpace = None

        self.faceSpriteScale = (75,75)
        self.faceSpritePos = (70,475)
        self.speakerNameTextPos = (74,562)
        self.faceFrameIndex = 0

        self.typingSpeed = 35
        self.dialogueIndex = 1
        self.charIndex = 0

        self.xStartText = 190
        self.textXPos = self.xStartText
        self.xDistanceBetween = 13
        self.maximumXTextXBounds = 740

        self.yStartText = 495
        self.textYPos = self.yStartText
        self.textYOffset = 18
        self.maximumXTextYBounds = 531

        self.keyPressedCount = 0
        self.skipKeyPressed = False
        self.buttonPressedTime = None

        self.lineCut = False
        self.dialogueActive = False
        self.ticked = False
        self.lineFinished = False
        self.skippedDialogue = False

        self.importFaceSprites()
        self.importFontSprites()

    def importFontSprites(self):
        self.letterSprites = {
        }
        for i in letters:
            self.letterSprites[str(i)] = loadSprite(f"{self.fontSpritePath}{i}.png", (24, 24)).convert_alpha()


    def importFaceSprites(self):
        spritePath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Dialouge UI/Face/"
        self.spriteFaces = {
            "Player": [],
            "Merchant": []
        }

        for animation in self.spriteFaces.keys():
            fullPath = spritePath + animation
            self.spriteFaces[animation] = import_folder(fullPath)

    def animateFaceSprites(self):
        currentFaceAnimation = self.spriteFaces["Player"]
        if self.faceFrameIndex >= len(currentFaceAnimation) or self.lineFinished:
            self.faceFrameIndex = 0
        currentSpeakerSprite = dialogues[self.speaker][self.dialogueIndex][0]
        scaledSprite = pg.transform.scale(self.spriteFaces[currentSpeakerSprite][int(self.faceFrameIndex)].convert_alpha(), self.faceSpriteScale)
        self.screen.blit(scaledSprite, self.faceSpritePos)

    def startDialogue(self,speaker):
        self.speaker = speaker
        self.dialogueActive = True
        self.skippedDialogue = False

    def endDialogue(self):
        self.dialogueIndex = 1
        if self.speaker == "Merchant":
            self.dynamicUi.displayMerchandise = True
        self.speaker = None
        self.dialogueActive = False

    def checkPlayerInput(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            if not self.skipKeyPressed:
                if self.lineFinished:
                    self.nextDialogue()
                else:
                    self.skippedDialogue = True
            self.buttonPressedTime = pg.time.get_ticks()
            self.skipKeyPressed = True


    def checkSkipDialogue(self):
        if not self.skippedDialogue:
            return
        self.typingSpeed = 0

    def nextDialogue(self):
        self.charIndex = 0
        self.dialogueIndex += 1
        self.textXPos = self.xStartText
        self.textYPos = self.yStartText
        self.renderedText.clear()
        self.lineFinished = False
        self.typingSpeed = 35
        self.skippedDialogue = False

    def addRenderedText(self, txt):
        characterSprite = self.letterSprites[txt[self.charIndex].replace(" ", "SPACE")]
        currentTxt = txt[self.charIndex].replace(" ", "SPACE")
        self.renderedText[f"{currentTxt}{self.charIndex}"] = {
            "LetterSprite": characterSprite,
            "XPos": self.textXPos,
            "YPos": self.textYPos,
            "LetterStored": txt[self.charIndex].replace(" ", "SPACE"),
            "IndexPos": self.charIndex
        }

        self.playVoiceSFX(self.renderedText[f"{currentTxt}{self.charIndex}"]["LetterStored"])

    def playVoiceSFX(self,txt):
        if txt != "SPACE" and not self.skippedDialogue:
            pg.mixer.Sound.play(self.voice)

    def displayText(self, txt):
        if self.lineFinished : return

        if self.charIndex >= len(txt):
            self.lineFinished = True
            return

        self.checkSkipDialogue()
        self.checkTextOutOfBounds()
        if not self.lineCut:
            if not self.ticked:
                self.ticked = True
                for texts in range(len(txt)):
                    self.faceFrameIndex += 0.6
                    self.addRenderedText(txt)
                    self.textXPos += 13
                    self.animateFaceSprites()
                    self.charIndex += 1
                    self.tickTime = pg.time.get_ticks()
                    return


    def renderDialogueBox(self):
        self.screen.blit(self.dialogueBoxSprite, self.boxPos)
        self.animateFaceSprites()
        currentSpeakerSprite = dialogues[self.speaker][self.dialogueIndex][0]
        nameText = self.font.render(currentSpeakerSprite,True,self.fontColor)
        self.screen.blit(nameText,self.speakerNameTextPos)


    def fixOutOfBoundsText(self):
        self.textXPos = self.xStartText
        self.textYPos += self.textYOffset
        for textIndex, text in enumerate(reversed(self.renderedText.values())):
            if text["LetterStored"] != "SPACE":
                self.textToMove.append(text)
            else:
                reversedInt = self.textToMove[::-1]
                for index, texts in enumerate(reversedInt):
                    newTextXOffset = self.xStartText + (index * self.xDistanceBetween)
                    texts["XPos"] = newTextXOffset
                    texts["YPos"] += self.textYOffset
                    self.textXPos = newTextXOffset + self.xDistanceBetween
                self.textToMove.clear()
                self.lineCut = False
                return

    def checkTextOutOfBounds(self):
        if self.textYPos <= self.maximumXTextYBounds:
            if self.textXPos > self.maximumXTextXBounds:
                self.lineCut = True
                self.fixOutOfBoundsText()

        else:
            self.textXPos = self.xStartText
            self.textYPos = self.yStartText
            self.renderedText.clear()

    def display(self):
        currentTime = pg.time.get_ticks()

        self.checkPlayerInput()

        if self.skipKeyPressed:
            if currentTime - self.buttonPressedTime > 50:
                self.skipKeyPressed = False

        if self.ticked:
            if currentTime - self.tickTime > self.typingSpeed:
                self.ticked = False

        if self.speaker is not None:
            if self.dialogueIndex <= len(dialogues[self.speaker]):
                self.renderDialogueBox()
                self.displayText(dialogues[self.speaker][self.dialogueIndex][1].upper())
            else:
                self.endDialogue()

        for text in self.renderedText.values():
            self.screen.blit(text["LetterSprite"], (text["XPos"], text["YPos"]))


class StaticUI:
    def __init__(self,dynamicUi):
        self.screen = pg.display.get_surface()

        self.dynamicUi = dynamicUi
        self.faceContainerBackground = uiSprites["FaceContainer"].convert_alpha()
        self.faceContainerBackgroundPos = (10, 10)
        self.faceContainerBackgroundRect = self.faceContainerBackground.get_rect()

        self.coinHeartBackGround = uiSprites["HeartCoinContainer"].convert_alpha()
        self.coinHeartBackGroundPos = (120, 10)

        self.staticUi = {
            "FaceContainer": {
                "Sprite": self.faceContainerBackground,
                "Position": self.faceContainerBackgroundPos,
            },
            "CoinHeartContainer": {
                "Sprite": self.coinHeartBackGround,
                "Position": self.coinHeartBackGroundPos
            },

        }

    def display(self):
        if not self.dynamicUi.displayMerchandise:
            for keys, values in enumerate(self.staticUi.values()):
                self.screen.blit(values["Sprite"], values["Position"])


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

        self.store = MerchantStore()
        self.displayMerchandise = False



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
            1: {
                "Sprite": self.fullHeartSprite,
                "Position":(self.heartPosX,self.heartPosY)
            },
            2: {
                "Sprite": self.fullHeartSprite,
                "Position": (self.heartPosX + 30, self.heartPosY)
            },
            3: {
                "Sprite": self.fullHeartSprite,
                "Position": (self.heartPosX + 60, self.heartPosY)
            }
        }

        for i in self.hearts.values():
            self.heartList.append(i)

    def decreasePlayerHeart(self):
        self.playerLives = self.player.lives
        if self.player.lives > 0:
            self.hearts[self.player.lives]["Sprite"] = self.fullHeartSprite
            self.hearts[self.player.lives + 1]["Sprite"] = self.emptyHeartSprite
        else:
            self.hearts[1]["Sprite"] = self.emptyHeartSprite

    def resetPlayerHeart(self):
        if self.player.laidToBed:
            for i in range(1,4):
                self.hearts[i]["Sprite"] = self.fullHeartSprite

    def displayMerchantStore(self):
        if not self.displayMerchandise: return

        self.store.display()


    def display(self):
        self.displayMerchantStore()

        if not self.displayMerchandise:
            for key,values in enumerate(self.hearts.values()):
                self.screen.blit(values["Sprite"],values["Position"])
            self.coinText = self.font.render(str(self.player.coins), True, self.fontColor)
            self.screen.blit(self.coinText, self.coinCounterLocation)
            self.resetPlayerHeart()
            self.animateFace()
            self.screen.blit(self.faceSprite, self.faceSpritePos)


class MerchantStore:
    def __init__(self):
        self.screen = pg.display.get_surface()

        backGroundSpritePath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Merchant/BackGround.png"
        self.backGroundSpiteSize = (450,500)
        self.backGroundSprite = loadSprite(backGroundSpritePath,self.backGroundSpiteSize)
        self.backGroundSpritePos = (160,50)
        self.backGroundSpriteRect = self.backGroundSprite.get_rect(topleft=self.backGroundSpritePos)

    def display(self):
        self.screen.blit(self.backGroundSprite,self.backGroundSpriteRect)