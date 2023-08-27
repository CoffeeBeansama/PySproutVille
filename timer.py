import pygame as pg

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