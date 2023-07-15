import pygame as pg
from settings import *
from entity import Entity
from support import import_folder


class Player(Entity):
    def __init__(self,image,group,collidable_sprites,level):
        super().__init__(group)

        self.level = level
        self.startingPos = (100,100)

        self.frame_index = 0
        self.animation_time = 1 / 6

        self.image = pg.image.load(image).convert_alpha()

        self.rect = self.image.get_rect(topleft=self.startingPos)
        self.hitbox = self.rect.inflate(0, 0)
        self.collisionSprites = collidable_sprites
        self.faceDirection = "Down"
        self.importSprites()

    def importSprites(self):
        player_path = "Sprites/Player/"

        self.animations_States = {'Up': [], 'Down': [], 'Left': [], 'Right': [],
                                  "Up_idle": [], "Down_idle": [], "Left_idle": [], "Right_idle": []
                                  }

        for animation in self.animations_States.keys():
            full_path = player_path + animation
            self.animations_States[animation] = import_folder(full_path)

    def animate(self):
        # increments the frame index when receiving input
        # when frame index reaches to maximum it loops over again to repeat the animation cycle

        animation = self.animations_States[self.faceDirection]
        self.frame_index += self.animation_time

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image = pg.transform.scale(self.image,(124,124))
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def getState(self,function,value,state):
        return function(value,state)

    def horizontalDirection(self, value, state):
        self.direction.x = value
        self.direction.y = 0
        self.faceDirection = state

    def verticalDirection(self, value, state):
        self.direction.x = 0
        self.direction.y = value
        self.faceDirection = state

    def movement(self,speed):
        self.rect.center += self.direction * speed
        self.hitbox.x += self.direction.x * speed
        self.checkCollision("Horizontal")
        self.hitbox.y += self.direction.y * speed
        self.checkCollision("Vertical")
        self.rect.center = self.hitbox.center

    def checkCollision(self,direction):

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

    def idleState(self):
        self.direction.x = 0
        self.direction.y = 0
        if not "idle" in self.faceDirection:
            self.faceDirection = f"{self.faceDirection}_idle"

    def getInputs(self):

        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.getState(self.verticalDirection,-1,"Up")
        elif keys[pg.K_s]:
            self.getState(self.verticalDirection, 1, "Down")
        elif keys[pg.K_a]:
            self.getState(self.horizontalDirection,-1,"Left")
        elif keys[pg.K_d]:
            self.getState(self.horizontalDirection,1,"Right")

        else:
            self.idleState()

    def update(self):
        self.getInputs()
        self.movement(playerSpeed)
        self.animate()





