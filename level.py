from settings import *
from tile import *
from player import Player
from inventory import *
from debug import debug
from plants import PlantTile
from soil import SoilTile
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
from roof import RoofTile
from berries import *
from sound import *


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
        self.zoomInSize = (1500, 1500)

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
        self.screen = self.main.screen

        self.gamePaused = False
        self.displayMerchantStore = False
        self.currentEquipmentInstance = None

        self.visibleSprites = CameraGroup()
        self.collisionSprites = pg.sprite.Group()
        self.equipmentSprites = pg.sprite.Group()
        self.soilTileSprites = pg.sprite.Group()
        self.woodTileSprites = pg.sprite.Group()
        self.pickAbleItemSprites = pg.sprite.Group()
        self.playerSprite = pg.sprite.Group()
        self.interactableSprites = pg.sprite.Group()
        self.animalCollider = pg.sprite.Group()
        self.roofSprites = pg.sprite.Group()
        self.outsideHouseSprites = pg.sprite.Group()
        self.animalSprites = pg.sprite.Group()

        self.timer = Timer(200)
        self.timeManager = TimeManager(None,self.updateEntities)

        self.PlantedSoilTileList = []
        self.plantTile = None
        self.plantList = []
        self.appleList = []
        self.animalsList = []
        self.soilList = []
        self.berryBushesList = []


        self.treeList = []

        self.soilIndex = 0
        self.appleIndex = 0


        self.coinList = []


        self.invisibleSprite = loadSprite(f"{testSpritePath}wall.png",(tileSize,tileSize))

        self.playerInventory = PlayerInventory(None)
        self.player = Player([self.visibleSprites, self.playerSprite], self.collisionSprites, self.createEquipmentTile,
                             self.interactableSprites, self.pickAbleItemSprites, self.timeManager, None,
                             self.playerInventory)
        self.chestInventory = ChestInventory(self.playerInventory, self.closeChestInventory)
        self.playerInventory.chestInventory = self.chestInventory

        self.createMap()


        self.gameState = {
            "Player": self.player.data,
            "Plants": {},
            "Trees": {},
            "Apples": {},
            "Soil": {},
            "PickableItems": {},
            "Animals": {},
            "PlayerInventorySlots": {},
            "ItemChestItems": {},
            "ItemChestSlots": { "itemName":{}},

        }

        self.defaultGameState = {
            "Player": self.player.defaultData,
            "Plants": {},
            "Trees": {},
            "Apples": {},
            "Soil": {},
            "PickableItems": {},
            "Animals": {},
            "PlayerInventorySlots": {},
            "ItemChestItems": {},
            "ItemChestSlots": {"itemName":{}}

        }


        self.merchantStore = MerchantStore(self.player, self.closeMerchantStore,self.createChickenInstance,self.createCowInstance,self.playerInventory.openInventory)
        self.dialogueSystem = DialogueSystem(self.player, None, self.openMerchantStore,self.playerInventory.closeInventory)

        self.getPlayerData([self.timeManager,self.bedTile,self.doorObject])

        self.ui = Ui(self.player,self.displayMerchantStore)
        self.dynamicUi = self.ui.dynamicUi
        self.merchant.dialogueSystem,dynamicUi = self.dialogueSystem,self.dynamicUi
        self.dialogueSystem.dynamicUi = self.dynamicUi
        self.player.dialogueSystem = self.dialogueSystem

        self.chickenSpawnPoint = (1206, 938)
        self.cowSpawnPoint = (1130, 1378)

        playBGM("level")

        self.font = pg.font.Font("Font/PeaberryBase.ttf", 60)
        self.fontColor = (255, 255, 255)
        self.titleText = self.font.render("Sprout Ville",True,self.fontColor)
        self.startLevel = False

        self.timer = Timer(300)

        self.saveload = SaveLoadSystem(".data", "savedata",self.player,self.treeList,self.chestInventory,self.plantList,self.appleList,self.soilList,self.animalsList,self.pickAbleItemSprites,
                                       self.visibleSprites,self.timeManager,self.soilTileSprites,self.animalCollider,self.animalSprites,self.berryBushesList)
        self.saveload.loadGameState()

    def createMap(self):

        mapLayouts = {
            "boundary": import_csv_layout("Map/wall.csv"),
            "soilTile": import_csv_layout("Map/plantableGrounds_Plantable Ground.csv"),
            "InteractableObjects": import_csv_layout('Map/InteractableObjects.csv'),
            "Animal Collider": import_csv_layout('Map/AnimalCollision.csv'),
            "Fence": import_csv_layout('Map/Fences.csv'),
            "Tree Base": import_csv_layout('Map/Tree Base.csv'),
            "Roof": import_csv_layout('Map/roof.csv'),
            "HouseCollider": import_csv_layout('Map/HouseCollider.csv'),
            "BerryBush": import_csv_layout('Map/BerryBushes.csv')

        }
        for style, layout in mapLayouts.items():
            for rowIndex, row in enumerate(layout):
                for columnIndex, column in enumerate(row):

                    if column != "-1":
                        x = columnIndex * tileSize
                        y = rowIndex * tileSize

                        if style == "boundary":
                            Tile(self.invisibleSprite, (x, y), [self.collisionSprites])

                        if style == "soilTile":
                            self.soilList.append(SoilTile((x, y), [self.visibleSprites,self.soilTileSprites],False,self.soilIndex))
                            self.soilIndex += 1

                        if style == "HouseCollider":
                            if column == "Outside":
                                Tile(self.invisibleSprite, (x, y), [self.outsideHouseSprites])

                        if style == "InteractableObjects":
                            if column == "bed":
                                self.bedTile = Bed(loadSprite(f"{testSpritePath}wall.png",(tileSize,tileSize)),(x,y),[self.interactableSprites], None)
                            if column == "chest":
                                self.chestObject = Chest((x - tileSize, y-tileSize),[self.visibleSprites,self.collisionSprites],self.player,self.interactableSprites,self.openChestInventory)
                            if column == "door":
                                self.doorObject = Door((x, y),[self.visibleSprites,self.interactableSprites],None)

                        if style == "Animal Collider":
                            Fence(self.invisibleSprite, (x, y), [self.animalCollider])

                        if style == "Fence":
                            Fence(self.invisibleSprite, (x, y), [self.collisionSprites])

                        if style == "BerryBush":
                            bush = BerryBush((x,y),[self.visibleSprites,self.interactableSprites],self.visibleSprites,self.pickAbleItemSprites,self.timeManager,self.player.inventory)
                            self.berryBushesList.append(bush)

                        if style == "Tree Base":
                            self.treeList.append(TreeBase((x,y),[self.woodTileSprites,self.collisionSprites,self.visibleSprites],self.visibleSprites,self.pickAbleItemSprites,self.appleList,self.appleIndex,[self.visibleSprites,self.collisionSprites]))
                            self.appleIndex += 1

                        if style == "Roof":
                            RoofTile(loadSprite(f"{roofSpritePath}{column}.png",(tileSize,tileSize)).convert_alpha(), (x,y), [self.visibleSprites, self.roofSprites], self.playerSprite, self.roofSprites)

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
        self.currentEquipmentInstance = Equipment([self.equipmentSprites], self.player)
        return

    def updateEntities(self):
        for plants in self.plantList:
            plants.NextPhase()
        for bushes in self.berryBushesList:
            bushes.NextPhase()
        for animals in self.animalsList:
            animals.produce()
        for soils in self.soilList:
            soils.update()

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
            animalSpriteCollided = pg.sprite.spritecollide(sprites,self.animalSprites, False)

            if inventory.currentItems[inventory.itemIndex] is not None:
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
                        playSound("Axe")

                if animalSpriteCollided:
                    animalSpriteCollided[0].feed()

            if self.currentEquipmentInstance is not None:
                self.currentEquipmentInstance.kill()
                return



    def seedPlantTile(self, soilTile,data):
        if soilTile.planted: return
        if soilTile.currentState == "Tilted" or soilTile.currentState == "Watered":
            plantTile = PlantTile(soilTile.rect.topleft,
                                  [self.visibleSprites],
                                  data,
                                  self.pickAbleItemSprites,
                                  self.timeManager,self.soilTileSprites)
            soilTile.currentPlant = plantTile
            self.plantList.append(plantTile)
            self.PlantedSoilTileList.append(soilTile)
            soilTile.planted = True
            playSound("Seed")


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
        newChicken = Chicken("Chicken",
                             self.chickenSpawnPoint, 
                             [self.visibleSprites,self.animalSprites], 
                             self.animalCollider, 
                             self.pickAbleItemSprites)
        self.animalsList.append(newChicken)

    def createCowInstance(self):
        newCow = Cow("Cow",
                     self.cowSpawnPoint,
                     [self.visibleSprites,
                      self.animalSprites], 
                      self.animalCollider, 
                      self.pickAbleItemSprites)
        self.animalsList.append(newCow)


    def titleScreen(self):
        pos = pg.mouse.get_pos()
        mouse_presses = pg.mouse.get_pressed()

        self.screen.blit(uiSprites["MenuBackground"].convert_alpha(),(0,0))
        self.screen.blit(uiSprites["MenuImageOverLay"].convert_alpha(),(100,100))
        playButton = self.screen.blit(uiSprites["PlayButton"].convert_alpha(),(300,320))

        self.screen.blit(self.titleText.convert_alpha(),(200,200))
        playButtonPressed = playButton.collidepoint(pos)

        if playButtonPressed:
            if mouse_presses[0]:
                self.startLevel = True


    def update(self):
        self.timer.update()

        if self.startLevel:
                self.timer.update()
                self.visibleSprites.custom_draw(self.player)
                self.dialogueSystem.display()
                self.merchantStore.display()
                self.chestInventory.display()
                self.equipmentTileCollisionLogic()
                self.playerPickUpItems()
                self.updateCoinList()
                self.doorObject.update()
                self.playerInventory.display()
                self.chestObject.update()

                for trees in self.treeList:
                    trees.update()

                for roofTiles in self.roofSprites:
                    roofTiles.update()

                if not self.gamePaused:
                    for animals in self.animalsList:
                        animals.update()
                    self.ui.display()
                    self.timeManager.dayNightCycle()
                    self.player.update()
        else:
            self.titleScreen()
