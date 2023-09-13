import pygame as pg
from tile import Tile
from abc import abstractmethod
from settings import *
from timeManager import TimeManager
from timer import Timer


class InteractableObjects(pg.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)

        self.interacted = False

    @abstractmethod
    def interact(self):
        pass

    @abstractmethod
    def disengage(self):
        pass


class CoinOverHead(pg.sprite.Sprite):
    def __init__(self, pos, group,coinList):
        super().__init__(group)

        self.type = "object"
        self.spritePath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Icons/Coin/"

        self.frameIndex = 0
        self.speed = 0.5
        self.coinList = coinList

        self.timer = Timer(200,self.killself)

        self.image = loadSprite(f"{self.spritePath}1.png", (tileSize, tileSize)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def killself(self):
        self.coinList.remove(self)
        self.kill()

    def update(self,coinList):
        self.rect.y -= 1 * self.speed
        self.timer.update()

        if not self.timer.activated:
            self.timer.activate()


class PickAbleItems(pg.sprite.Sprite):
    def __init__(self,pos,group,data):
        super().__init__(group)

        self.rect = None
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
            if self.data["name"] in sellableItems:
                player.increaseCoin(self.data["costs"])
                coinList.append(CoinOverHead((player.rect.x + tileSize,player.rect.y), coinSpriteGroup,coinList))
            else:
                player.inventory.AddItem(self)

            self.kill()


class Fence(pg.sprite.Sprite):
    def __init__(self,image,pos,group):
        super().__init__(group)
        self.type = "object"
        self.image = image.convert_alpha()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-12,-5)


class Chest(pg.sprite.Sprite):
    def __init__(self, pos, group,player,interactableSprites,openChestInventory):
        super().__init__(group)
        self.type = "Chest"

        self.player = player
        self.spriteIndex = 1
        self.image = chestSprites[self.spriteIndex].convert_alpha()
        self.animationTime = 1 / 20
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.interactRect = self.image.get_rect(topleft=(pos[0], pos[1] + tileSize))
        self.interactHitbox = self.interactRect.inflate(-40, -40)

        self.interactableSprites = interactableSprites
        self.openChestInventory = openChestInventory
        self.add(self.interactableSprites)

        self.interacted = False


    def interact(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_x]:
            if not self.interacted:
                self.OpenAnimation()
                self.openChestInventory()
                self.interacted = True
            else:
                return

    def disengage(self):
        self.interacted = False

        self.CloseAnimation()

    def OpenAnimation(self):
        self.image = chestSprites[5].convert_alpha()

    def CloseAnimation(self):
        self.image = chestSprites[1].convert_alpha()


class Bed(InteractableObjects):
    def __init__(self,group,player,pos=(848,800),image=testSprites["Wall"]):
        super().__init__(group)

        self.player = player
        self.type = "Bed"
        self.rect = image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.interactRect = image.get_rect(topleft=(pos[0], pos[1] + tileSize))
        self.interactHitbox = self.interactRect.inflate(-40, -40)

    def interact(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_x]:
            if not self.interacted:
                self.player.laidToBed = True
                self.interacted = True


    def disengage(self):
        self.interacted = False