import pygame as pg
from settings import *

class Slot:
    def __init__(self,pos):

        self.defaultSprite =  pg.transform.scale(pg.image.load("Sprites/Sprout Lands - Sprites - Basic pack/Ui/EmptySlot.png"),slotScale)
        self.screen = pg.display.get_surface()
        self.pos = pos



class Inventory:
    def __init__(self):

        self.inventoryPos = (80, 500)
        self.screen = pg.display.get_surface()
        self.imagePath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/"
        self.background = pg.image.load(uiSprites['InventoryHolder'])

        self.currentItems = ["Hoe","Axe","WateringCan"]
        self.inventoryCapacity = 9
        self.width = self.inventoryPos[0] // self.inventoryCapacity

        self.importSlotSprites()
        self.createSlots()


    def importSlotSprites(self):
        self.slotSprites = {}

        for i in items.keys():
            images = pg.transform.scale(pg.image.load(f"{self.imagePath}{items[i]}.png"),slotScale)
            self.slotSprites[f"{items[i]}"] = images


    def createSlots(self):
        self.slotList = []

        for index,slots in enumerate(self.currentItems):
            inventoryWidth = 600  #less the borders
            increment = inventoryWidth // self.inventoryCapacity

            left = (index * increment) + (increment - self.width) + 37

            slots = Slot((left,511))
            self.slotList.append(slots)




    def display(self):
        self.screen.blit(self.background,self.inventoryPos)
        for index,slots in enumerate(self.slotList):
            self.screen.blit(self.slotSprites[self.currentItems[index]],slots.pos)







