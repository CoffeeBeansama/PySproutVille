import pygame as pg
class TimeManager:
    def __init__(self):
        self.plantList = []
        self.currentTime = 0
        self.startTickTime = 0

        self.cycleTime = 3000

        self.DayTime()

        self.dayTime = True
        self.nightTime = False

    def DayTime(self):
        self.dayTime = True
        self.startTickTime = pg.time.get_ticks()
        print("day time")

    def NightTime(self):
        self.nightTime = True
        self.startTickTime = pg.time.get_ticks()
        print("night time")

    def dayNightCycle(self):
        self.currentTime = pg.time.get_ticks()

        if self.dayTime:
            if self.currentTime - self.startTickTime > self.cycleTime:
                self.NightTime()
                self.dayTime = False
        elif self.nightTime:
            if self.currentTime - self.startTickTime > self.cycleTime:
                self.DayTime()
                self.nightTime = False



