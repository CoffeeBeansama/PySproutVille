import pygame as pg
from settings import *
from timer import Timer


class TimeManager:
    def __init__(self,player,updateEntities):

        self.currentTime = 0
        self.startTickTime = 0
        self.screen = pg.display.get_surface()

        self.importSprites()
        
        self.transitionTickTime = None

        self.day = 1
        self.dayNightCyclePeriod = 600000
        self.darknessAnimationDuration = 2000

        self.currentPeriod = -1
        self.dayTimer = Timer(self.dayNightCyclePeriod)

        self.currentDayState = {
            1: self.Day,
            -1: self.Night
        }

        self.dayTransitioned = False
        self.entitiesUpdated = False

        self.updateEntities = updateEntities
        self.player = player

    
    def importSprites(self):
        self.darknessOpacity = 0
        self.nightDarknessSprite = loadSprite("Sprites/NightMask.png",(WIDTH, HEIGHT)).convert_alpha()
        self.nightDarknessSprite.set_alpha(0)


        self.transitionSpriteAlpha = 0
        self.sleepTransitionSprite = loadSprite("Sprites/transitionSprite.png",(WIDTH, HEIGHT)).convert_alpha()
        self.sleepTransitionSprite.set_alpha(0)

    def Day(self):
        if self.darknessOpacity >= 0:
            self.darknessOpacity -= 0.07
            self.nightDarknessSprite.set_alpha(self.darknessOpacity)
        else:
            self.newDay()

    def Night(self):
        if self.darknessOpacity <= 255:
            self.darknessOpacity += 0.07
            self.nightDarknessSprite.set_alpha(self.darknessOpacity)

    def reset(self):
        self.currentPeriod = 1
        self.getCurrentPeriod = self.currentDayState.get(self.currentPeriod)
        self.dayTransitioned = False
        self.player.laidToBed = False

    def newDay(self):
        if not self.entitiesUpdated:
            self.day += 1
            self.updateEntities() if self.day > 2 else None

            self.player.resetLives()
            self.entitiesUpdated = True

    def daySleepTransitionAnimation(self):
        if self.player.laidToBed:
            if not self.dayTransitioned:
                self.darknessFadeAnimation()
            else:
                self.relightAnimation()

    def darknessFadeAnimation(self):
        if self.transitionSpriteAlpha <= 250:
            self.transitionSpriteAlpha += 2.125
            self.sleepTransitionSprite.set_alpha(self.transitionSpriteAlpha)
        else:
            self.entitiesUpdated = False
            self.newDay()
            self.dayTransitioned = True
            self.transitionTickTime = pg.time.get_ticks()


    def relightAnimation(self):
        if self.currentTime - self.transitionTickTime > self.darknessAnimationDuration:
            self.darknessOpacity = 0
            self.nightDarknessSprite.set_alpha(self.darknessOpacity)
            if self.transitionSpriteAlpha >= 5:
                self.transitionSpriteAlpha -= 2.125
                self.sleepTransitionSprite.set_alpha(self.transitionSpriteAlpha)
            else:
                self.reset()

    def getCurrentPeriod(self):
        match self.currentPeriod:
            case -1: self.Night()
            case 1: self.Day()
    
    def renderDarkness(self):
        self.screen.blit(self.nightDarknessSprite,(0,0))
        self.screen.blit(self.sleepTransitionSprite,(0,0))
        
        

    def dayNightCycle(self):
        self.dayTimer.update()
        self.currentTime = pg.time.get_ticks()
         
        self.renderDarkness()

        if not self.dayTimer.activated:
            self.currentPeriod *= -1
            self.dayTimer.activate()

        self.getCurrentPeriod()
        self.player.checkifSleepy(self.currentPeriod)
        self.daySleepTransitionAnimation()
