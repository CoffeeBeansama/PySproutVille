import pygame as pg
from tile import Tile
from abc import abstractmethod
from settings import *
from timeManager import TimeManager


class InteractableObjects(Tile):
    def __init__(self,image,pos,group):
        super().__init__(image,pos,group)

        self.interacted = False

    @abstractmethod
    def interact(self):
        pass

    @abstractmethod
    def disengage(self):
        pass


class CoinOverHead(pg.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.type = "object"
        self.spritePath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Icons/Coin/"

        self.frameIndex = 0
        self.speed = 0.8

        self.sprites = {
            0: loadSprite(f"{self.spritePath}1.png", (tileSize, tileSize)).convert_alpha(),
            1: loadSprite(f"{self.spritePath}2.png", (tileSize, tileSize)).convert_alpha(),
            2: loadSprite(f"{self.spritePath}3.png", (tileSize, tileSize)).convert_alpha(),
            3: loadSprite(f"{self.spritePath}4.png", (tileSize, tileSize)).convert_alpha(),

        }
        self.image = self.sprites[self.frameIndex]
        self.rect = self.image.get_rect(topleft=pos)

        self.animationTime = 1 / 8

    def update(self,coinList):
        self.frameIndex += self.animationTime

        if self.frameIndex >= len(self.sprites) - 1:
            coinList.remove(self)
            self.kill()

        self.image = self.sprites[int(self.frameIndex)]
        self.rect.y -= 1 * self.speed

class PickAbleItems(pg.sprite.Sprite):
    def __init__(self,pos,group,data):
        super().__init__(group)

        self.data = data
        self.collided = False

    def pickUpItem(self, plantlist,player,coinSpriteGroup,coinList):

        self.image = self.data["CollisionSprite"].convert_alpha()
        self.currentTime = pg.time.get_ticks()

        plantlist.remove(self) if self in plantlist else None

        if not self.collided:
            self.collided = True
            self.tickStart = pg.time.get_ticks()

        if self.currentTime - self.tickStart > 100 and self.collided:
            player.coins += self.data["costs"]
            coinList.append(CoinOverHead((player.rect.x + tileSize,player.rect.y), coinSpriteGroup))
            self.kill()

class ChestObject(pg.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.type = "object"
        self.spriteIndex = 1
        self.image = chestSprites[self.spriteIndex]
        self.animationTime = 1 / 20
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

    def OpenAnimation(self):
        self.image = chestSprites[5]

    def CloseAnimation(self):
        self.image = chestSprites[1]


class ChestTile(InteractableObjects):
    def __init__(self,pos,group,chestObject,player,image=testSprites["Wall"]):
        super().__init__(image,pos,group)


        self.type = "chest"
        self.player = player
        self.rect = image.get_rect(topleft=pos)
        self.chestObject = chestObject

    def interact(self):
        keys = pg.key.get_pressed()
        playerInventory = self.player.inventory
        if keys[pg.K_x]:
            if not self.interacted:
                self.chestObject.OpenAnimation()
                playerInventory.sellItems()
                self.interacted = True
            else:
                return

    def disengage(self):
        self.interacted = False
        self.chestObject.CloseAnimation()


class BedTile(InteractableObjects):
    def __init__(self,group,timeManager,pos=(848,800),image=testSprites["Wall"]):
        super().__init__(image,pos,group)

        self.timeManager = timeManager
        self.type = "object"
        self.rect = image.get_rect(topleft=pos)

    def interact(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_x]:
            if not self.interacted:
                self.timeManager.laidToBed = True
                self.interacted = True

    def disengage(self):
        self.interacted = False