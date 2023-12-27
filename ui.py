import pygame as pg
from settings import *
from support import *
from dialogues import *
from support import *
from pygame import mixer
from timer import Timer


class Ui:
    def __init__(self,player,displayMerchantStore):
        self.screen = pg.display.get_surface()
        self.player = player
        self.playerLives = self.player.lives

        self.displayUi = True
        
        self.initializeBackgrounds() 
        self.initializePlayerFaceUI()
        self.initializeFonts()
        self.initializePlayerHealthHUD()

        self.timer = Timer(200)

    def initializePlayerFaceUI(self):
        self.faceSpritePos = (30, 30)
        self.faceSpriteScale = (62,62) 
        self.frameIndex = 0
        self.animationTime = 1 / 64
        self.animationStates = None
        self.importPlayerMoodSprites()

    def importPlayerMoodSprites(self):
        faceUISprite = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Face/"

        self.animationStates = {
            "Idle": [],
            "Happy": [],
            "Sleepy": []
        }

        for animation in self.animationStates.keys():
            full_path = faceUISprite + animation
            self.animationStates[animation] = import_folder(full_path)
    
    def initializePlayerHealthHUD(self):
        heartSpriteSize = (40,38)
        self.fullHeartSprite = loadSprite(uiSprites["FullHeart"],heartSpriteSize).convert_alpha()
        self.emptyHeartSprite = loadSprite(uiSprites["EmptyHeart"],heartSpriteSize).convert_alpha()
        self.heartList = []
        self.heartPosX = 133
        self.heartPosY = 19

        self.hearts = {}

        for i in range(1,4):
            self.hearts[i] = {
                    "Sprite": self.fullHeartSprite,
                    "Position": (self.heartPosX + (30 * (i - 1)), self.heartPosY)
                    }
        
        for i in self.hearts.values():
            self.heartList.append(i)

    def initializeBackgrounds(self):
        faceContainerSize = (100,100)
        self.faceContainerBackground = loadSprite(uiSprites["FaceContainer"],faceContainerSize).convert_alpha()
        self.faceContainerBackgroundPos = (10, 10)
        self.faceContainerBackgroundRect = self.faceContainerBackground.get_rect()

        coinHeartBGSize = (130,130)
        self.coinHeartBackGround = loadSprite(uiSprites["HeartCoinContainer"],coinHeartBGSize).convert_alpha()
        self.coinHeartBackGroundPos = (120, 10)

    def initializeFonts(self):
        self.font = pg.font.Font("Font/PeaberryBase.ttf", 26)
        self.fontColor = (144, 98, 93)
        self.coinCounterLocation = (160, 102)

    def handlePlayerFaceAnimation(self):
        animation = self.animationStates[self.player.mood]

        self.frameIndex += self.animationTime
        if self.frameIndex >= len(animation):
            self.frameIndex = 0 if self.player.mood != "Happy" else len(animation) -1
            
        self.faceSprite = pg.transform.scale(animation[int(self.frameIndex)],self.faceSpriteScale)

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

    def display(self):
        if not self.displayUi: return

        # Backgrounds
        self.screen.blit(self.faceContainerBackground,self.faceContainerBackgroundPos)
        self.screen.blit(self.coinHeartBackGround,self.coinHeartBackGroundPos)

        # Player Face
        self.handlePlayerFaceAnimation()
        self.screen.blit(self.faceSprite, self.faceSpritePos)

        # Coins
        self.coinText = self.font.render(str(self.player.coins), True, self.fontColor)
        self.screen.blit(self.coinText, self.coinCounterLocation)

        # Player Hearts
        for key,values in enumerate(self.hearts.values()):
            self.screen.blit(values["Sprite"],values["Position"])
            self.resetPlayerHeart()


