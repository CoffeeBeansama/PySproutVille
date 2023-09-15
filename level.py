from settings import *
from tile import *
from player import Player
from inventory import *
from debug import debug
from items import *
from plants import *
from support import import_csv_layout
from equipment import Equipment
from timeManager import TimeManager
from objects import *
from tree import *
from ui import *
from npc import *
from merchantStore import MerchantStore
from dialogueManager import DialogueSystem
from saveload import SaveLoadSystem
from chestInventory import ChestInventory
from inventory import PlayerInventory


class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_canvas = pg.display.get_surface()
        self.half_width = self.display_canvas.get_size()[0] // 2
        self.half_height = self.display_canvas.get_size()[1] // 2

        self.groundSprite = pg.image.load("Sprites/level.png").convert()

        self.groundRect = self.groundSprite.get_rect(topleft=(0, 0))


        self.internalSurfaceSize = (500, 500)
        self.internalSurface = pg.Surface(self.internalSurfaceSize, pg.SRCALPHA)
        self.internalRect = self.internalSurface.get_rect(center=(self.half_width, self.half_height))
        self.offset_rect = None
        self.zoomInSize = (1100, 1100)

        self.internalOffset = pg.math.Vector2()
        self.internalOffset.x = self.internalSurfaceSize[0] // 2 - self.half_width
        self.internalOffset.y = self.internalSurfaceSize[1] // 2 - self.half_height

        self.offset = pg.math.Vector2()

    def custom_draw(self, player):
        # getting the offset  for camera
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        self.internalSurface.fill("black")

        floor_offset_pos = self.groundRect.topleft - self.offset + self.internalOffset
        self.internalSurface.blit(self.groundSprite, floor_offset_pos)


        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery - 15 if sprite.type in OverlapTiles else sprite.rect.centery):
            self.offset_rect = sprite.rect.topleft - self.offset + self.internalOffset

            self.internalSurface.blit(sprite.image, self.offset_rect)


        scaledSurface = pg.transform.scale(self.internalSurface, self.zoomInSize)
        scaledRect = scaledSurface.get_rect(center=(self.half_width, self.half_height))
        self.display_canvas.blit(scaledSurface, scaledRect)



class Level:
    def __init__(self, main):

        self.main = main
        self.player = None
        self.screen = pg.display.get_surface()

        self.gamePaused = False
        self.displayMerchantStore = False
        self.currentEquipment = None

        self.visibleSprites = CameraGroup()
        self.collisionSprites = pg.sprite.Group()
        self.equipmentSprites = pg.sprite.Group()
        self.soilTileSprites = pg.sprite.Group()
        self.woodTileSprites = pg.sprite.Group()
        self.pickAbleItemSprites = pg.sprite.Group()
        self.playerSprite = pg.sprite.Group()
        self.interactableSprites = pg.sprite.Group()
        self.animalCollider = pg.sprite.Group()

        self.timer = Timer(200)
        self.timeManager = TimeManager(None,self.updateEntities)

        self.PlantedSoilTileList = []
        self.plantTile = None
        self.plantList = []
        self.appleList = []
        self.animalsList = []
        self.soilList = []

        self.treeList = []

        self.soilIndex = 0
        self.appleIndex = 0


        self.coinList = []

        self.createMap()


        self.saveload = SaveLoadSystem(".data", "savedata")
        self.playerInventory = PlayerInventory(None)
        self.player = Player(testSprites["Player"],[self.visibleSprites,self.playerSprite],self.collisionSprites,self.createEquipmentTile,self.interactableSprites,self.pickAbleItemSprites,self.timeManager,None,self.saveGameState,self.loadGameState,self.playerInventory)
        self.chestInventory = ChestInventory(self.playerInventory,self.closeChestInventory)
        self.playerInventory.chestInventory = self.chestInventory


        self.gameState = {
            "Player": self.player.data,
            "Plants": {},
            "Apples": {},
            "Soil": {},
            "PickableItems": {},
            "Animals": {},
            "ItemChest": {},

        }

        self.defaultGameState = {
            "Player": self.player.defaultData,
            "Plants": {},
            "Apples": {},
            "Soil": {},
            "PickableItems": {},
            "Animals": {},
            "ItemChest": {}

        }

        self.loadGameState()

        self.merchantStore = MerchantStore(self.player, self.closeMerchantStore,self.createChickenInstance,self.createCowInstance)
        self.dialogueSystem = DialogueSystem(self.player, None, self.openMerchantStore)

        self.getPlayerData([self.timeManager,
                              self.bedTile])

        self.ui = Ui(self.player,self.displayMerchantStore)
        self.dynamicUi = self.ui.dynamicUi
        self.merchant.dialogueSystem,dynamicUi = self.dialogueSystem,self.dynamicUi
        self.dialogueSystem.dynamicUi = self.dynamicUi
        self.player.dialogueSystem = self.dialogueSystem

        self.chickenSpawnPoint = (1206, 938)
        self.cowSpawnPoint = (1130, 1378)



    def createMap(self):

        mapLayouts = {
            "boundary": import_csv_layout("Map/wall.csv"),
            "soilTile": import_csv_layout("Map/plantableGrounds_Plantable Ground.csv"),
            "InteractableObjects": import_csv_layout('Map/InteractableObjects.csv'),
            "Tree Trunks": import_csv_layout('Map/Tree trunks.csv'),
            "Animal Collider": import_csv_layout('Map/AnimalCollision.csv'),
            "Fence": import_csv_layout('Map/Fences.csv'),

        }
        for style, layout in mapLayouts.items():
            for rowIndex, row in enumerate(layout):
                for columnIndex, column in enumerate(row):

                    if column != "-1":
                        x = columnIndex * tileSize
                        y = rowIndex * tileSize

                        if style == "boundary":
                            Tile(testSprites["Player"], (x, y), [self.collisionSprites])

                        if style == "soilTile":
                            self.soilList.append(SoilTile((x, y), [self.visibleSprites,self.soilTileSprites],False,self.soilIndex))
                            self.soilIndex += 1

                        if style == "InteractableObjects":
                            if column == "Bed":
                                self.bedTile = Bed([self.interactableSprites], None)
                            if column == "Chest":
                                self.chestObject = Chest((x, y - tileSize),[self.visibleSprites,self.collisionSprites],self.player,self.interactableSprites,self.openChestInventory)
                        if style == "Tree Trunks":
                            self.treeList.append(Tree((x,y),[self.collisionSprites,self.woodTileSprites],self.visibleSprites,self.pickAbleItemSprites,self.appleList,self.appleIndex))
                            self.appleIndex += 1

                        if style == "Animal Collider":
                            Fence(testSprites["Player"], (x, y), [self.animalCollider])

                        if style == "Fence":
                            Fence(testSprites["Player"], (x, y), [self.collisionSprites])

        self.merchant = Merchant([self.visibleSprites,self.collisionSprites],self.interactableSprites,None,None)



    def DecreasePlayerLives(self):
        self.player.lives -= 1
        self.dynamicUi.decreasePlayerHeart()

    def pauseGame(self):
        if not self.gamePaused:
            self.gamePaused = True

    def unpauseGame(self):
        if self.gamePaused:
            self.gamePaused = False

    def getPlayerData(self,object):
        for classes in object:
            classes.player = self.player


    def plantGrowth(self):
        for soil in self.PlantedSoilTileList:
            soil.update()

    def createEquipmentTile(self):
        self.currentEquipment = Equipment([self.equipmentSprites], self.player)
        return

    def updateEntities(self):
        for plants in self.plantList:
            plants.NextPhase()
        for animals in self.animalsList:
            animals.produce()

        for apples in self.appleList[::-1]:
            if apples.alive():
                apples.growth()
            else:
                self.appleList.remove(apples)


    def playerPickUpItems(self):
        for itemIndex, items in enumerate(self.pickAbleItemSprites):
            if items.hitbox.colliderect(self.player.hitbox):
                items.pickUpItem(self.plantList,self.player,self.visibleSprites,self.coinList)


    def equipmentTileCollisionLogic(self):
        inventory = self.player.inventory
        for sprites in self.equipmentSprites:
            soilTileCollided = pg.sprite.spritecollide(sprites, self.soilTileSprites, False)
            woodTileCollided = pg.sprite.spritecollide(sprites, self.woodTileSprites, False)
            itemName = inventory.currentItems[inventory.itemIndex]["name"]
            if soilTileCollided:

                if itemName == "Hoe":
                    soilTileCollided[0].tiltSoil()
                elif itemName == "WateringCan":
                    soilTileCollided[0].waterSoil()
                elif itemName in seedItems:
                    self.seedPlantTile(soilTileCollided[0],inventory.currentItems[inventory.itemIndex])

            if woodTileCollided:
                if itemName == "Axe":
                    woodTileCollided[0].chopped()

        if self.currentEquipment is not None:
            self.currentEquipment.kill()
            return


    def seedPlantTile(self, soilTile,data):
        if soilTile.planted: return
        if soilTile.currentState == "Tilted" or soilTile.currentState == "Watered":
            plantTile = PlantTile(soilTile.rect.topleft,[self.visibleSprites],data,self.pickAbleItemSprites,self.timeManager,self.soilTileSprites)
            soilTile.currentPlant = plantTile
            self.plantList.append(plantTile)
            self.PlantedSoilTileList.append(soilTile)
            soilTile.planted = True


    def updateCoinList(self):
        if len(self.coinList) > 0:
            for coins in self.coinList:
                coins.update(self.coinList)

    def openChestInventory(self):
        self.chestInventory.displayInventory()
        self.displayPlayerInventory = True
        self.playerInventory.inventoryActive = True
        self.pauseGame()

    def closeChestInventory(self):
        self.displayPlayerInventory = False
        self.playerInventory.inventoryActive = False
        self.unpauseGame()

    def openMerchantStore(self):
        self.displayMerchantStore = True
        self.merchantStore.displayMerchandise = True
        self.pauseGame()

    def closeMerchantStore(self):
        self.unpauseGame()
        self.displayMerchantStore = False

    def createChickenInstance(self):
        newChicken = Chicken("Chicken",self.chickenSpawnPoint, [self.visibleSprites], self.animalCollider, self.pickAbleItemSprites)
        self.animalsList.append(newChicken)

    def createCowInstance(self):
        newCow = Cow("Cow", self.cowSpawnPoint, [self.visibleSprites], self.animalCollider, self.pickAbleItemSprites)
        self.animalsList.append(newCow)

    def savePlayerData(self):
        player = self.player
        player.currentItemsHolding.clear()
        player.data["Position"] = player.hitbox.center
        player.data["Coins"] = player.coins
        for items in player.inventory.currentItems:
            player.currentItemsHolding.append(items["name"] if items is not None else None)
            player.data["Items"] = player.currentItemsHolding
        self.gameState["Player"] = player.data


    def saveItemChestData(self):
        itemChest = self.chestInventory
        for index,items in enumerate(itemChest.currentItemHolding):
            self.gameState["ItemChest"][index] = items["name"] if items is not None else None


    def savePlantData(self):
        for index,plants in enumerate(self.plantList):
            if plants.type == "Plants":
                savedPlant = self.gameState["Plants"][f"{plants.type}{index}"] = {}
                savedPlant["Name"] = plants.data["name"]
                savedPlant["Position"] = plants.rect.topleft
                savedPlant["CurrentPhase"] = plants.currentPhase

        for index,apples in enumerate(self.appleList):
            if apples.type == "Apple":
                savedApple = self.gameState["Apples"][f"{apples.type}{index}"] = {}
                savedApple["Name"] = apples.data["name"]
                savedApple["IndexId"] = apples.IndexId
                savedApple["Position"] = apples.rect.topleft
                savedApple["CurrentPhase"] = apples.currentPhase

    def saveSoilData(self):
        for index,soil in enumerate(self.soilTileSprites):
            savedSoil = self.gameState["Soil"][f"{soil.type}{index}"] = {}
            savedSoil["Position"] = soil.rect.topleft
            savedSoil["CurrentState"] = soil.currentState
            savedSoil["Watered"] = soil.watered
            savedSoil["Tilted"] = soil.tilted
            savedSoil["IndexId"] = soil.indexId
            savedSoil["Planted"] = soil.planted

    def saveAnimalData(self):
        for index,animals in enumerate(self.animalsList):
            savedAnimal = self.gameState["Animals"][f"{animals.type}{index}"] = {}
            savedAnimal["Name"] = animals.type
            savedAnimal["Position"] = animals.rect.topleft

    def savePickableSprites(self):
        for index, items in enumerate(self.pickAbleItemSprites):
            if items.type == "Apple":
                savedApple = self.gameState["PickableItems"][f"{items.type}{index}"] = {}
                savedApple["Name"] = items.data["name"]
                savedApple["Position"] = items.rect.topleft

    def loadPlayerData(self):
        player = self.player
        player.coins = self.gameState["Player"]["Coins"]
        player.hitbox.center = self.gameState["Player"]["Position"]
        try:
            for index, items in enumerate(self.gameState["Player"]["Items"]):
                player.inventory.loadItems(index, items)
        except:
            print("no items found")


    def loadItemChestData(self):
        for index,items in enumerate(self.gameState["ItemChest"].values()):
            self.chestInventory.loadItems(index,items)


    def loadAnimalData(self):
        for index,animals in enumerate(self.gameState["Animals"].values()):
            if animals["Name"] == "Chicken":
                newChicken = Chicken(animals["Name"], animals["Position"], [self.visibleSprites], self.animalCollider, self.pickAbleItemSprites)
                self.animalsList.append(newChicken)
            if animals["Name"] == "Cow":
                newCow = Cow(animals["Name"], animals["Position"], [self.visibleSprites], self.animalCollider, self.pickAbleItemSprites)
                self.animalsList.append(newCow)

    def loadSoilData(self):
        for index,soil in enumerate(self.gameState["Soil"].values()):
            currentSoil = self.soilList[soil["IndexId"]]
            currentSoil.rect.topleft = soil["Position"]
            currentSoil.currentState = soil["CurrentState"]
            currentSoil.tilted = soil["Tilted"]
            currentSoil.watered = soil["Watered"]
            currentSoil.indexId = soil["IndexId"]
            currentSoil.planted = soil["Planted"]
            currentSoil.loadState()


    def loadPlantData(self):
        for plantIndex, plants in enumerate(self.gameState["Plants"].values()):
            if plants["Name"] in seedItems:
                plant = PlantTile(plants["Position"], [self.visibleSprites], itemData[plants["Name"]],self.pickAbleItemSprites, self.timeManager, self.soilTileSprites)
                plant.LoadPhase(plants["CurrentPhase"])
                self.plantList.append(plant)


        for appleIndex,apple in enumerate(self.gameState["Apples"].values()):
                currentApple = self.appleList[apple["IndexId"]]
                currentApple.currentPhase = apple["CurrentPhase"]
                currentApple.loadState()


    def loadPickableSprites(self):
        for itemIndex, item in enumerate(self.gameState["PickableItems"].values()):
            if item["Name"] == "Apple":
                self.pickAbleItemSprites.add(AppleItem(item["Position"], self.visibleSprites,itemData["Apple"],self.pickAbleItemSprites))

    def saveGameState(self):
        for items in self.gameState.values():
                items.clear()

        self.savePlayerData()
        self.savePickableSprites()
        self.saveSoilData()
        self.savePlantData()
        self.saveAnimalData()
        self.saveItemChestData()

        self.saveload.saveGameData(self.gameState,"gameState")

    def loadGameState(self):
        self.gameState = self.saveload.loadGameData("gameState",self.defaultGameState)
        self.loadPlantData()
        self.loadSoilData()
        self.loadPickableSprites()
        self.loadAnimalData()
        self.loadItemChestData()
        self.loadPlayerData()


    def update(self):

        self.timer.update()
        self.visibleSprites.custom_draw(self.player)
        self.dialogueSystem.display()
        self.merchantStore.display()
        self.chestInventory.display()
        self.equipmentTileCollisionLogic()
        self.playerPickUpItems()
        self.updateCoinList()
        self.playerInventory.display()

        for trees in self.treeList:
            trees.update()

        if not self.gamePaused:
            for animals in self.animalsList:
                animals.update()
            self.ui.display()
            self.timeManager.dayNightCycle()
            self.player.update()