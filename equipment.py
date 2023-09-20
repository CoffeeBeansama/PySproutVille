import pygame as pg
from settings import *


class Equipment(pg.sprite.Sprite):
    def __init__(self, group, player):
        super().__init__(group)

        self.type = "Equipment"

        self.equipment = True

        playerItemEquipped = player.inventory.currentItems[player.inventory.itemIndex]["name"]
        playerDirection = player.facingDirection
        self.image = pg.Surface((6, 6))

        if playerItemEquipped in equipmentItems:
            if playerDirection == "Up":
                self.rect = self.image.get_rect(midbottom=player.rect.midtop + pg.math.Vector2(0, 16))
            elif playerDirection == "Down":
                self.rect = self.image.get_rect(midtop=player.rect.midbottom - pg.math.Vector2(0, 12))
            elif playerDirection == "Left":
                self.rect = self.image.get_rect(midright=player.rect.midleft + pg.math.Vector2(18, 5))
            elif playerDirection == "Right":
                self.rect = self.image.get_rect(midleft=player.rect.midright - pg.math.Vector2(18, -5))

        elif playerItemEquipped in seedItems:
            self.rect = self.image.get_rect(center=player.rect.center)
            player.inventory.decreaseItemStack()