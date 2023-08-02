import pygame as pg
from settings import *
from items import *


class Slot:
    def __init__(self,pos,item,index):

        self.screen = pg.display.get_surface()
        self.pos = pos
        self.index = index
        self.itemHolding = item
        self.sprite = self.itemHolding["uiSprite"]
        self.selectedSprite = self.itemHolding["uiSpriteSelected"]


class EmptySlot:
    def __init__(self, pos, item, index):
        self.screen = pg.display.get_surface()
        self.pos = pos
        self.index = index
        self.itemHolding = item
        self.sprite = pg.transform.scale(pg.image.load("Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/EmptySlot.png"), slotScale)
        self.selectedSprite = pg.transform.scale(pg.image.load("Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/EmptySlotSelected.png"), slotScale)


class Inventory:
    def __init__(self):

        self.inventoryPos = (80, 500)
        self.slotPosY = 514
        self.screen = pg.display.get_surface()

        self.selectorSprite = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/SlotSelector.png"
        self.selectorSprite2 = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/SlotSelector2.png"

        self.selector = pg.transform.scale(pg.image.load(self.selectorSprite),slotScale)
        self.selector2 = pg.transform.scale(pg.image.load(self.selectorSprite2),slotScale)

        self.swappingItems = False

        self.background = pg.image.load(uiSprites['InventoryHolder'])

        self.defaultInventorySetup = [itemData["Hoe"],itemData["Axe"],itemData["WateringCan"],itemData["Wheat"],itemData["Tomato"],None,None,None,None]
        self.currentItems = self.defaultInventorySetup

        self.itemIndex = 0
        self.itemSwapIndex = 0
        self.inventoryCapacity = 9

        self.width = self.inventoryPos[0] // self.inventoryCapacity

        self.createSlots()

    def selectFromRight(self):
        if not self.swappingItems:
            self.itemIndex += 1
            if self.itemIndex >= self.inventoryCapacity:
                self.itemIndex = 0
        else:
            self.itemSwapIndex += 1
            if self.itemSwapIndex >= self.inventoryCapacity:
                self.itemSwapIndex = 0

    def selectFromLeft(self):
        if not self.swappingItems:
            self.itemIndex -= 1
            if self.itemIndex == -1:
                self.itemIndex = self.inventoryCapacity -1
        else:
            self.itemSwapIndex -= 1
            if self.itemSwapIndex == -1:
                self.itemSwapIndex = self.inventoryCapacity -1

    def swapItems(self):

        # Item Swap Logic
        self.currentItems[self.itemSwapIndex],self.currentItems[self.itemIndex] = self.currentItems[self.itemIndex],self.currentItems[self.itemSwapIndex]
        self.slotList[self.itemSwapIndex].sprite,self.slotList[self.itemIndex].sprite = self.slotList[self.itemIndex].sprite,self.slotList[self.itemSwapIndex].sprite
        self.slotList[self.itemSwapIndex].selectedSprite,self.slotList[self.itemIndex].selectedSprite = self.slotList[self.itemIndex].selectedSprite,self.slotList[self.itemSwapIndex].selectedSprite

        self.itemIndex = self.itemSwapIndex

    def renderSelector(self):
        if self.swappingItems:
            self.swapItems()
            self.swappingItems = False
        else:
            self.itemSwapIndex = self.itemIndex
            self.swappingItems = True

    def selectingEquipmentSlot(self):
        if self.currentItems[self.itemIndex] is not None:
            if self.currentItems[self.itemIndex]["name"] in equipmentItems:
                return True
            elif self.currentItems[self.itemIndex]["name"] in seedItems:
                return True
            else:
                return False

    def getCurrentSelectedItem(self):
        item = self.currentItems[self.itemIndex]["name"]  # if selecting Equipment
        return item

    def createSlots(self):
        self.slotList = []

        for index,item in enumerate(self.currentItems):
            inventoryWidth = 600  # less the borders
            increment = inventoryWidth // self.inventoryCapacity

            left = (index * increment) + (increment - self.width) + 37

            newSlots = Slot((left,self.slotPosY),item,index) if self.currentItems[index] is not None else EmptySlot((left,self.slotPosY),item,index)

            self.slotList.append(newSlots)

    def update(self,item):
        for itemIndex,items in enumerate(self.currentItems):
            if items is None:
                self.currentItems[itemIndex] = item
                self.slotList[itemIndex].sprite = item["uiSprite"]
                self.slotList[itemIndex].selectedSprite = item["uiSpriteSelected"]
                return
            else:
                pass

    def display(self):

        self.screen.blit(self.background,self.inventoryPos)

        for index,slots in enumerate(self.slotList):

            self.screen.blit(slots.sprite.convert_alpha() if self.itemIndex != slots.index else slots.selectedSprite.convert_alpha(),slots.pos)
        self.screen.blit(self.selector,self.slotList[self.itemIndex].pos)

        if self.swappingItems:
            self.screen.blit(self.selector2, self.slotList[self.itemSwapIndex].pos)









