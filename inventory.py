import pygame as pg
from settings import *

class Slot:
    def __init__(self,pos):


        self.screen = pg.display.get_surface()
        self.slotScale = (60, 60)
        self.slotImage = pg.transform.scale(pg.image.load(uiSprites['Slot']), self.slotScale)
        self.pos = pos

    def display(self):
        self.screen.blit(self.slotImage,self.pos)

class Inventory:
    def __init__(self):

        self.inventoryPos = (80, 500)
        self.screen = pg.display.get_surface()
        self.background = pg.image.load(uiSprites['InventoryHolder'])
        self.currentItems = ["Hoe","Axe","WateringCan",None,None,None,None,None,None]
        self.inventoryCapacity = 9
        self.width = self.inventoryPos[0] // self.inventoryCapacity
        self.createSlots()

    def createSlots(self):
        self.slotList = []

        for slots in range(self.inventoryCapacity):
            inventoryWidth = 600 #less the borders
            increment = inventoryWidth // self.inventoryCapacity

            left = (slots * increment) + (increment - self.width) + 37

            slots = Slot((left,511))
            self.slotList.append(slots)


    def display(self):
        self.screen.blit(self.background,self.inventoryPos)

        for slots in self.slotList:
            slots.display()

