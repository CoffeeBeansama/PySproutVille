import pygame as pg
from settings import *
from inventory import InventorySlot
from timer import Timer

class ChestInventory:
    def __init__(self,playerInventory,inventoryClosed):
        self.screen = pg.display.get_surface()
        self.playerInventory = playerInventory
        self.inventoryPos = (73, 130)
        self.backGroundImage = uiSprites["ChestBackground"].convert_alpha()

        self.slotPosY = 170
        self.chestOpened = False
        self.inventoryClosed = inventoryClosed

        self.selectorSprite = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/SlotSelector.png"
        self.selectorSprite2 = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/SlotSelector2.png"

        self.selector = pg.transform.scale(pg.image.load(self.selectorSprite), slotScale).convert_alpha()
        self.selector2 = pg.transform.scale(pg.image.load(self.selectorSprite2), slotScale).convert_alpha()

        self.rowCapacity = 4

        self.maxSlotPerRow = 9
        self.width = self.inventoryPos[0] // self.rowCapacity

        self.defaultInventorySetup = [None, None, None, None, None, None, None, None, None,
                                      None, None, None, None, None, None, None, None, None,
                                      None, None, None, None, None, None, None, None, None,
                                      None, None, None, None, None, None, None, None, None,
                                      ]

        self.currentItemHolding = self.defaultInventorySetup
        self.itemIndex = self.playerInventory.itemIndex + len(self.defaultInventorySetup)
        self.itemSwapIndex = self.playerInventory.itemSwapIndex + len(self.defaultInventorySetup)
        self.rowSlot = -self.itemIndex
        self.slotList = []
        self.createSlots()

    def createSlots(self):
        for i in range(self.rowCapacity):
            for j in range(self.maxSlotPerRow):
                inventoryWidth = 600 # less the borders
                increment = inventoryWidth // self.maxSlotPerRow
                left = (j * increment) + (increment - self.width) + 47
                newSlots = InventorySlot((left, self.slotPosY), self.defaultInventorySetup[j], self.rowSlot)
                self.slotList.append(newSlots)

                self.rowSlot +=1

            self.slotPosY += 70
    def displayInventory(self):
        self.chestOpened = True
        self.playerInventory.renderPlayerInventory()



    def closeInventory(self):
        self.chestOpened = False
        self.inventoryClosed()

    def display(self):
        if not self.chestOpened: return


        self.screen.blit(self.backGroundImage, self.inventoryPos)

        for index,slots in enumerate(self.slotList):
            self.screen.blit(slots.sprite.convert_alpha() if self.playerInventory.itemIndex != slots.index else slots.selectedSprite.convert_alpha(),slots.pos)

        self.itemIndex = self.playerInventory.itemIndex + len(self.currentItemHolding)
        self.itemSwapIndex = self.playerInventory.itemIndex + len(self.currentItemHolding)



        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.closeInventory()


