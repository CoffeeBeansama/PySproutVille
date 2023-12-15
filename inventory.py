import pygame as pg
from settings import uiPath,slotScale,itemData,animalFodders,equipmentItems,seedItems
from timer import Timer
from pygame import mixer
from sound import *
from support import loadSprite
from eventManager import EventHandler


class InventorySlot:
    def __init__(self,pos,data,index):

        self.screen = pg.display.get_surface()
        self.pos = pos
        self.index = index
        self.data = data

        self.stackNum = 1
        self.maximumStack = 9
        
        self.defaultSprite = loadSprite(f"{uiPath}Slots/EmptySlot.png",slotScale).convert_alpha()
        self.defaultSelectedSprite = loadSprite(f"{uiPath}Slots/EmptySlotSelected.png",slotScale).convert_alpha()

        self.sprite = self.data["Default Sprite"] if data is not None else self.defaultSprite.convert_alpha()
        self.selectedSprite = self.data["Selected Sprite"] if data is not None else self.defaultSelectedSprite.convert_alpha()

        self.textRect = self.sprite.get_rect(topleft=pos)

class PlayerInventory:
    def __init__(self,chestInventory):
        self.chestInventory = chestInventory
        self.screen = pg.display.get_surface()
        
    

        self.swappingItems = False

        self.sellableItems = []
        
        self.initializeInventory()
        
        self.importUISprites()
        self.createSlots()

        self.inventoryActive = False
        self.displayPlayerInventory = True
        self.timer = Timer(200)

        self.font = pg.font.Font("Font/PeaberryBase.ttf", 16)
        self.fontColor = (255, 255, 255)
        
        self.importUISprites()
            
    
    def initializeInventory(self):
        self.itemIndex = 0  
        self.itemSwapIndex = 0
        self.inventoryCapacity = 9

        self.defaultInventorySetup = [itemData["Hoe"],itemData["Axe"],itemData["WateringCan"],None,None,None,None,None,None]
        self.currentItems = self.defaultInventorySetup
        self.inventoryPos = (73, 495)


    def importUISprites(self):
        self.sprites = {}
        for items in itemData.keys():
            self.sprites[items] = {}
            self.sprites[items]["Default Sprite"] = loadSprite(itemData[items]["uiSprite"],slotScale).convert_alpha()
            self.sprites[items]["Selected Sprite"] = loadSprite(itemData[items]["uiSpriteSelected"],slotScale).convert_alpha()

        backGroundSize = (625,90)
        self.background = loadSprite(f"{uiPath}Inventory.png",backGroundSize).convert_alpha()

        self.selector = loadSprite(f"{uiPath}Slots/SlotSelector.png",slotScale).convert_alpha()
        self.selector2 = loadSprite(f"{uiPath}Slots/SlotSelector2.png",slotScale).convert_alpha()

    def createSlots(self):
        self.slotList = []

        width = self.inventoryPos[0] // self.inventoryCapacity
        offset = 37

        yPos = 514

        for index,item in enumerate(self.currentItems):
            inventoryWidth = 600  # less the borders
            increment = inventoryWidth // self.inventoryCapacity
            xPos = (index * increment) + (increment - width) + offset
            newSlots = InventorySlot((xPos, yPos), self.sprites[item["name"]] if item is not None else item, index)
            self.slotList.append(newSlots)

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
            if self.chestInventory.chestOpened:
                if self.itemIndex <= -37:
                    self.itemIndex = -36

            if self.itemIndex == -1:
                self.itemIndex = 0
        else:
            self.itemSwapIndex -= 1
            if self.chestInventory.chestOpened:
                if self.itemSwapIndex <= -37:
                    self.itemSwapIndex = -36
            if self.itemSwapIndex == -1:
                self.itemSwapIndex = 0

    def selectFromTop(self):
        if not self.swappingItems:
            self.itemIndex -= 9
            if self.itemIndex < -36:
                self.itemIndex = 0
        else:
            self.itemSwapIndex -= 9
            if self.itemSwapIndex < -36:
                self.itemSwapIndex = 0


    def selectFromBottom(self):
        if not self.swappingItems:
            self.itemIndex += 9
            if self.itemIndex > 8:
                self.itemIndex = -36
        else:
            self.itemSwapIndex += 9
            if self.itemSwapIndex >= 9:
                self.itemSwapIndex = -36

    def swapItems(self):
        chestItem = self.chestInventory.currentItemHolding
        chestSlot = self.chestInventory.itemSlots
        if self.itemSwapIndex >= 0:
            if self.itemIndex < 0:
                # chest to inventory
                self.swapItemData(False,self.currentItems,chestItem,self.slotList,chestSlot)
            else:
                # inventory to inventory
                self.swapItemData(True,self.currentItems,self.currentItems,self.slotList,self.slotList)
        else:
            if self.itemIndex < 0:
                # chest to chest
                self.swapItemData(True,chestItem,chestItem,chestSlot,chestSlot)
            else:
                # inventory to chests
                self.swapItemData(False,chestItem,self.currentItems,chestSlot,self.slotList)
        playSound("ItemSwap")


    def swapItemData(self,sameInventory,item1,item2,slot1,slot2):
        match sameInventory:
            case True:
                item1[self.itemSwapIndex],item2[self.itemIndex] = item2[self.itemIndex],item1[self.itemSwapIndex]
                slot1[self.itemSwapIndex].data, slot2[self.itemIndex].data = slot1[self.itemIndex].data,slot2[self.itemSwapIndex].data
                slot1[self.itemSwapIndex].sprite, slot2[self.itemIndex].sprite = slot1[self.itemIndex].sprite,slot2[self.itemSwapIndex].sprite
                slot1[self.itemSwapIndex].selectedSprite, slot2[self.itemIndex].selectedSprite = slot1[self.itemIndex].selectedSprite,slot2[self.itemSwapIndex].selectedSprite
                slot1[self.itemSwapIndex].stackNum, slot2[self.itemIndex].stackNum = slot1[self.itemIndex].stackNum,slot2[self.itemSwapIndex].stackNum
                self.itemIndex = self.itemSwapIndex
                return
            case False:
                item1[self.itemSwapIndex],item2[self.itemIndex] = item2[self.itemIndex],item1[self.itemSwapIndex]
                slot1[self.itemSwapIndex].data, slot2[self.itemIndex].data = slot2[self.itemIndex].data,slot1[self.itemSwapIndex].data
                slot1[self.itemSwapIndex].sprite, slot2[self.itemIndex].sprite = slot2[self.itemIndex].sprite,slot1[self.itemSwapIndex].sprite
                slot1[self.itemSwapIndex].selectedSprite, slot2[self.itemIndex].selectedSprite = slot2[self.itemIndex].selectedSprite,slot1[self.itemSwapIndex].selectedSprite
                slot1[self.itemSwapIndex].stackNum, slot2[self.itemIndex].stackNum = slot2[self.itemIndex].stackNum,slot1[self.itemSwapIndex].stackNum
                self.itemIndex = self.itemSwapIndex
                return

    def renderSelector(self):
        if self.swappingItems:
            self.swapItems()
            self.swappingItems = False
        else:
            self.itemSwapIndex = self.itemIndex
            self.swappingItems = True

    def selectingEquipmentSlot(self):
        if self.currentItems[self.itemIndex] is not None:
            usableItems = [equipmentItems,seedItems,animalFodders]
            for items in usableItems:
                if self.currentItems[self.itemIndex]["name"] in items:
                    return True
            return False


    def loadItems(self,index,items):
        self.currentItems[index] = itemData[items] if items is not None else None
        self.slotList[index].sprite = self.sprites[items]["Default Sprite"] if items is not None else self.slotList[index].defaultSprite
        self.slotList[index].selectedSprite = self.sprites[items]["Selected Sprite"] if items is not None else self.slotList[index].defaultSelectedSprite


    def loadSlotStacks(self,index,data):
        self.slotList[index].stackNum = data

    def AddItem(self,item):
        for slotIndex, itemSlots in enumerate(self.slotList):
            if self.currentItems[slotIndex] is not None:
                if self.currentItems[slotIndex]["name"] == item.data["name"]:
                    if itemSlots.stackNum < itemSlots.maximumStack:
                        itemSlots.stackNum += 1
                        return
            else:
                for i in range(slotIndex, self.inventoryCapacity):
                    if self.currentItems[i] is not None:
                        if self.currentItems[i]["name"] == item.data["name"]:
                            if self.slotList[i].stackNum < self.slotList[i].maximumStack:
                                self.slotList[i].stackNum += 1
                                return
                self.storeItemData(itemSlots, slotIndex, item)
                return

    def PurchaseItem(self,item):
        for slotIndex,itemSlots in enumerate(self.slotList):
            if self.currentItems[slotIndex] is not None:
                if self.currentItems[slotIndex]["name"] == item.data["name"]:
                    if itemSlots.stackNum < itemSlots.maximumStack:
                        itemSlots.stackNum += 1
                        return
            else:
                for i in range(slotIndex,self.inventoryCapacity):
                    if self.currentItems[i] is not None:
                        if self.currentItems[i]["name"] == item.data["name"]:
                            if self.slotList[i].stackNum < self.slotList[i].maximumStack:
                                self.slotList[i].stackNum += 1
                                return
                self.storeItemData(itemSlots, slotIndex, item)
                return

    def addItemStack(self,currentItems,item,slot):
        if currentItems["name"] == item.data["name"]:
            if slot.stackNum < slot.maximumStack:
                slot.stackNum += 1
                return


    def storeItemData(self,slot,slotIndex,item):
        newData = itemData[f"{item.data['name']}"]
        slot.data = newData
        self.currentItems[slotIndex] = newData
        slot.sprite = self.sprites[item.data["name"]]["Default Sprite"]
        slot.selectedSprite = self.sprites[item.data["name"]]["Selected Sprite"]
        return

    def removeItemData(self,slot):
        self.currentItems[self.itemIndex] = None
        slot.sprite = slot.defaultSprite
        slot.selectedSprite = slot.defaultSelectedSprite

    def decreaseItemStack(self):
        if self.slotList[self.itemIndex].stackNum > 1:
            self.slotList[self.itemIndex].stackNum -= 1
        else:
            self.removeItemData(self.slotList[self.itemIndex])


    def getCurrentSelectedItem(self):
        item = self.currentItems[self.itemIndex]["name"]  # if selecting Equipment
        return item

    def update(self,item):
        for itemIndex,items in enumerate(self.currentItems):
            if items is None:
                self.currentItems[itemIndex] = item
                self.slotList[itemIndex].sprite = item["uiSprite"]
                self.slotList[itemIndex].selectedSprite = item["uiSpriteSelected"]
                return
            else:
                pass

    def handleKeyboardInput(self):
        if not self.timer.activated:
            if EventHandler.pressingInteractKey():
                if self.inventoryActive:
                    self.renderSelector()
                    self.timer.activate()
                    self.chestInventory.updateIndex()
            if EventHandler.pressingInventoryLeftKey():
                self.selectFromLeft()
                playSound("Selection")
                self.chestInventory.updateIndex()
                self.timer.activate()
            if EventHandler.pressingInventoryRightKey():
                self.selectFromRight()
                playSound("Selection")
                self.chestInventory.updateIndex()
                self.timer.activate()
            if self.chestInventory.chestOpened:
                if EventHandler.pressingInventoryUpKey():
                    self.selectFromTop()
                    playSound("Selection")
                    self.chestInventory.updateIndex()
                    self.timer.activate()
                if EventHandler.pressingInventoryDownKey():
                    self.selectFromBottom()
                    playSound("Selection")
                    self.chestInventory.updateIndex()
                    self.timer.activate()


    def openInventory(self):
        self.resetIndexes()
        self.displayPlayerInventory = True

    def closeInventory(self):
        self.resetIndexes()
        self.displayPlayerInventory = False

    def resetIndexes(self):
        self.itemIndex = 0
        self.itemSwapIndex = 0

    def renderPlayerInventory(self):
        if not self.displayPlayerInventory: return

        self.handleKeyboardInput()
        self.timer.update()

        self.screen.blit(self.background,self.inventoryPos)

        for index,slots in enumerate(self.slotList):
            self.screen.blit(slots.sprite if self.itemIndex != slots.index else slots.selectedSprite,slots.pos)
            if slots.stackNum > 1:
                stackText = self.font.render(str(slots.stackNum),True,self.fontColor)
                self.screen.blit(stackText,slots.textRect.topright)

        if self.itemIndex >= 0:
            self.screen.blit(self.selector,self.slotList[self.itemIndex].pos)

        if self.swappingItems and self.itemSwapIndex >= 0:
            self.screen.blit(self.selector2, self.slotList[self.itemSwapIndex].pos)









