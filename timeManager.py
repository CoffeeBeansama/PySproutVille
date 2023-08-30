import pygame as pg
from settings import *


class TimeManager:

    def __init__(self,player,updateEntities):

        self.currentTime = 0
        self.startTickTime = 0
        self.screen = pg.display.get_surface()

        self.darknessOpacity = 0
        self.nightDarknessSprite = pg.transform.scale(pg.image.load("Sprites/NightMask.png"),(WIDTH, HEIGHT)).convert_alpha()
        self.nightDarknessSprite.set_alpha(0)

        self.transitionSpriteAlpha = 0
        self.sleepTransitionSprite = pg.transform.scale(pg.image.load("Sprites/transitionSprite.png"),(WIDTH, HEIGHT)).convert_alpha()
        self.sleepTransitionSprite.set_alpha(0)
        self.transitionTickTime = None

        self.day = 1
        self.dayNightCyclePeriod = 300000
        self.fullDayDuration = 36000

        self.dayTime = True
        self.nightTime = False

        self.startTickTime = pg.time.get_ticks()

        self.dayTransitioned = False

        self.updateEntities = updateEntities

        self.player = player

    def newDay(self):

        self.dayTime = True
        self.nightTime = False

        self.day += 1
        self.updateEntities()

        self.nightDarknessSprite.set_alpha(0)
        self.startTickTime = pg.time.get_ticks()

    def daySleepTransitionAnimation(self):

        if self.player.laidToBed:
            if not self.dayTransitioned:
                self.darknessFadeAnimation()
            else:
                self.relightAnimation()

    def darknessFadeAnimation(self):
        if self.transitionSpriteAlpha <= 255:
            self.transitionSpriteAlpha += 2.125
            self.sleepTransitionSprite.set_alpha(self.transitionSpriteAlpha)
        else:
            self.transitionTickTime = pg.time.get_ticks()
            self.newDay()
            self.dayTransitioned = True
            self.player.resetLives()

    def relightAnimation(self):
        if self.currentTime - self.transitionTickTime > 2000:
            if self.transitionSpriteAlpha >= 0:
                self.transitionSpriteAlpha -= 2.125
                self.sleepTransitionSprite.set_alpha(self.transitionSpriteAlpha)

            else:
                self.dayTransitioned = False
                self.player.laidToBed = False

    def evening(self):
        self.nightTime = True
        self.dayTime = False
        self.startTickTime = pg.time.get_ticks()

    def sunset(self):
        if self.darknessOpacity <= 255:
            self.darknessOpacity += 0.07
            self.nightDarknessSprite.set_alpha(self.darknessOpacity)
        else:
            self.evening()

    def sunrise(self):
        if self.darknessOpacity >= 0:
            self.darknessOpacity -= 0.07
            self.nightDarknessSprite.set_alpha(self.darknessOpacity)
        else:
            self.newDay()

    def dayNightCycle(self):
        self.currentTime = pg.time.get_ticks()
        self.screen.blit(self.nightDarknessSprite,(0,0))
        self.screen.blit(self.sleepTransitionSprite,(0,0))

        if self.dayTime:
            if self.currentTime - self.startTickTime > self.dayNightCyclePeriod:
                self.sunset()

        if self.nightTime:
            if self.currentTime - self.startTickTime > self.dayNightCyclePeriod:
                self.sunrise()

        self.player.checkifSleepy(self.dayTime)
        self.daySleepTransitionAnimation()