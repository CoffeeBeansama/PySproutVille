import pygame as pg
from settings import *
from entity import Entity
from support import import_folder
from inventory import Inventory
from objects import CoinOverHead
from enum import Enum



class Player(Entity):
    def __init__(self, image, group,collidable_sprites,useEquipmentTile,interactableObjects,pickableItems,timeManager,dialogueSystem):
        super().__init__(group)

        self.type = "player"
        self.animations_States = None
        self.startingPos = (948, 866)

        self.maxLives = 3
        self.lives = 3

        self.frame_index = 0
        self.walkingAnimationTime = 1 / 8
        self.eqpActionAnimationTime = 1 / 20

        self.image = testSprites["Player"]
        self.screen = pg.display.get_surface()
        self.rect = self.image.get_rect(topleft=self.startingPos)
        self.hitbox = self.rect.inflate(0, 0)

        self.coins = 0

        self.mood = "Idle"

        self.collisionSprites = collidable_sprites
        self.pickAbleItems = pickableItems
        self.createEquipmentTile = useEquipmentTile
        self.dialogueSystem = dialogueSystem

        self.inventory = Inventory(self)
        self.displayInventory = False

        self.facingDirection = "Down"
        self.state = "Down_idle"
        self.importSprites()

        self.itemIndex = 0
        self.equippedItem = equipmentItems[self.itemIndex]

        self.timeManager = timeManager

        self.usingItem = False

        self.interactableObjects = interactableObjects

        self.laidToBed = False


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

        animation = self.animations_States[self.state]
        self.frame_index += self.eqpActionAnimationTime if self.usingItem else self.walkingAnimationTime

        notMoving = self.direction.x == 0 and self.direction.y == 0

        if self.frame_index >= len(animation):
            self.frame_index = 0 if not self.usingItem else len(animation) - 1

            usingEquipment = not "idle" in self.state and notMoving
            if usingEquipment:
                self.createEquipmentTile()
                self.usingItem = False

        self.image = animation[int(self.frame_index)].convert_alpha()

        self.rect = self.image.get_rect(center=self.hitbox.center)


    @staticmethod
    def getState(function, value, state):
        return function(value, state)

    def updateInventory(self,item):
        self.inventory.update(item)

    def renderInventory(self):
        if self.displayInventory:
            self.displayInventory = False
        else:
            self.displayInventory = True

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

        self.hitbox.x += self.direction.x * speed if self.direction.x > 0 else self.direction.x * speed / 1.5
        self.checkWallCollision("Horizontal")
        self.hitbox.y += self.direction.y * speed if self.direction.y > 0 else self.direction.y * speed / 1.5
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

    def useItemEquipped(self):
        canUseItem = not self.laidToBed and not self.dialogueSystem.dialogueActive
        if canUseItem:
            inventory = self.inventory
            notMoving = self.direction.x == 0 and self.direction.y == 0
            if notMoving and self.inventory.selectingEquipmentSlot():
                self.frame_index = 0

                self.usingItem = True
                if inventory.currentItems[inventory.itemIndex]["name"] in equipmentItems:
                    self.state = f"{self.inventory.getCurrentSelectedItem()}_{self.facingDirection}"
                elif inventory.currentItems[inventory.itemIndex]["name"] in seedItems:
                    self.state = f"{self.facingDirection}_idle"
                    self.createEquipmentTile()
                    self.usingItem = False

    def getInputs(self):
        keys = pg.key.get_pressed()
        allowedToMove = not self.usingItem and not self.laidToBed and not self.dialogueSystem.dialogueActive
        if allowedToMove:
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

    def resetLives(self):
        self.lives = self.maxLives
    def checkifSleepy(self,dayTime):
        if self.mood != "Happy" :
            if dayTime is False or self.laidToBed:
                self.mood = "Sleepy"
            else:
                self.mood = "Idle"

    def updateMood(self):
        if self.mood == "Happy":
            if self.currentTime - self.moodTickTime > 300:
                self.mood = "Idle"

    def update(self):
        self.currentTime = pg.time.get_ticks()

        if self.displayInventory:
            self.inventory.display()

        else:
            self.updateMood()
            self.getInputs()
            self.movement(playerSpeed)
            self.animate()
            self.interact()




