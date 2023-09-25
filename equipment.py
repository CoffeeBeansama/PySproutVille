import pygame as pg
from settings import *


class Equipment(pg.sprite.Sprite):
    def __init__(self, group, player):
        super().__init__(group)

        self.type = "Equipment"

        self.equipment = True

        playerItemEquipped = player.inventory.currentItems[player.inventory.itemIndex]["name"]
        playerDirection = player.facingDirection
        self.image = pg.Surface((10, 10))

        if playerItemEquipped in equipmentItems:
            match playerDirection:
                case "Up": self.rect = self.image.get_rect(midbottom=player.rect.midtop + pg.math.Vector2(0, 16))
                case "Down": self.rect = self.image.get_rect(midtop=player.rect.midbottom - pg.math.Vector2(0, 12))
                case "Left":  self.rect = self.image.get_rect(midright=player.rect.midleft + pg.math.Vector2(10, 8))
                case "Right": self.rect = self.image.get_rect(midleft=player.rect.midright - pg.math.Vector2(10, -8))

        elif playerItemEquipped in seedItems:
            self.rect = self.image.get_rect(center=player.rect.center)
            player.inventory.decreaseItemStack()