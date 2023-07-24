import pygame as pg

WIDTH = 800
HEIGHT = 600
FPS = 60

uiPath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/"

playerSpeed = 4
slotScale = (55, 55)

def loadImage(imagePath):
    newImage = pg.transform.scale(pg.image.load(imagePath),slotScale)
    return newImage



itemData = {
    "Hoe":{"name": "Hoe","uiSprite": loadImage(f"{uiPath}Hoe.png"),"uiSpriteSelected": loadImage(f"{uiPath}HoeSelected.png"),},
    "Axe": {"name": "Axe","uiSprite": loadImage(f"{uiPath}Axe.png"),"uiSpriteSelected": loadImage(f"{uiPath}AxeSelected.png"),},
    "WateringCan": {"name": "WateringCan","uiSprite": loadImage(f"{uiPath}WateringCan.png"),"uiSpriteSelected": loadImage(f"{uiPath}WateringCanSelected.png"),},



}

slotSprites = {1: "Hoe", 2: "Axe", 3: "WateringCan", 4: "EmptySlot",5:"Apple",
                6: "HoeSelected", 7: "AxeSelected", 8: "WateringCanSelected", 9: "EmptySlotSelected",10:"AppleSelected"
               }

tileSize = 64   
testSprites = {"Wall": "Sprites/test/wall.png","Player": "Sprites/test/player.png",
               "Apple": "Sprites/Sprout Lands - Sprites - Basic pack/Objects/AppleFruit Final.png"
               }

uiSprites = {"InventoryHolder":"Sprites/Sprout Lands - Sprites - Basic pack/Ui/Inventory.png",
             "Slot": "Sprites/Sprout Lands - Sprites - Basic pack/Ui/EmptySlot.png"}

equippableItems = ["Hoe","Axe","WateringCan"]


map = [
    ["W","W","W","W","W","W","W","W","W","W","W"],
    ["W"," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," ","P"," "," "," ","A"," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," ","W"],
    ["W","W","W","W","W","W","W","W","W","W","W"],

]

