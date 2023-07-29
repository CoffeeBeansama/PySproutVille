from settings import *
from tile import *
from player import Player
from inventory import *
from debug import debug
from items import *
from support import import_csv_layout


class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_canvas = pg.display.get_surface()
        self.half_width = self.display_canvas.get_size()[0] // 2
        self.half_height = self.display_canvas.get_size()[1] // 2

        self.groundSprite = pg.image.load("Sprites/map.png").convert()
        self.groundRect = self.groundSprite.get_rect(topleft=(0,0))

        self.internalSurfaceSize = (500,500)
        self.internalSurface = pg.Surface(self.internalSurfaceSize,pg.SRCALPHA)
        self.internalRect = self.internalSurface.get_rect(center=(self.half_width,self.half_height))

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

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery - 15 if sprite.type == "object" else sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset + self.internalOffset
            self.internalSurface.blit(sprite.image, offset_rect)

        scaledSurface = pg.transform.scale(self.internalSurface, self.zoomInSize)
        scaledRect = scaledSurface.get_rect(center=(self.half_width,self.half_height))
        self.display_canvas.blit(scaledSurface,scaledRect)


class Level:
    def __init__(self,main):

        self.main = main
        self.player = None
        self.screen = pg.display.get_surface()

        self.visibleSprites = CameraGroup()
        self.collisionSprites = pg.sprite.Group()
        self.pickAbleItems = pg.sprite.Group()
        self.playerSprite = pg.sprite.Group()

        self.createMap()

    def createMap(self):

        mapLayouts = {
            "boundary": import_csv_layout("Map/wall.csv"),
            "plantTile": import_csv_layout("map/plantableGrounds_Plantable Ground.csv")

        }
        for style, layout in mapLayouts.items():
            for rowIndex,row in enumerate(layout):
                for columnIndex,column in enumerate(row):

                    if column != "-1":
                        x = columnIndex * tileSize
                        y = rowIndex * tileSize

                        if style == "boundary":
                            Tile(testSprites["Player"],(x,y),[self.collisionSprites])

                        if style == "plantTile":
                            PlantTile((x,y),[self.visibleSprites])

        self.player = Player(testSprites["Player"],[self.visibleSprites,self.playerSprite],self.collisionSprites,self)


    def playerCollision(self):
        for sprites in self.playerSprite:
            itemCollided = pg.sprite.spritecollide(sprites,self.pickAbleItems,False)

            if itemCollided:
                for items in itemCollided:
                    self.player.updateInventory(items.data)
                    items.kill()


    def update(self):
        self.visibleSprites.custom_draw(self.player)
        self.playerCollision()
        self.player.update()

