import pygame as pg
from support import loadSprite

tileSize = 16
WIDTH = 800
HEIGHT = 600
FPS = 60

spritePath = "Sprites/Sprout Lands - Sprites - Basic pack/Objects/"
uiPath = "Sprites/Sprout Lands - Sprites - Basic pack/Ui/"
testSpritePath = "Sprites/test/"
roofSpritePath = "Sprites/Roof/"

playerSpeed = 2
slotScale = (55, 55)
itemScale = (24,24)

itemData = {
    "Hoe":{
        "name": "Hoe",
        "uiSprite": loadSprite(f"{uiPath}Slots/Hoe.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}Slots/HoeSelected.png", slotScale),
         },
    "Axe": {
        "name": "Axe",
        "uiSprite": loadSprite(f"{uiPath}Slots/Axe.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}Slots/AxeSelected.png", slotScale),
         },
    "WateringCan": {
        "name": "WateringCan",
        "uiSprite": loadSprite(f"{uiPath}Slots/WateringCan.png", slotScale),
        "uiSpriteSelected":loadSprite(f"{uiPath}Slots/WateringCanSelected.png", slotScale),
        },
    "Apple": {
        "name": "Apple",
        "costs": 5,
        "CropSprite":  loadSprite(f"{spritePath}/Plants/Apple/2.png",(tileSize,tileSize)),
        "uiSprite": loadSprite(f"{uiPath}Slots/Apple.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}Slots/AppleSelected.png", slotScale),
        "PhaseOneSprite": loadSprite(f"{spritePath}/Plants/Apple/1.png",(tileSize,tileSize)),
        "PhaseTwoSprite": loadSprite(f"{spritePath}/Plants/Apple/2.png",(tileSize,tileSize)),
        "PhaseThreeSprite": loadSprite(f"{spritePath}/Plants/Apple/3.png",(tileSize,tileSize)),
        "CollisionSprite": loadSprite(f"{spritePath}/Plants/Apple/collision.png",(tileSize,tileSize)),
         },

    "Wheat":{
        "name": "Wheat",
        "costs": 10,
        "uiSprite": loadSprite(f"{uiPath}Slots/Wheat.png",slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}Slots/WheatSelected.png", slotScale),
        "PhaseOneSprite": loadSprite(f"{spritePath}/Plants/Wheat/1.png",(tileSize,tileSize)),
        "PhaseTwoSprite": loadSprite(f"{spritePath}/Plants/Wheat/2.png",(tileSize,tileSize)),
        "PhaseThreeSprite": loadSprite(f"{spritePath}/Plants/Wheat/3.png",(tileSize,tileSize)),
        "PhaseFourSprite": loadSprite(f"{spritePath}/Plants/Wheat/4.png",(tileSize,tileSize)),
        "CropSprite": loadSprite(f"{spritePath}/Plants/Wheat/5.png",(tileSize,tileSize)),
        "CollisionSprite": loadSprite(f"{spritePath}/Plants/Wheat/collision.png",(tileSize,tileSize)),

        },
    "Tomato":{
        "name": "Tomato",
        "costs": 15,
        "uiSprite": loadSprite(f"{uiPath}Slots/Tomato.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}Slots/TomatoSelected.png", slotScale),
        "PhaseOneSprite": loadSprite(f"{spritePath}Plants/Tomato/1.png",(tileSize,tileSize)),
        "PhaseTwoSprite": loadSprite(f"{spritePath}Plants/Tomato/2.png",(tileSize,tileSize)),
        "PhaseThreeSprite": loadSprite(f"{spritePath}Plants/Tomato/3.png",(tileSize,tileSize)),
        "PhaseFourSprite": loadSprite(f"{spritePath}/Plants/Tomato/4.png",(tileSize,tileSize)),
        "CropSprite": loadSprite(f"{spritePath}/Plants/Tomato/5.png",(tileSize,tileSize)),
        "CollisionSprite": loadSprite(f"{spritePath}/Plants/Tomato/collision.png",(tileSize,tileSize)),
    },
    "Berry":{
        "name": "Berry",
        "uiSprite": loadSprite(f"{uiPath}Slots/Berry.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}Slots/BerrySelected.png", slotScale),

    },
    "Wood":{
        "name": "Wood",
        "CropSprite":  loadSprite(f"{spritePath}/Plants/Wood/Wood.png",(tileSize,tileSize)),
        "uiSprite": loadSprite(f"{uiPath}Slots/Wood.png", slotScale),
        "uiSpriteSelected": loadSprite(f"{uiPath}Slots/WoodSelected.png", slotScale),
        "CollisionSprite": loadSprite(f"{spritePath}/Plants/Wood/collision.png",(tileSize,tileSize)),

    },
    "Egg":{
        "name": "Egg",
        "costs": 10,
        "CollisionSprite": loadSprite(f"{spritePath}/EggCollision.png",(tileSize,tileSize)),
    },

    "Milk":{
        "name": "Milk",
        "costs": 35,
        "CollisionSprite": loadSprite(f"{spritePath}MilkCollision.png",(tileSize,tileSize)),
    }



}

soilSprites = {

    "untiledSprite": loadSprite(f"{spritePath}untiledDirt.png",(tileSize,tileSize)),
    "tiledSprite": loadSprite(f"{spritePath}tiledDirt.png",(tileSize,tileSize)),
    "WateredSprite": loadSprite(f"{spritePath}WateredTiledDirt.png",(tileSize,tileSize)),

}


uiSprites = {
             "InventoryHolder":loadSprite(f"{uiPath}Inventory.png",(625,90)),
             "EmptySlot": loadSprite(f"{uiPath}EmptySlot.png",slotScale),
             "EmptySlotSelected": loadSprite(f"{uiPath}Slots/EmptySlotSelected.png",slotScale),
             "FaceContainer":loadSprite(f"{uiPath}FaceContainer.png",(100,100)),
             "HeartCoinContainer":loadSprite(f"{uiPath}CoinHeartContainer.png",(130,130)),
             "DefaultFace": loadSprite(f"{uiPath}DefaultFace.png",(62,62)),
             "FullHeart": loadSprite(f"{uiPath}Icons/Heart/Full.png",(40,38)),
             "HalfHeart": loadSprite(f"{uiPath}Icons/Heart/Half.png",(40,38)),
             "EmptyHeart": loadSprite(f"{uiPath}Icons/Heart/Empty.png",(40,38)),
             "DialogueBox": loadSprite(f"{uiPath}Dialouge UI/DialogueBox.png",(750,150)),
             "ChestBackground" :loadSprite(f"{uiPath}ChestBackground.png",(625,350)),
             "MenuBackground" :loadSprite("Sprites/menuBg.png",(WIDTH,HEIGHT)),
             "MenuImageOverLay" :loadSprite(f"{uiPath}ChestBackground.png",(600,420)),
             "PlayButton": loadSprite(f"{uiPath}PlayButton.png",(180,50))
             }


animalFodders = ["Berry"]
equipmentItems = ["Hoe", "Axe", "WateringCan"]
seedItems = ["Wheat","Tomato"]
stackAbleItems = ["Wheat","Tomato","Wood"]
sellableItems = ["Wheat","Tomato","Apple","Egg","Milk"]
OverlapTiles = ["Soil", "Plants","npc"]




