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

        self.cycleTime = 600000
        self.fullDayDuration = 600000  # 10 minutes
        self.sunriseTime = 125000
        self.sunsetTime = 425000

        #1000 per second
        #60000 per minute
        #25000 in game one hour

        self.firstDay = True
        self.dayTime = True
        self.nightTime = False

        self.startTickTime = pg.time.get_ticks()

    def newDay(self):
        self.startTickTime = pg.time.get_ticks()

    def sunset(self):
        if self.darknessOpacity <= 255:
            self.darknessOpacity += 0.0006
            self.nightDarknessSprite.set_alpha(self.darknessOpacity)
        else:
            print("it is 9pm")


    def dayNightCycle(self):
        self.currentTime = pg.time.get_ticks()
        self.screen.blit(self.nightDarknessSprite,(0,0))
        

        if self.currentTime - self.startTickTime > self.sunsetTime:
            self.sunset()


        if self.currentTime - self.startTickTime > self.fullDayDuration:
            self.newDay()





