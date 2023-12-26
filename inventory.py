import pygame as pg
from settings import uiPath,slotScale,itemData,animalFodders,equipmentItems,seedItems,uiSprites
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

class Inventory:
    def __init__(self,unPauseGame):
        self.screen = pg.display.get_surface()
    
        self.swappingItems = False

        self.sellableItems = []

        self.importUISprites()
                
        self.initializePlayerInventory()
        self.initializeChestInventory() 


        self.itemIndex = 0  
        self.itemSwapIndex = 0
        
        self.chestItemIndex = self.itemIndex + len(self.chestInventoryDefaultItems)
        self.chestItemSwapIndex = self.itemSwapIndex + len(self.chestInventoryDefaultItems)

        self.createPlayerInventorySlots()
        self.createChestInventorySlots()

        self.inventoryActive = False
        self.displayPlayerInventory = True
        self.timer = Timer(200)

        self.font = pg.font.Font("Font/PeaberryBase.ttf", 16)
        self.fontColor = (255, 255, 255)

        self.unPauseGame = unPauseGame

    def initializePlayerInventory(self):
        self.playerInventoryPos = (73, 495)
        self.playerInventoryCapacity = 9

        self.playerInventoryDefaultItems = [itemData["Hoe"],itemData["Axe"],itemData["WateringCan"],None,None,None,None,None,None]
        self.playerCurrentItems = self.playerInventoryDefaultItems



    def initializeChestInventory(self):
        self.chestInventoryPos = (73, 130)

        self.chestOpened = False

        chestCapacity = 36
        self.chestInventoryDefaultItems = [None for i in range(chestCapacity)]

        self.chestCurrentItems = self.chestInventoryDefaultItems 

    def importUISprites(self):
        self.sprites = {}
        for items in itemData.keys():
            self.sprites[items] = {}
            self.sprites[items]["Default Sprite"] = loadSprite(itemData[items]["uiSprite"],slotScale).convert_alpha()
            self.sprites[items]["Selected Sprite"] = loadSprite(itemData[items]["uiSpriteSelected"],slotScale).convert_alpha()

        playerInventoryBackgroundSize = (625,90)
        self.playerInventoryBackground = loadSprite(f"{uiPath}Inventory.png",playerInventoryBackgroundSize).convert_alpha()

        self.selector = loadSprite(f"{uiPath}Slots/SlotSelector.png",slotScale).convert_alpha()
        self.selector2 = loadSprite(f"{uiPath}Slots/SlotSelector2.png",slotScale).convert_alpha()

        chestBackgroundSize = (625,350)
        self.chestBackgroundImage = loadSprite(uiSprites["ChestBackground"],chestBackgroundSize).convert_alpha()

    def createPlayerInventorySlots(self):
        self.playerItemSlotList = []

        width = self.playerInventoryPos[0] // self.playerInventoryCapacity
        offset = 37

        yPos = 514

        for index,item in enumerate(self.playerCurrentItems):
            inventoryWidth = 600  # less the borders
            increment = inventoryWidth // self.playerInventoryCapacity
            xPos = (index * increment) + (increment - width) + offset
            newSlots = InventorySlot((xPos, yPos), self.sprites[item["name"]] if item is not None else item, index)
            self.playerItemSlotList.append(newSlots)

    def createChestInventorySlots(self):
        self.chestItemSlots = {}

        rows = 4
        columns = 9

        width = self.chestInventoryPos[0] // rows
        offset = 47
        yPos = 170

        slotID = -self.chestItemIndex

        for i in range(rows):
            for j in range(columns):
                inventoryWidth = 600 # less the borders
                increment = inventoryWidth // columns
                xPos = (j * increment) + (increment - width) + offset
                newSlots = InventorySlot((xPos, yPos), None, slotID)
                self.chestItemSlots[slotID] = newSlots
                slotID += 1
            yPos += 70


    def displayChestInventory(self):
        self.chestOpened = True
        playSound("Chest")

    def closeChestInventory(self):
        self.chestOpened = False
        self.swappingItems = False
        self.unPauseGame()
        self.resetIndexes()

    def loadChestSlotsData(self):
        for index,slots in enumerate(self.chestItemSlots.values()):
            item = self.chestCurrentItems[index]
            
            if item is not None:
                slots.sprite = self.sprites[item["name"]]["Default Sprite"]
                slots.selectedSprite = self.sprites[item["name"]]["Selected Sprite"]


    def loadChestSlotsStack(self,index,stack):
        self.chestItemSlots[index].stackNum = stack
        
    def loadChestCurrentItems(self,index,item):
        if item is not None:
            self.chestCurrentItems[index] = itemData[item]            

    def swapItems(self):
        chestItem = self.chestCurrentItems
        chestSlot = self.chestItemSlots
        if self.itemSwapIndex >= 0:
            if self.itemIndex < 0:
                # chest to inventory
                self.swapItemData(False,self.playerCurrentItems,chestItem,self.playerItemSlotList,chestSlot)
            else:
                # inventory to inventory
                self.swapItemData(True,self.playerCurrentItems,self.playerCurrentItems,self.playerItemSlotList,self.playerItemSlotList)
        else:
            if self.itemIndex < 0:
                # chest to chest
                self.swapItemData(True,chestItem,chestItem,chestSlot,chestSlot)
            else:
                # inventory to chests
                self.swapItemData(False,chestItem,self.playerCurrentItems,chestSlot,self.playerItemSlotList)
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
        if self.playerCurrentItems[self.itemIndex] is not None:
            usableItems = [equipmentItems,seedItems,animalFodders]
            for items in usableItems:
                if self.playerCurrentItems[self.itemIndex]["name"] in items:
                    return True
            return False


    def loadPlayerInventoryItems(self,index,items):
        self.playerCurrentItems[index] = itemData[items] if items is not None else None
        self.playerItemSlotList[index].sprite = self.sprites[items]["Default Sprite"] if items is not None else self.playerItemSlotList[index].defaultSprite
        self.playerItemSlotList[index].selectedSprite = self.sprites[items]["Selected Sprite"] if items is not None else self.playerItemSlotList[index].defaultSelectedSprite

    def loadPlayerInventorySlotStacks(self,index,data):
        self.playerItemSlotList[index].stackNum = data

    def AddItem(self,item):
        for slotIndex, itemSlots in enumerate(self.playerItemSlotList):
            if self.playerCurrentItems[slotIndex] is not None:
                if self.playerCurrentItems[slotIndex]["name"] == item.data["name"]:
                    if itemSlots.stackNum < itemSlots.maximumStack:
                        itemSlots.stackNum += 1
                        return
            else:
                for i in range(slotIndex, self.playerInventoryCapacity):
                    if self.playerCurrentItems[i] is not None:
                        if self.playerCurrentItems[i]["name"] == item.data["name"]:
                            if self.playerItemSlotList[i].stackNum < self.playerItemSlotList[i].maximumStack:
                                self.playerItemSlotList[i].stackNum += 1
                                return
                self.storeItemData(itemSlots, slotIndex, item)
                return

    def PurchaseItem(self,item):
        for slotIndex,itemSlots in enumerate(self.playerItemSlotList):
            if self.playerCurrentItems[slotIndex] is not None:
                if self.playerCurrentItems[slotIndex]["name"] == item.data["name"]:
                    if itemSlots.stackNum < itemSlots.maximumStack:
                        itemSlots.stackNum += 1
                        return
            else:
                for i in range(slotIndex,self.playerInventoryCapacity):
                    if self.playerCurrentItems[i] is not None:
                        if self.playerCurrentItems[i]["name"] == item.data["name"]:
                            if self.playerItemSlotList[i].stackNum < self.playerItemSlotList[i].maximumStack:
                                self.playerItemSlotList[i].stackNum += 1
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
        self.playerCurrentItems[slotIndex] = newData
        slot.sprite = self.sprites[item.data["name"]]["Default Sprite"]
        slot.selectedSprite = self.sprites[item.data["name"]]["Selected Sprite"]
        return

    def removeItemData(self,slot):
        self.playerCurrentItems[self.itemIndex] = None
        slot.sprite = slot.defaultSprite
        slot.selectedSprite = slot.defaultSelectedSprite

    def decreaseItemStack(self):
        if self.playerItemSlotList[self.itemIndex].stackNum > 1:
            self.playerItemSlotList[self.itemIndex].stackNum -= 1
        else:
            self.removeItemData(self.playerItemSlotList[self.itemIndex])


    def getCurrentSelectedItem(self):
        item = self.playerCurrentItems[self.itemIndex]["name"]  # if selecting Equipment
        return item

    
    def checkOutOfIndex(self):    

        if not self.chestOpened:
           if self.itemIndex < 0:
              self.itemIndex = len(self.playerCurrentItems) -1
              return

           if self.itemIndex >= len(self.playerCurrentItems):
              self.itemIndex = 0
              return
        
        maxIndex = -36
        
        if self.itemIndex < maxIndex:
           self.itemIndex = 0
        
        if self.itemIndex > len(self.playerCurrentItems) -1:
           self.itemIndex = maxIndex
        
        if self.itemSwapIndex < maxIndex:
           self.itemSwapIndex = 0

        if self.itemSwapIndex > len(self.playerCurrentItems) -1:   
           self.itemSwapIndex = maxIndex 

    def handleKeyboardInput(self):
        
        if not self.timer.activated:
            if EventHandler.pressingInteractKey() and self.chestOpened:
                self.inventoryActive = True        
                self.renderSelector()
                self.timer.activate()
            
            if EventHandler.pressingInventoryKey() and not self.chestOpened:

                if self.inventoryActive:
                   self.inventoryActive = False
                else:
                    self.inventoryActive = True

                self.timer.activate()

            if EventHandler.pressingLeftKey() and self.inventoryActive:
                if not self.swappingItems:
                   self.itemIndex -= 1
                else:
                    self.itemSwapIndex -= 1
                                
                playSound("Selection")
                self.timer.activate()

            if EventHandler.pressingRightKey() and self.inventoryActive:
               if not self.swappingItems:
                  self.itemIndex += 1
               else:
                  self.itemSwapIndex += 1
    
               playSound("Selection")
               self.timer.activate()

            if EventHandler.pressingUpKey() and self.chestOpened:
                if not self.swappingItems:
                   self.itemIndex -= 9
                else:
                   self.itemSwapIndex -= 9

                playSound("Selection")
                self.timer.activate()

            if EventHandler.pressingDownKey() and self.chestOpened:
               if not self.swappingItems:
                  self.itemIndex += 9
               else:
                  self.itemSwapIndex += 9
                    
               playSound("Selection")
               self.timer.activate()

            if EventHandler.pressingCloseKey(): 
               if self.chestOpened:
                  self.closeChestInventory()
               self.timer.activate()

        self.checkOutOfIndex()


    def resetIndexes(self):
        self.itemIndex = 0
        self.itemSwapIndex = 0

    def openInventory(self):
        self.resetIndexes()
        self.displayPlayerInventory = True

    def closeInventory(self):
        self.resetIndexes()
        self.displayPlayerInventory = False

    def renderChestInventory(self):
        if not self.chestOpened: return
        
        self.chestItemIndex = self.itemIndex
        self.chestItemSwapIndex = self.itemSwapIndex

        self.screen.blit(self.chestBackgroundImage, self.chestInventoryPos)
        
        for keyIndex,slots in enumerate(self.chestItemSlots.values()):
            self.screen.blit(slots.sprite if self.chestItemIndex != slots.index else slots.selectedSprite,slots.pos)
            if slots.stackNum > 1:
                stackText = self.font.render(str(slots.stackNum),True,self.fontColor)
                self.screen.blit(stackText,slots.textRect.topright)

        if self.chestItemIndex < 0:
            self.screen.blit(self.selector,self.chestItemSlots[self.chestItemIndex].pos)

        if self.swappingItems and self.chestItemSwapIndex < 0:
            self.screen.blit(self.selector2, self.chestItemSlots[self.chestItemSwapIndex].pos)

        

    def renderPlayerInventory(self):
        if not self.displayPlayerInventory: return
        
        self.screen.blit(self.playerInventoryBackground,self.playerInventoryPos)

        for index,slots in enumerate(self.playerItemSlotList):
            self.screen.blit(slots.sprite if self.itemIndex != slots.index else slots.selectedSprite,slots.pos)
            if slots.stackNum > 1:
                stackText = self.font.render(str(slots.stackNum),True,self.fontColor)
                self.screen.blit(stackText,slots.textRect.topright)
        
        if self.itemIndex >= 0 and self.inventoryActive:
            self.screen.blit(self.selector,self.playerItemSlotList[self.itemIndex].pos)

        if self.swappingItems and self.itemSwapIndex >= 0:
            self.screen.blit(self.selector2, self.playerItemSlotList[self.itemSwapIndex].pos)

    def update(self):
        self.timer.update()
        self.handleKeyboardInput()         
        self.renderPlayerInventory()
        self.renderChestInventory()
        







