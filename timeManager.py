import pygame as pg
from settings import *


class TimeManager:

    def __init__(self):
        self.plantList = []
        self.currentTime = 0
        self.startTickTime = 0
        self.screen = pg.display.get_surface()

        self.darknessOpacity = 0
        self.nightDarknessSprite = pg.transform.scale(pg.image.load("Sprites/NightMask.png"),(WIDTH, HEIGHT)).convert_alpha()
        self.nightDarknessSprite.set_alpha(0)

        self.day = 1
        self.dayNightCyclePeriod = 300000
        self.fullDayDuration = 36000  # 10 minutes

        # sunrise at 5am
        # sunset 6pm-9pm
        # 7.08 minutes sunset starts
        # 8.33 minutes at full darkness
        # 1000 per second
        # 60000 per minute
        # 25000 in game one hour

        self.dayTime = True
        self.nightTime = False

        self.startTickTime = pg.time.get_ticks()

    def newDay(self):
        self.dayTime = True
        self.nightTime = False

        self.day += 1
        if len(self.plantList) > 0:
            for plants in self.plantList:
                plants.NextPhase()

        self.nightDarknessSprite.set_alpha(0)
        self.startTickTime = pg.time.get_ticks()

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

        if self.dayTime:
            if self.currentTime - self.startTickTime > self.dayNightCyclePeriod:
                self.sunset()

        if self.nightTime:
            if self.currentTime - self.startTickTime > self.dayNightCyclePeriod:
                self.sunrise()






