import pygame as pg
from support import loadSprite

tileSize = 16
WIDTH = 800
HEIGHT = 600
FPS = 60

spritePath = "Sprites/Sprout Lands - Sprites - Basic pack/Objects/"
uiPath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/"
testSpritePath = "Sprites/test/"

playerSpeed = 3
slotScale = (55, 55)
itemScale = (24,24)

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
         },
    "WheatSeed":{
        "name": "WheatSeed",
        "cost": 10,
        "uiSprite": loadSprite(f"{uiPath}Wheat.png",slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}WheatSelected.png", slotScale),
        "cropUiSprite": loadSprite(f"{uiPath}WheatCrop.png", slotScale),
        "cropUiSpriteSelected": loadSprite(f"{uiPath}WheatCropSelected.png", slotScale),
        "PhaseOneSprite": loadSprite(f"{spritePath}/Plants/Wheat/1.png",(tileSize,tileSize)),
        "PhaseTwoSprite": loadSprite(f"{spritePath}/Plants/Wheat/2.png",(tileSize,tileSize)),
        "PhaseThreeSprite": loadSprite(f"{spritePath}/Plants/Wheat/3.png",(tileSize,tileSize)),
        "PhaseFourSprite": loadSprite(f"{spritePath}/Plants/Wheat/4.png",(tileSize,tileSize)),


        },
    "TomatoSeed":{
        "name": "TomatoSeed",
        "cost": 12,
        "uiSprite": loadSprite(f"{uiPath}Tomato.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}TomatoSelected.png", slotScale),
        "cropUiSprite": loadSprite(f"{uiPath}TomatoCrop.png", slotScale),
        "cropUiSpriteSelected": loadSprite(f"{uiPath}TomatoCropSelected.png", slotScale),
        "PhaseOneSprite": loadSprite(f"{spritePath}Plants/Tomato/1.png",(tileSize,tileSize)),
        "PhaseTwoSprite": loadSprite(f"{spritePath}Plants/Tomato/2.png",(tileSize,tileSize)),
        "PhaseThreeSprite": loadSprite(f"{spritePath}Plants/Tomato/3.png",(tileSize,tileSize)),
        "PhaseFourSprite": loadSprite(f"{spritePath}/Plants/Tomato/4.png",(tileSize,tileSize)),

    },
    "WheatCrop": {
        "name": "WheatCrop",
        "costs": 10,
        "CropSprite": loadSprite(f"{spritePath}/Plants/Wheat/5.png",(tileSize,tileSize)),
        "uiSprite": loadSprite(f"{uiPath}WheatCrop.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}WheatCropSelected.png", slotScale),

    },
    "TomatoCrop": {
        "name": "TomatoCrop",
        "costs": 15,
        "CropSprite": loadSprite(f"{spritePath}/Plants/Tomato/5.png",(tileSize,tileSize)),
        "uiSprite": loadSprite(f"{uiPath}TomatoCrop.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}TomatoCropSelected.png", slotScale),

    }

}

chestSprites = {
    1: loadSprite(f"{spritePath}Chests/1.png",(tileSize,tileSize)),
    2: loadSprite(f"{spritePath}Chests/2.png",(tileSize,tileSize)),
    3: loadSprite(f"{spritePath}Chests/3.png",(tileSize,tileSize)),
    4: loadSprite(f"{spritePath}Chests/4.png",(tileSize,tileSize)),
    5: loadSprite(f"{spritePath}Chests/5.png",(tileSize,tileSize)),

}

plantTileSprites = {
    "Soil":{
        "untiledSprite": loadSprite(f"{spritePath}untiledDirt.png",(tileSize,tileSize)),
        "tiledSprite": loadSprite(f"{spritePath}tiledDirt.png",(tileSize,tileSize)),
        "WateredSprite": loadSprite(f"{spritePath}WateredTiledDirt.png",(tileSize,tileSize)),
    },
}

testSprites = {"Wall": loadSprite(f"{testSpritePath}wall.png",(tileSize,tileSize)),
               "Player": loadSprite(f"{testSpritePath}player.png",(tileSize,tileSize)),
               "Apple": "Sprites/Sprout Lands - Sprites - Basic pack/Objects/AppleFruit Final.png",
               "Chest": loadSprite(f"{spritePath}Chests/1.png",(tileSize,tileSize)),
               "AppleFruit": loadSprite(f"{testSpritePath}AppleFruit.png",(tileSize // 2,tileSize // 2)),
               }

uiSprites = {"InventoryHolder":"Sprites/Sprout Lands - Sprites - Basic pack/Ui/Inventory.png",
             "EmptySlot": loadSprite("Sprites/Sprout Lands - Sprites - Basic pack/Ui/EmptySlot.png",slotScale),
             "EmptySlotSelected": loadSprite("Sprites/Sprout Lands - Sprites - Basic pack/Ui/Slots/EmptySlotSelected.png",slotScale),
             }

equipmentItems = ["Hoe", "Axe", "WateringCan"]
seedItems = ["WheatSeed","TomatoSeed"]
sellableItems = ["WheatCrop","TomatoCrop","Apple"]
groundTiles = ["Soil","Plants"]

map = [
    ["W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
    ["W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"],

]

