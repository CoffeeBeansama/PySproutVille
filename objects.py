import pygame as pg
from tile import Tile
from abc import abstractmethod
from settings import *
from timeManager import TimeManager
from timer import Timer
from sound import playSound
from support import import_folder
from sound import playSound
from eventManager import EventHandler

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
       
        self.frameIndex = 0
        self.speed = 0.5
        self.coinList = coinList

        self.timer = Timer(200,self.killself)

        self.spritePath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Icons/Coin/"
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
        self.image = loadSprite(self.data["CollisionSprite"],(tileSize,tileSize)).convert_alpha()
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
        self.interactableSprites = interactableSprites
        self.openChestInventory = openChestInventory
        self.add(self.interactableSprites)

        self.importSprites()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-30, -30)

        self.interactRect = self.image.get_rect(topleft=(pos[0], pos[1] + tileSize))
        self.interactHitbox = self.interactRect.inflate(-40, -40)

        self.frame_index = 0
        self.animationTime = 1 / 6
        self.state = "close"
        self.interacted = False

    def importSprites(self):
        self.sprites = {}
        spriteSize = (48, 48)
        for index in range(5):
            self.sprites[index] = loadSprite(f"{spritePath}Chests/{index}.png", spriteSize).convert_alpha()
        
        self.image = self.sprites[0]

    def interact(self):
        if EventHandler.pressingInteractKey():
            if not self.interacted:
                self.openChestInventory()
                self.interacted = True
                self.state = "Open"
            else:
                return

    def disengage(self):
        self.state = "Close"


    def animate(self):
        match self.state:
            case "Open":
                self.frame_index += self.animationTime
                if self.frame_index >= len(self.sprites):
                    self.frame_index = len(self.sprites) -1
            case "Close":
                self.frame_index -= self.animationTime
                if self.frame_index <= 0:
                    self.frame_index = 0
                    if self.interacted:
                        playSound("Chest")
                        self.interacted = False

        self.image = self.sprites[int(self.frame_index)]

    def update(self):
        self.animate()


class Bed(InteractableObjects):
    def __init__(self,image,pos,group,player):
        super().__init__(group)

        self.player = player
        self.type = "Bed"
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.interactRect = image.get_rect(topleft=(pos[0], pos[1] + tileSize))
        self.interactHitbox = self.interactRect.inflate(-40, -40)

    def interact(self):
        if EventHandler.pressingInteractKey():
            if not self.interacted:
                self.player.laidToBed = True
                self.interacted = True


    def disengage(self):
        self.interacted = False

class Door(InteractableObjects):
    def __init__(self,pos,group,player):
        super().__init__(group)
        self.player = player
        self.type = "Door"
        self.state = "Close"

        self.importSprites()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.interactRect = self.image.get_rect(topleft=(pos[0], pos[1]))
        self.interactHitbox = self.interactRect.inflate(0,20)

        self.animationTime = 1 / 6
        self.frame_index = 0

    def importSprites(self):
        self.sprites = {}
        for index in range(0,4):
            self.sprites[index] = loadSprite(f"Sprites/{self.type}/{index+1}.png", (tileSize, tileSize)).convert_alpha()
        self.image = self.sprites[0]

    def interact(self):
        self.state = "Open"
        if not self.interacted:
            playSound("Door Open")
            self.interacted = True

    def disengage(self):
        self.state = "Close"
        if self.interacted:
            playSound("Door Close")
            self.interacted = False


    def animate(self):
        match self.state:
            case "Open":
                self.frame_index += self.animationTime
                if self.frame_index >= len(self.sprites):
                    self.frame_index = len(self.sprites) -1
            case "Close":
                self.frame_index -= self.animationTime
                if self.frame_index <= 0:
                    self.frame_index = 0

        self.image = self.sprites[int(self.frame_index)]

    def update(self):
        self.animate()











