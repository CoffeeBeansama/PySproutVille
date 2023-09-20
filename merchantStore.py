from support import *
from settings import *
from timer import Timer
from sound import playSound

class MerchantStore:
    def __init__(self,player,action,chickenBought,cowBought,openInventory):
        self.screen = pg.display.get_surface()

        self.player = player
        self.playerCoinPos = (320,490)
        backGroundSpritePath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Merchant/BackGround.png"
        self.backGroundSpiteSize = (450,500)
        self.backGroundSprite = loadSprite(backGroundSpritePath,self.backGroundSpiteSize).convert_alpha()
        self.backGroundSpritePos = (160,50)
        self.backGroundSpriteRect = self.backGroundSprite.get_rect(topleft=self.backGroundSpritePos)
        self.backGroundLength = self.backGroundSpiteSize[1]

        self.itemStoreSpriteSize = (35,35)
        self.font = pg.font.Font("Font/PeaberryBase.ttf", 32)
        self.fontColor = (144, 98, 93)

        self.renderedItems = []

        self.itemsAvailable = {
            "Wheat": {
                "name": "Wheat",
                "storeCost": 1,
                "StoreSprite": loadSprite(f"{spritePath}/Plants/Wheat/5.png",self.itemStoreSpriteSize),
            },
            "Tomato": {
                "name": "Tomato",
                "storeCost": 3,
                "StoreSprite": loadSprite(f"{spritePath}/Plants/Tomato/5.png", self.itemStoreSpriteSize),
            },
            "Chicken": {
                "name": "Chicken",
                "storeCost": 60,
                "StoreSprite": loadSprite("Sprites/Chicken/Idle/0.png",self.itemStoreSpriteSize),
            },
            "Cow": {
                "name": "Cow",
                "storeCost": 90,
                "StoreSprite": loadSprite("Sprites/Cow/Idle/0.png",(38,38)),
            },
        }

        self.itemSetup = [self.itemsAvailable["Wheat"], self.itemsAvailable["Tomato"], self.itemsAvailable["Chicken"], self.itemsAvailable["Cow"]]

        self.slotPosX = 195

        self.padding = 1.3
        self.lengthDistance = self.backGroundSpritePos[1] // len(self.itemSetup) + 1

        self.itemSlots = None
        self.createItems()

        self.closeMenu = action

        self.itemIndex = 0

        self.timer = Timer(300)
        self.allowedToPurchase = False
        self.displayMerchandise = False

        self.chickenBought = chickenBought
        self.cowBought = cowBought
        self.openInventory = openInventory

    def createItems(self):
        for index,items in enumerate(self.itemSetup):
            lengthIncrement = self.backGroundLength // len(self.itemSetup)
            y = (index * lengthIncrement // self.padding) + (lengthIncrement - self.lengthDistance)

            Item = ItemSlot((self.slotPosX,y),items,index)
            self.renderedItems.append(Item)

    def purchaseItem(self):
        canPurchase = self.player.coins >= self.renderedItems[self.itemIndex].itemCost
        if canPurchase:
            if self.renderedItems[self.itemIndex].itemName in seedItems:
                self.player.inventory.PurchaseItem(self.renderedItems[self.itemIndex])
            if self.renderedItems[self.itemIndex].itemName == "Chicken":
                self.chickenBought()
            if self.renderedItems[self.itemIndex].itemName == "Cow":
                self.cowBought()
            self.player.coins -= self.renderedItems[self.itemIndex].itemCost
            playSound("Purchase")
        else:
            playSound("No Cash")

        return

    def getPlayerInputs(self):
        if self.allowedToPurchase:
            keys = pg.key.get_pressed()

            if self.itemIndex >= len(self.itemSetup):
                self.itemIndex = 0
            elif self.itemIndex < 0:
                self.itemIndex = len(self.itemSetup) - 1

            if not self.timer.activated:
                if keys[pg.K_w]:
                    self.itemIndex -= 1
                    self.timer.activate()
                    playSound("Selection")
                if keys[pg.K_s]:
                    self.itemIndex += 1
                    self.timer.activate()
                    playSound("Selection")
                if keys[pg.K_ESCAPE]:
                    self.closeMenu()
                    self.displayMerchandise = False
                    self.allowedToPurchase = False
                    self.timer.activate()
                    playSound("CloseInventory")
                    self.openInventory()

                if keys[pg.K_SPACE]:
                    self.purchaseItem()
                    self.timer.activate()



    def display(self):
        if self.displayMerchandise:
            self.timer.update()
            self.getPlayerInputs()
            if not self.timer.activated and not self.allowedToPurchase:
                self.allowedToPurchase = True
                self.timer.activate()

            self.screen.blit(self.backGroundSprite,self.backGroundSpriteRect)

            if len(self.renderedItems) > 0:
                for items in self.renderedItems:

                    self.screen.blit(items.sprite if self.itemIndex != items.index else items.selectedSprite,items.pos)

                    self.screen.blit(items.itemSprite, (items.pos[0] + 30, items.pos[1] + 15))

                    itemName = self.font.render(str(items.itemName), True, self.fontColor)
                    self.screen.blit(itemName, (items.pos[0] + 80,items.pos[1] + 15))

                    itemCost = self.font.render(str(items.itemCost), True, self.fontColor)
                    self.screen.blit(itemCost,(items.pos[0] + 315, items.pos[1] + 16))

            playerCoin = self.font.render(str(f"Cash: {self.player.coins}"),True,self.fontColor)
            self.screen.blit(playerCoin,self.playerCoinPos)

class ItemSlot:
    def __init__(self,pos,item,index):

        self.pos = pos
        self.index = index

        self.data = item
        self.itemName = item["name"]
        self.itemCost = item["storeCost"]
        self.itemSprite = item["StoreSprite"].convert_alpha()

        spritePath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Merchant/ItemSlot.png"
        selectedSpritePath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Merchant/ItemSlotSelected.png"

        self.slotSize = (375,60)
        self.sprite = loadSprite(spritePath,self.slotSize).convert_alpha()
        self.selectedSprite = loadSprite(selectedSpritePath,self.slotSize).convert_alpha()