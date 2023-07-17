from settings import *
from tile import *
from player import Player
from inventory import *

class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_canvas = pg.display.get_surface()
        self.half_width = self.display_canvas.get_size()[0] // 2
        self.half_height = self.display_canvas.get_size()[1] // 2
        self.offset = pg.math.Vector2()

    def custom_draw(self, player):
        # getting the offset  for camera
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset
            self.display_canvas.blit(sprite.image, offset_rect)
class Level:
    def __init__(self,main):

        self.main = main
        self.player = None
        self.screen = pg.display.get_surface()
        self.visibleSprites = CameraGroup()
        self.collisionSprites = pg.sprite.Group()

        self.inventory = Inventory()
        self.displayInventory = False

        self.createMap()

    def renderInventory(self):
        if self.displayInventory:
            self.displayInventory = False
        else:
            self.displayInventory = True

    def createMap(self):
        for rowIndex,row in enumerate(map):
            for columnIndex,column in enumerate(row):
                x = columnIndex * tileSize
                y = rowIndex * tileSize

                if column == "W":
                    Tile(testSprites["Wall"],(x,y),[self.visibleSprites,self.collisionSprites])

        self.player = Player(testSprites["Player"],[self.visibleSprites],self.collisionSprites,self)

    def update(self):

        self.visibleSprites.custom_draw(self.player)

        if self.displayInventory:
            self.inventory.display()
        else:
            self.player.update()

