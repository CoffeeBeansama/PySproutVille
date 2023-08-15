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


        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery - 15 if sprite.type in groundTiles else sprite.rect.centery):
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

        self.currentEquipment = None

        self.visibleSprites = CameraGroup()
        self.collisionSprites = pg.sprite.Group()
        self.equipmentSprites = pg.sprite.Group()
        self.soilTileSprites = pg.sprite.Group()
        self.woodTileSprites = pg.sprite.Group()
        self.pickAbleItemSprites = pg.sprite.Group()
        self.playerSprite = pg.sprite.Group()
        self.interactableSprites = pg.sprite.Group()


        self.timeManager = TimeManager()
        self.PlantedSoilTileList = []

        self.plantTile = None
        self.plantTileList = []

        self.coinList = []

        self.createMap()


    def createMap(self):

        mapLayouts = {
            "boundary": import_csv_layout("Map/wall.csv"),
            "soilTile": import_csv_layout("map/plantableGrounds_Plantable Ground.csv"),
            "InteractableObjects": import_csv_layout('Map/InteractableObjects.csv'),
            "Tree Trunks": import_csv_layout('Map/Tree trunks.csv'),

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
                            SoilTile((x, y), [self.visibleSprites,self.soilTileSprites])


                        if style == "InteractableObjects":
                            if column == "Bed":
                                self.bedTile = BedTile([self.interactableSprites], self.timeManager)
                            if column == "Chest":
                                self.chestObject = ChestObject((x, y - tileSize),[self.visibleSprites,self.collisionSprites])
                                self.chestTile = ChestTile((x, y), [self.interactableSprites], self.chestObject,self.player)

                        if style == "Tree Trunks":
                            Tree((x,y),[self.collisionSprites,self.woodTileSprites],self.visibleSprites,self.timeManager,self.pickAbleItemSprites)



        self.player = Player(
            testSprites["Player"],
            [self.visibleSprites,
             self.playerSprite],
            self.collisionSprites,
            self.createEquipmentTile,
            self.interactableSprites,
            self.pickAbleItemSprites,
            self.timeManager
            )


        self.chestTile.player = self.player


    def plantGrowth(self):
        for soil in self.PlantedSoilTileList:
            soil.update()

    def createEquipmentTile(self):
        self.currentEquipment = Equipment([self.equipmentSprites], self.player)

    def playerPickUpItems(self):
        for itemIndex, items in enumerate(self.pickAbleItemSprites):
            if items.hitbox.colliderect(self.player.hitbox):

                items.pickUpItem(self.timeManager.plantList,self.player,self.visibleSprites,self.coinList)


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
            pass
            self.currentEquipment.kill()

    def seedPlantTile(self, soilTile,data):
        if soilTile.currentPlant is None and soilTile.tilted:

            plantTile = PlantTile(soilTile.rect.topleft,[self.visibleSprites],data,soilTile,self.pickAbleItemSprites,self.timeManager)

            soilTile.currentPlant = plantTile
            self.timeManager.plantList.append(plantTile)
            self.PlantedSoilTileList.append(soilTile)

    def updateCoinList(self):
        if len(self.coinList) > 0:
            for coins in self.coinList:
                coins.update(self.coinList)


    def update(self):

        self.visibleSprites.custom_draw(self.player)
        self.equipmentTileCollisionLogic()
        self.player.update()
        self.playerPickUpItems()
        self.updateCoinList()
        self.timeManager.dayNightCycle()