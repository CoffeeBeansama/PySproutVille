import pygame as pg
from settings import *
from inventory import InventorySlot
from timer import Timer
from sound import playSound
from support import loadSprite


class ChestInventory:
    def __init__(self,playerInventory,inventoryClosed):
        self.screen = pg.display.get_surface()
        self.playerInventory = playerInventory
        self.inventoryPos = (73, 130)

        self.backGroundImage = uiSprites["ChestBackground"].convert_alpha()

        self.chestOpened = False
        self.inventoryClosed = inventoryClosed

        self.selectorSprite = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/SlotSelector.png"
        self.selectorSprite2 = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/SlotSelector2.png"

        self.selector = pg.transform.scale(pg.image.load(self.selectorSprite), slotScale).convert_alpha()
        self.selector2 = pg.transform.scale(pg.image.load(self.selectorSprite2), slotScale).convert_alpha()

        self.importUISprites()

        self.initializeInventory()
        
        self.createSlots()

        self.font = pg.font.Font("Font/PeaberryBase.ttf", 16)
        self.fontColor = (255, 255, 255)


    def importUISprites(self):
        self.sprites = {}
        
        for items in itemData.keys():
            self.sprites[items] = {}
            self.sprites[items]["Default Sprite"] = loadSprite(itemData[items]["uiSprite"],slotScale).convert_alpha()
            self.sprites[items]["Selected Sprite"] = loadSprite(itemData[items]["uiSpriteSelected"],slotScale).convert_alpha()
    
    def initializeInventory(self):
        capacity = 36
        self.defaultInventorySetup = [None for i in range(capacity)]

        self.currentItemHolding = self.defaultInventorySetup 

        self.itemIndex = self.playerInventory.itemIndex + len(self.defaultInventorySetup)
        self.itemSwapIndex = self.playerInventory.itemSwapIndex + len(self.defaultInventorySetup)
        

    def createSlots(self):
        self.itemSlots = {}

        rows = 4
        columns = 9
        
        width = self.inventoryPos[0] // rows
        offset = 47
        yPos = 170

        slotID = -self.itemIndex

        for i in range(rows):
            for j in range(columns):
                inventoryWidth = 600 # less the borders
                increment = inventoryWidth // columns
                xPos = (j * increment) + (increment - width) + offset
                newSlots = InventorySlot((xPos, yPos), None, rows)
                self.itemSlots[slotID] = newSlots
                slotID += 1
            yPos += 70


    def displayInventory(self):
        self.chestOpened = True
        playSound("Chest")


    def closeInventory(self):
        self.chestOpened = False
        self.playerInventory.resetIndexes()
        self.updateIndex()
        self.inventoryClosed()

    def loadSlotsData(self):
        for index,slots in enumerate(self.itemSlots.values()):
            item = self.currentItemHolding[index]
            
            if item is not None:
                slots.sprite = self.sprites[item["name"]]["Default Sprite"]
                slots.selectedSprite = self.sprites[item["name"]]["Selected Sprite"]

    def loadSlotsStack(self,index,stack):
        self.itemSlots[index].stackNum = stack


    def updateIndex(self):
        self.itemIndex = self.playerInventory.itemIndex
        self.itemSwapIndex = self.playerInventory.itemSwapIndex

    def loadCurrentItems(self,index,item):
        if item is not None:
            self.currentItemHolding[index] = itemData[item]

    def display(self):
        if not self.chestOpened: return

        self.screen.blit(self.backGroundImage, self.inventoryPos)
        
        for keyIndex,slots in enumerate(self.itemSlots.values()):
            self.screen.blit(slots.sprite if self.playerInventory.itemIndex != slots.index else slots.selectedSprite,slots.pos)
            if slots.stackNum > 1:
                stackText = self.font.render(str(slots.stackNum),True,self.fontColor)
                self.screen.blit(stackText,slots.textRect.topright)

        if self.itemIndex < 0:
            self.screen.blit(self.selector,self.itemSlots[self.itemIndex].pos)

        if self.playerInventory.swappingItems and self.itemSwapIndex < 0:
            self.screen.blit(self.selector2, self.itemSlots[self.itemSwapIndex].pos)

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.updateIndex()
            self.closeInventory()


