import pygame as pg
from settings import *
from dialogues import *
from support import *
from pygame import mixer
from eventManager import EventHandler

class DialogueSystem:
    def __init__(self,player,dynamicUi,displayMerchantStore,hidePlayerInventory):
        self.screen = pg.display.get_surface()
        self.player = player
        self.dynamicUi = dynamicUi
        self.hidePlayerInventory = hidePlayerInventory
        self.displayMerchantStore = displayMerchantStore

        self.renderedText = {}
        self.textToMove = []

        self.speaker = None
        self.lastSpace = None

        self.typingSpeed = 35
        self.dialogueIndex = 1
        self.charIndex = 0

        self.skipKeyPressed = False
        self.buttonPressedTime = None

        self.lineCut = False
        self.dialogueActive = False
        self.ticked = False
        self.lineFinished = False
        self.skippedDialogue = False

        self.voice = mixer.Sound("SFX/Voices/voice2.wav")
        self.voice.set_volume(0.1)

        self.initializeFonts()
        self.initializeTextPositions()
        self.initializeTextBox() 
        self.initializeFaceSpriteData()

        self.importFaceSprites()
        self.importFontSprites()



    def initializeTextPositions(self):
        self.textStartPos = [200, 500]

        self.xStartText = 190
        self.textXPos = self.xStartText
        self.xDistanceBetween = 13
        self.maximumXTextXBounds = 740

        self.yStartText = 495
        self.textYPos = self.yStartText
        self.textYOffset = 18
        self.maximumXTextYBounds = 531
    
    def initializeFonts(self):
        self.fontSpritePath = "Font/SpriteSheet/WhitePeaberry/Alphabet/"
        self.fontSpriteColor = (144, 98, 93)
        self.font = pg.font.Font("Font/PeaberryBase.ttf", 16)
        self.fontColor = (0, 0, 0)
    
    def initializeFaceSpriteData(self):
        self.faceSpriteScale = (75,75)
        self.faceSpritePos = (70,475)
        self.speakerNameTextPos = (74,562)
        self.faceFrameIndex = 0

    def initializeTextBox(self):
        dialogueBoxSize = (750,150)
        self.dialogueBoxSprite = loadSprite(uiSprites["DialogueBox"],dialogueBoxSize).convert_alpha()
        self.boxPos = (30,440)

    def importFontSprites(self):
        self.letterSprites = {}
        
        fontSpriteSize = (24,24)
        for i in letters:
            self.letterSprites[str(i)] = loadSprite(f"{self.fontSpritePath}{i}.png", fontSpriteSize).convert_alpha()


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
        self.hidePlayerInventory()

    def endDialogue(self):
        self.dialogueIndex = 1
        if self.speaker == "Merchant":
            self.displayMerchantStore()

        self.speaker = None
        self.dialogueActive = False


    def checkPlayerInput(self):
        if EventHandler.pressingInteractKey():
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
            "Surface": characterSprite,
            "X Position": self.textXPos,
            "Y Position": self.textYPos,
            "Letter": txt[self.charIndex].replace(" ", "SPACE"),
            "Index Position": self.charIndex
        }

        self.playVoiceSFX(self.renderedText[f"{currentTxt}{self.charIndex}"]["Letter"])

    def playVoiceSFX(self,txt):
        if txt != "SPACE" and not self.skippedDialogue:
            pg.mixer.Sound.play(self.voice)

    def addToRenderedText(self, txt):
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
            if text["Letter"] != "SPACE":
                self.textToMove.append(text)
            else:
                reversedInt = self.textToMove[::-1]
                for index, texts in enumerate(reversedInt):
                    newTextXOffset = self.xStartText + (index * self.xDistanceBetween)
                    texts["X Position"] = newTextXOffset
                    texts["Y Position"] += self.textYOffset
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

    def handleRendering(self):
        if self.speaker is None: return
        if self.dialogueIndex <= len(dialogues[self.speaker]):
            self.renderDialogueBox()
            self.addToRenderedText(dialogues[self.speaker][self.dialogueIndex][1].upper())
        else:
            self.endDialogue()

        for text in self.renderedText.values():
            self.screen.blit(text["Surface"], (text["X Position"], text["Y Position"]))

    def update(self):
        currentTime = pg.time.get_ticks()

        self.checkPlayerInput()

        if self.skipKeyPressed:
            if currentTime - self.buttonPressedTime > 50:
                self.skipKeyPressed = False

        if self.ticked:
            if currentTime - self.tickTime > self.typingSpeed:
                self.ticked = False
        
        self.handleRendering()


