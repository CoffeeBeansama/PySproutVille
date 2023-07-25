import pygame as pg

tileSize = 64
WIDTH = 800
HEIGHT = 600
FPS = 60

spritePath = "Sprites/Sprout Lands - Sprites - Basic pack/Objects/"
uiPath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/"

playerSpeed = 4
slotScale = (55, 55)
itemScale = (24,24)



def loadSprite(imagePath, scale):
    newImage = pg.transform.scale(pg.image.load(imagePath),scale)
    return newImage



itemData = {
    "Hoe":{
        "name": "Hoe",
        "uiSprite": loadSprite(f"{uiPath}Hoe.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}HoeSelected.png", slotScale),
         },
    "Axe": {
        "name": "Axe",
        "uiSprite": loadSprite(f"{uiPath}Axe.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}AxeSelected.png", slotScale),
         },
    "WateringCan": {
        "name": "WateringCan",
        "uiSprite": loadSprite(f"{uiPath}WateringCan.png", slotScale),
        "uiSpriteSelected":loadSprite(f"{uiPath}WateringCanSelected.png", slotScale),
        },
    "Apple": {
        "name": "Apple",
        "sprite":  loadSprite(f"{spritePath}Apple.png",itemScale),
        "uiSprite": loadSprite(f"{uiPath}Apple.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}AppleSelected.png", slotScale)
         }
}

slotSprites = {1: "Hoe", 2: "Axe", 3: "WateringCan", 4: "EmptySlot",5:"Apple",
                6: "HoeSelected", 7: "AxeSelected", 8: "WateringCanSelected", 9: "EmptySlotSelected",10:"AppleSelected"
               }


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

