import pygame as pg
from settings import *
from items import *


class InventorySlot:
    def __init__(self,pos,item,index):

        self.screen = pg.display.get_surface()
        self.pos = pos
        self.index = index
        self.data = item

        self.defaultSprite = uiSprites["EmptySlot"]
        self.defaultSelectedSprite = uiSprites["EmptySlotSelected"]

        self.sprite = self.data["uiSprite"] if item is not None else self.defaultSprite
        self.selectedSprite = self.data["uiSpriteSelected"] if item is not None else self.defaultSelectedSprite

class PlayerInventory:
    def __init__(self):

        self.inventoryPos = (73, 495)
        self.slotPosY = 514
        self.screen = pg.display.get_surface()

        self.selectorSprite = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/SlotSelector.png"
        self.selectorSprite2 = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/SlotSelector2.png"

        self.selector = pg.transform.scale(pg.image.load(self.selectorSprite),slotScale).convert_alpha()
        self.selector2 = pg.transform.scale(pg.image.load(self.selectorSprite2),slotScale).convert_alpha()

        self.swappingItems = False

        self.background = uiSprites['InventoryHolder']

        self.defaultInventorySetup = [itemData["Hoe"],itemData["Axe"],itemData["WateringCan"],itemData["Wheat"],itemData["Tomato"],None,None,None,None]
        self.currentItems = self.defaultInventorySetup

        self.itemIndex = 0
        self.itemSwapIndex = 0
        self.inventoryCapacity = 9

        self.sellableItems = []
        self.width = self.inventoryPos[0] // self.inventoryCapacity

        self.slotList = []
        self.createSlots()
        self.inventoryActive = False

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
        self.currentItems[self.itemSwapIndex],self.currentItems[self.itemIndex] = self.currentItems[self.itemIndex],self.currentItems[self.itemSwapIndex]
        self.slotList[self.itemSwapIndex].data, self.slotList[self.itemIndex].data = self.slotList[self.itemIndex].data, self.slotList[self.itemSwapIndex].data
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

    def loadItems(self,index,items):
        self.currentItems[index] = itemData[items] if items is not None else None
        self.slotList[index].sprite = itemData[items]["uiSprite"] if items is not None else self.slotList[index].defaultSprite
        self.slotList[index].selectedSprite = itemData[items]["uiSpriteSelected"] if items is not None else self.slotList[index].defaultSelectedSprite

    def AddItem(self,item):
        for slotIndex,itemSlots in enumerate(self.slotList):
            if itemSlots.data is None and self.currentItems[slotIndex] is None:
                itemSlots.data = item.data
                self.currentItems[slotIndex] = item.data
                itemSlots.sprite = item.data["uiSprite"]
                itemSlots.selectedSprite = item.data["uiSpriteSelected"]
                return
            
    def PurchaseItem(self,item):
        for slotIndex,itemSlots in enumerate(self.slotList):
            if itemSlots.data is None and self.currentItems[slotIndex] is None:
                newData = itemData[f"{item.data['name']}"]
                itemSlots.data = newData
                self.currentItems[slotIndex] = newData
                itemSlots.sprite = newData["uiSprite"]
                itemSlots.selectedSprite = newData["uiSpriteSelected"]
                return

    def getCurrentSelectedItem(self):
        item = self.currentItems[self.itemIndex]["name"]  # if selecting Equipment
        return item

    def createSlots(self):
        for index,item in enumerate(self.currentItems):
            inventoryWidth = 600  # less the borders
            increment = inventoryWidth // self.inventoryCapacity
            left = (index * increment) + (increment - self.width) + 37
            newSlots = InventorySlot((left, self.slotPosY), item, index)

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
        if not self.inventoryActive: return
        self.screen.blit(self.background,self.inventoryPos)

        for index,slots in enumerate(self.slotList):
            self.screen.blit(slots.sprite.convert_alpha() if self.itemIndex != slots.index else slots.selectedSprite.convert_alpha(),slots.pos)
        self.screen.blit(self.selector,self.slotList[self.itemIndex].pos)

        if self.swappingItems:
            self.screen.blit(self.selector2, self.slotList[self.itemSwapIndex].pos)









