import pygame as pg
from settings import *
from sound import playSound


class Equipment(pg.sprite.Sprite):
    def __init__(self, group, player):
        super().__init__(group)

        self.type = "Equipment"

        self.equipment = True

        playerItemEquipped = player.inventory.playerCurrentItems[player.inventory.itemIndex]["name"]
        self.playEquipmentSound(playerItemEquipped if playerItemEquipped not in seedItems else "Seed")
        playerDirection = player.facingDirection
        self.image = pg.Surface((10, 10))
        if playerItemEquipped in equipmentItems:
            match playerDirection:
                case "Up": self.rect = self.image.get_rect(midbottom=player.rect.midtop + pg.math.Vector2(0, 16))
                case "Down": self.rect = self.image.get_rect(midtop=player.rect.midbottom - pg.math.Vector2(0, 12))
                case "Left":  self.rect = self.image.get_rect(midright=player.rect.midleft + pg.math.Vector2(16, 8))
                case "Right": self.rect = self.image.get_rect(midleft=player.rect.midright - pg.math.Vector2(16, -8))

        elif playerItemEquipped in seedItems or playerItemEquipped in animalFodders:
            self.rect = self.image.get_rect(center=player.rect.center)
            player.inventory.decreaseItemStack()


    def playEquipmentSound(self,equipmentName):
        playSound(equipmentName)
