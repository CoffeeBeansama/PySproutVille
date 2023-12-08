import pygame as pg
from settings import seedItems,equipmentItems,tileSize,animalFodders
from entity import Entity
from support import import_folder,loadSprite
from enum import Enum
from timer import Timer
from sound import *

class Player(Entity):
    def __init__(self,group,collidable_sprites,useEquipmentTile,interactableObjects,pickableItems,timeManager,dialogueSystem,inventory):
        super().__init__(group)
        self.screen = pg.display.get_surface()
        self.type = "player"
        self.animations_States = None

        self.inventory = inventory
        self.displayInventory = False
        self.currentItemsHolding = []

        self.data = {
            "Position" : (948, 866),
            "Coins": 0,
            "Items": self.inventory.currentItems

        }
        self.defaultData = {
            "Position": (948, 866),
            "Coins": 600,
            "Items": self.inventory.defaultInventorySetup

        }

        self.startingPos = self.data["Position"]

        self.maxLives = 3
        self.lives = 3

        self.frame_index = 0
        self.walkingAnimationTime = 1 / 8
        self.eqpActionAnimationTime = 1 / 20

        self.image = loadSprite("Sprites/Player/Down_idle/00.png",(tileSize,tileSize)).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.startingPos)
        self.hitbox = self.rect.inflate(-5, 0)

        self.coins = self.data["Coins"]

        self.mood = "Idle"

        self.facingDirection = "Down"
        self.state = "Down_idle"
        self.importSprites()

        self.itemIndex = 0
        self.equippedItem = equipmentItems[self.itemIndex]

        self.usingItem = False

        self.laidToBed = False

        self.timer = Timer(200)

        self.collisionSprites = collidable_sprites
        self.pickAbleItems = pickableItems
        self.createEquipmentTile = useEquipmentTile
        self.dialogueSystem = dialogueSystem
        self.timeManager = timeManager
        self.interactableObjects = interactableObjects

        self.playerSpeed = 2

    def importSprites(self):
        player_path = "Sprites/Player/"
        self.animations_States = {
            'Up': [], 'Down': [], 'Left': [], 'Right': [],
            "Up_idle": [], "Down_idle": [], "Left_idle": [], "Right_idle": [],
            "Hoe_Up": [], "Hoe_Down": [], "Hoe_Left": [], "Hoe_Right": [],
            "Axe_Up": [], "Axe_Down": [], "Axe_Left": [], "Axe_Right": [],
            "WateringCan_Up": [], "WateringCan_Down": [], "WateringCan_Left": [], "WateringCan_Right": [],
        }

        for animation in self.animations_States.keys():
            full_path = player_path + animation
            self.animations_States[animation] = import_folder(full_path)

    def animate(self):
        if not self.laidToBed:
            animation = self.animations_States[self.state]
            self.frame_index += self.eqpActionAnimationTime if self.usingItem else self.walkingAnimationTime

            notMoving = self.direction.x == 0 and self.direction.y == 0

            if self.frame_index >= len(animation):
                self.frame_index = 0 if not self.usingItem else len(animation) - 1

                usingEquipment = not "idle" in self.state and notMoving
                if usingEquipment:
                    self.createEquipmentTile()
                    self.usingItem = False

            self.image = animation[int(self.frame_index)]
            self.rect = self.image.get_rect(center=self.hitbox.center)


    @staticmethod
    def getState(function, value, state):
        return function(value, state)

    def updateInventory(self,item):
        self.inventory.update(item)

    def horizontalDirection(self, value, state):
        self.direction.x = value
        self.direction.y = 0
        self.state = state
        self.facingDirection = state

    def verticalDirection(self, value, state):
        self.direction.x = 0
        self.direction.y = value
        self.state = state
        self.facingDirection = state

    def movement(self, speed):
        self.hitbox.x += self.direction.x * speed
        self.checkWallCollision("Horizontal")
        self.hitbox.y += self.direction.y * speed
        self.checkWallCollision("Vertical")
        self.rect.center = self.hitbox.center


    def interact(self):
        for objectIndex,object in enumerate(self.interactableObjects):
            if hasattr(object,"interactHitbox"):
                if object.interactHitbox.colliderect(self.hitbox):
                    object.interact()
                else:
                    object.disengage()


    def checkWallCollision(self, direction):
        for sprite in self.collisionSprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == "Horizontal":
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    else:
                        self.hitbox.right = sprite.hitbox.left

                elif direction == "Vertical":
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    else:
                        self.hitbox.bottom = sprite.hitbox.top


    def increaseCoin(self,cost):
        playSound("Coin")
        self.mood = "Happy"
        self.coins += cost
        self.moodTickTime = pg.time.get_ticks()


    def idleState(self):
        self.direction.x = 0
        self.direction.y = 0
        if not "idle" in self.state and not self.usingItem:
            self.state = f"{self.facingDirection}_idle"

    def getEItemEquipped(self):
        self.itemIndex += 1
        if self.itemIndex >= len(equipmentItems):
            self.itemIndex = 0
        self.equippedItem = equipmentItems[self.itemIndex]
    
    def cannotUseItem(self):
        if self.laidToBed:
           return True
        if self.dialogueSystem.dialogueActive:
           return True

        return False
    
    def useItemEquipped(self):    
        if self.cannotUseItem(): return
           
        if self.inventory.selectingEquipmentSlot():
           self.frame_index = 0
           self.usingItem = True

           if self.inventory.currentItems[self.inventory.itemIndex]["name"] in equipmentItems:
              self.state = f"{self.inventory.getCurrentSelectedItem()}_{self.facingDirection}"
           elif self.inventory.currentItems[self.inventory.itemIndex]["name"] in seedItems:
              self.state = f"{self.facingDirection}_idle"
              self.createEquipmentTile()
              self.usingItem = False
           elif self.inventory.currentItems[self.inventory.itemIndex]["name"] in animalFodders:
              self.state = f"{self.facingDirection}_idle"
              self.createEquipmentTile()
              self.usingItem = False
    
    def notMoving(self):
        if self.direction.x == 0 and self.direction.y == 0:
           return True
        return False
    
    def allowedToMove(self):
        if self.usingItem:
           return False
        if self.laidToBed:
           return False
        if self.dialogueSystem.dialogueActive:
           return False

        return True

    def getInputs(self):
        keys = pg.key.get_pressed()
        
        if self.allowedToMove():

            if keys[pg.K_w]:
                self.getState(self.verticalDirection, -1, "Up")
            elif keys[pg.K_s]:
                self.getState(self.verticalDirection, 1, "Down")
            elif keys[pg.K_a]:
                self.getState(self.horizontalDirection, -1, "Left")
            elif keys[pg.K_d]:
                self.getState(self.horizontalDirection, 1, "Right")
            else:
                self.idleState()
        
        if keys[pg.K_SPACE] and self.notMoving():

           if not self.timer.activated:
              self.useItemEquipped()
              self.timer.activate()

    def resetLives(self):
        self.lives = self.maxLives

    def checkifSleepy(self,dayPeriod):
        if self.mood != "Happy" :
            if dayPeriod == -1 or self.laidToBed:
                self.mood = "Sleepy"
            else:
                self.mood = "Idle"

    def updateMood(self):
        if self.mood == "Happy":
            self.frame_index = 0
            if self.currentTime - self.moodTickTime > 300:
                self.mood = "Idle"

    def update(self):
        self.currentTime = pg.time.get_ticks()


        self.timer.update()
        self.getInputs()
        self.updateMood()
        self.movement(self.playerSpeed)
        self.animate()
        self.interact()




