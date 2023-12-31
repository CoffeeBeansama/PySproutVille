import random
import pygame as pg
from support import loadSprite
from settings import *
from objects import *
from timer import Timer,AnimalTimer
from support import import_folder
import random
from abc import ABC,abstractmethod
from eventManager import EventHandler


class Merchant(InteractableObjects):
    def __init__(self,group,interactableSprites,dialogue,dynamicUi):
        super().__init__(group)

        self.type = "npc"
        self.dialogueId = "Merchant"
        self.startingPos = (800, 795)

        self.spritePath = "Sprites/Merchant.png"

        self.dialogueSystem = dialogue
        self.dynamicUi = dynamicUi
        self.image = pg.image.load(self.spritePath).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.startingPos)
        self.hitbox = self.rect.inflate(-40,-40)

        self.interactRect = self.image.get_rect(topleft=(self.startingPos[0], self.startingPos[1] + tileSize))
        self.interactHitbox = self.interactRect.inflate(-40,-40)

        self.interactableSprites = interactableSprites
        self.add(self.interactableSprites)

    def interact(self):
        if EventHandler.pressingInteractKey():
            if not self.interacted:
                self.dialogueSystem.startDialogue(self.dialogueId)
                self.interacted = True
            else:
                return

    def disengage(self):
        self.interacted = False


class AnimalStateSprite(pg.sprite.Sprite):
    def __init__(self,image,pos,group):
        super().__init__(group)
        self.type = "sprite"
        self.image = loadSprite(image,(tileSize,tileSize)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


class FarmAnimals(pg.sprite.Sprite,ABC):
    def __init__(self,name,pos,group,collisionSprites,pickAbleSprites):
        super().__init__(group)

        self.screen = pg.display.get_surface()
        self.group = group
        self.collisionSprites = collisionSprites
        self.pickAbleSprites = pickAbleSprites

        self.pos = pos
        self.imagePath = f"Sprites/{name}/Idle/0.png"
        self.image = pg.image.load(self.imagePath).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(10, 0)

        self.rect.center = self.hitbox.center

        self.direction = pg.math.Vector2()
        self.currentState = 1

        self.maximumLives = 5
        self.lives = self.maximumLives

        self.states = {
            -1: self.IdleState,
            1: self.RoamState
        }

        self.chooseDirection = False
        self.walkSpeed = 1
        self.availableDirections = ["Up", "Down", "Left", "Right"]
        self.chosenDirection = "Left"

        self.walkDirection = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0),
        }

        self.currentAnimationState = "Walk"
        self.walkingAnimationTime = 1 / 12
        self.idleAnimationTime = 1 / 120
        self.frameIndex = 0

        self.eaten = False
        self.stateSprite = None

        self.ImportSprites(name)
        self.timer = Timer(800,self.disableStateSprite)


    def ImportSprites(self,name):
        imagePath = f"Sprites/{name}/"
        self.animationStates = {
            "Idle" : [],
            "Walk" : []
        }

        for animation in self.animationStates.keys():
            full_path = imagePath + animation
            self.animationStates[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animationStates[self.currentAnimationState]
        self.frameIndex += self.idleAnimationTime if self.currentState == -1 else self.walkingAnimationTime

        if self.frameIndex >= len(animation):
            self.frameIndex = 0

        self.image = animation[int(self.frameIndex)]
        self.image = pg.transform.flip(self.image, True, False) if self.direction.x < 0 else pg.transform.flip(
            self.image, False, False)
        self.rect = self.image.get_rect(topleft=self.hitbox.center)


    def feed(self):
        if not self.eaten:
            self.eaten = True
            if self.lives < self.maximumLives:
                self.lives += 1
            self.stateSprite = AnimalStateSprite(animalStateSprites[self.lives],self.pos, self.group[0])
            return

    def Eaten(self):
        if self.eaten:
            return True
        else:
            return False

    def checkHealth(self):
        if self.lives < 1:
            self.kill()

    def disableStateSprite(self):
        self.stateSprite.kill()
        self.stateSprite = None

    def getCurrentState(self):
        match self.currentState:
            case -1:
                self.IdleState()
            case 1:
                self.RoamState()

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

    def movement(self,speed):
        self.hitbox.x += self.direction.x * speed
        self.checkWallCollision("Horizontal")
        self.hitbox.y += self.direction.y * speed
        self.checkWallCollision("Vertical")
        self.rect.center = self.hitbox.center

    @abstractmethod
    def IdleState(self):
        pass

    @abstractmethod
    def RoamState(self):
        pass

    @abstractmethod
    def produce(self):
        pass

    @abstractmethod
    def update(self):
        pass


class Egg(PickAbleItems):
    def __init__(self,pos,group,pickAbleSprites,data=None):
        super().__init__(pos,group,data)
        self.type = "item"

        self.imagePath = spritePath + "Egg.png"
        self.image = pg.transform.scale(pg.image.load(self.imagePath),(tileSize,tileSize)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

        self.pickAbleSprites = pickAbleSprites
        self.add(self.pickAbleSprites)


class Chicken(FarmAnimals):
    def __init__(self,name,pos,group,collisionSprites,pickAbleSprites):
        super().__init__(name,pos,group,collisionSprites,pickAbleSprites)
        self.type = "Chicken"
        self.animalTimer = AnimalTimer([random.randint(3000,8000),random.randint(500,1000)])

    def IdleState(self):
        self.chooseDirection = False
        self.currentAnimationState = "Idle"
        self.walkSpeed = 0

    def RoamState(self):
        self.walkSpeed = 1
        if not self.chooseDirection:
            self.chosenDirection = random.choice(self.availableDirections)
            self.currentAnimationState = "Walk"
            self.chooseDirection = True

        newDirection = pg.math.Vector2(self.walkDirection.get(self.chosenDirection))
        self.direction = newDirection


    def produce(self):
        if self.Eaten():
            Egg(self.rect.topleft,self.group,self.pickAbleSprites)
            self.eaten = False
        else:
            self.lives -= 1
            self.checkHealth()
            self.eaten = False
        return

    def update(self):
        self.animalTimer.update()
        self.timer.update()
        self.animate()

        if self.stateSprite is not None:
            self.stateSprite.rect.centerx = self.rect.centerx - 8
            self.stateSprite.rect.centery = self.rect.centery - 25

            if not self.timer.activated:
                self.timer.activate()

        if not self.animalTimer.activated:
            self.currentState *= -1

            self.animalTimer.activate()

        self.getCurrentState()
        self.movement(self.walkSpeed)


class Milk(PickAbleItems):
    def __init__(self,pos,group,pickAbleSprites,data=None):
        super().__init__(pos,group,data)

        self.type = "item"
        self.imagePath = spritePath + "Milk.png"
        self.image = pg.transform.scale(pg.image.load(self.imagePath),(tileSize,tileSize)).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

        self.pickAbleSprites = pickAbleSprites
        self.add(self.pickAbleSprites)


class Cow(FarmAnimals):
    def __init__(self,name,pos,group,collisionSprites,pickAbleSprites):
        super().__init__(name,pos,group,collisionSprites,pickAbleSprites)

        self.type = "Cow"
        self.animalTimer = AnimalTimer([random.randint(3000, 8000), random.randint(500, 1000)])
        self.hitbox = self.rect.inflate(0, 3)
        self.walkingAnimationTime = 1 / 12
        self.idleAnimationTime = 1 / 12

    def IdleState(self):
        self.walkSpeed = 0
        self.chooseDirection = False
        self.currentAnimationState = "Idle"

    def RoamState(self):
        self.walkSpeed = 1
        if not self.chooseDirection:
            self.chosenDirection = random.choice(self.availableDirections)
            self.currentAnimationState = "Walk"
            self.chooseDirection = True

        newDirection = pg.math.Vector2(self.walkDirection.get(self.chosenDirection))
        self.direction = newDirection

    def produce(self):
        if self.Eaten():
            Milk(self.rect.topleft,self.group,self.pickAbleSprites)
            self.eaten = False
        else:
            self.lives -= 1
            self.eaten = False
        return


    def update(self):
        self.timer.update()
        self.animalTimer.update()
        self.animate()

        if self.stateSprite is not None:
            self.stateSprite.rect.centerx = self.rect.centerx - 12
            self.stateSprite.rect.centery = self.rect.centery -25
            if not self.timer.activated:
                self.timer.activate()

        if not self.animalTimer.activated:
            self.currentState *= -1
            self.animalTimer.activate()

        self.getCurrentState()
        self.movement(self.walkSpeed)
