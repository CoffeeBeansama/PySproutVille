import pygame as pg
from random import randint

class Timer:
    def __init__(self,duration,function=None):
        self.duration = duration
        self.function = function
        self.startTime = 0
        self.activated = False


    def activate(self):
        self.activated = True
        self.startTime = pg.time.get_ticks()

    def deactivate(self):
        self.activated = False
        self.startTime = 0

    def update(self):
        currentTime = pg.time.get_ticks()
        if currentTime - self.startTime > self.duration:
            if self.function and self.startTime != 0:
                self.function()
            self.deactivate()

class AnimalTimer:
    def __init__(self,duration,function=None):
        self.duration = duration
        self.function = function
        self.startTime = 0
        self.activated = False


        self.currentDuration = -1

        self.Durations= {
            -1 : self.duration[0],
            1 : self.duration[1]
        }

    def activate(self):
        self.activated = True
        self.startTime = pg.time.get_ticks()

    def deactivate(self):
        self.currentDuration *= -1
        self.activated = False
        self.startTime = 0

    def update(self):
        currentTime = pg.time.get_ticks()
        getCurrentDuration = self.Durations.get(self.currentDuration)
        if currentTime - self.startTime > getCurrentDuration:
            if self.function and self.startTime != 0:
                self.function()
            self.deactivate()