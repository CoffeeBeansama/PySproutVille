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

        self.DayTime()
        self.cycleTime = 600000
        self.fullDayDuration = 600000  # 10 minutes
        self.dayTime = True
        self.nightTime = False

    def DayTime(self):
        self.dayTime = True
        self.startTickTime = pg.time.get_ticks()



    def NightTime(self):
        self.nightTime = True
        self.startTickTime = pg.time.get_ticks()
        print("night time")

    def dayNightCycle(self):
        self.currentTime = pg.time.get_ticks()
        self.screen.blit(self.nightDarknessSprite,(0,0))
        
        if self.dayTime:

            self.darknessOpacity += 1
            self.nightDarknessSprite.set_alpha(self.darknessOpacity)

            if self.currentTime - self.startTickTime > self.cycleTime:
                self.NightTime()
                self.dayTime = False
        elif self.nightTime:
            if self.currentTime - self.startTickTime > self.cycleTime:
                self.DayTime()
                self.nightTime = False



