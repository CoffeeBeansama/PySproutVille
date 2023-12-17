import pygame as pg
from settings import seedItems,equipmentItems,tileSize,animalFodders
from entity import Entity
from support import import_folder,loadSprite
from enum import Enum
from timer import Timer
from sound import *
from eventManager import EventHandler


class Player(Entity):
    def __init__(self,group,collidable_sprites,useEquipmentTile,interactableObjects,pickableItems,timeManager,dialogueSystem,inventory):
        super().__init__(group)
        self.type = "player"
        self.screen = pg.display.get_surface()

        self.collisionSprites = collidable_sprites
        self.pickAbleItems = pickableItems
        self.createEquipmentTile = useEquipmentTile
        self.dialogueSystem = dialogueSystem
        self.timeManager = timeManager
        self.interactableObjects = interactableObjects
        self.animations_States = None

        self.inventory = inventory
        self.displayInventory = False
        self.currentItemsHolding = []

        self.initializePlayerData()

        self.startingPos = self.data["Position"]
        self.image = loadSprite("Sprites/Player/Down_idle/00.png",(tileSize,tileSize)).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.startingPos)
        self.hitbox = self.rect.inflate(-5, 0)


        self.importSprites()

        self.usingItem = False
        self.laidToBed = False
        self.nearAnInteractableObject = False

        self.timer = Timer(300)


    
    def initializePlayerData(self):
        self.data = {
            "Position" : (948, 866),
            "Coins": 0,
            "Items": self.inventory.playerCurrentItems
        }

        self.defaultData = {
            "Position": (948, 866),
            "Coins": 600,
            "Items": self.inventory.playerInventoryDefaultItems
        }

        self.maxLives = 3
        self.lives = 3
        self.coins = self.data["Coins"]

        self.mood = "Idle"
        self.state = "Down_idle"

        self.walkSpeed = 2

        self.frame_index = 0
        self.walkingAnimationTime = 1 / 8
        self.eqpActionAnimationTime = 1 / 20
        self.facingDirection = "Down"

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

    def handleAnimation(self):
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

    def handleMovement(self, speed):
        self.hitbox.x += self.direction.x * speed
        self.checkWallCollision("Horizontal")
        self.hitbox.y += self.direction.y * speed
        self.checkWallCollision("Vertical")
        self.rect.center = self.hitbox.center


    def interact(self):
        for objectIndex,object in enumerate(self.interactableObjects):
            if hasattr(object,"interactHitbox"):
                if object.interactHitbox.colliderect(self.hitbox):
                    self.nearAnInteractableObject = True
                    object.interact()
                    return
                else:
                    self.nearAnInteractableObject = False
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
    
    def canUseItem(self):
        if self.laidToBed:
           return False
        if self.dialogueSystem.dialogueActive:
           return False
        if self.nearAnInteractableObject:
           return False

        return True
    
    def useItemEquipped(self):    
        if self.inventory.selectingEquipmentSlot():
           self.frame_index = 0
           self.usingItem = True

           if self.inventory.playerCurrentItems[self.inventory.itemIndex]["name"] in equipmentItems:
              self.state = f"{self.inventory.getCurrentSelectedItem()}_{self.facingDirection}"
           elif self.inventory.playerCurrentItems[self.inventory.itemIndex]["name"] in seedItems:
              self.state = f"{self.facingDirection}_idle"
              self.createEquipmentTile()
              self.usingItem = False
           elif self.inventory.playerCurrentItems[self.inventory.itemIndex]["name"] in animalFodders:
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

    def handleKeyboardInput(self):
    
        if self.allowedToMove():

            if EventHandler.pressingUpKey():
                self.getState(self.verticalDirection, -1, "Up")
            elif EventHandler.pressingDownKey():
                self.getState(self.verticalDirection, 1, "Down")
            elif EventHandler.pressingLeftKey():
                self.getState(self.horizontalDirection, -1, "Left")
            elif EventHandler.pressingRightKey():
                self.getState(self.horizontalDirection, 1, "Right")
            else:
                self.idleState()
        
        if self.notMoving():
            if EventHandler.pressingInteractKey() and self.canUseItem():
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
            

    def update(self):
    
        self.timer.update()
        self.handleKeyboardInput()
        self.updateMood()
        self.handleMovement(self.walkSpeed)
        self.handleAnimation()
        self.interact()




