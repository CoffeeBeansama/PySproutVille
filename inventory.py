import pygame as pg
from settings import *

class Slot:
    def __init__(self,pos):

        self.defaultSprite =  pg.transform.scale(pg.image.load("Sprites/Sprout Lands - Sprites - Basic pack/Ui/EmptySlot.png"),slotScale)
        self.screen = pg.display.get_surface()
        self.pos = pos

    def display(self,slotsImages,inventory):
        for i in range(len(slotsImages)):
            self.screen.blit(slotsImages[inventory[i]],self.pos)

class Inventory:
    def __init__(self):

        self.inventoryPos = (80, 500)
        self.screen = pg.display.get_surface()
        self.imagePath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/"
        self.background = pg.image.load(uiSprites['InventoryHolder'])

        self.currentItems = {0: "Hoe",1: "Axe", 2: "WateringCan",3: None, 4: None, 5: None, 6: None, 7: None, 8: None}
        self.inventoryCapacity = 9
        self.width = self.inventoryPos[0] // self.inventoryCapacity

        self.importSlotSprites()
        self.createSlots()

    def importSlotSprites(self):
        self.slotSprites = []

        for i in items.keys():
            images = pg.transform.scale(pg.image.load(f"{self.imagePath}{items[i]}.png"),slotScale)
            self.slotSprites.append(images)
        print(self.slotSprites)


    def createSlots(self):
        self.slotList = []

        for slots in range(self.inventoryCapacity):
            inventoryWidth = 600  #less the borders
            increment = inventoryWidth // self.inventoryCapacity

            left = (slots * increment) + (increment - self.width) + 37

            slots = Slot((left,511))
            self.slotList.append(slots)


    def display(self):
        self.screen.blit(self.background,self.inventoryPos)
        for slots in self.slotList:
            slots.display(self.slotSprites,self.currentItems)






