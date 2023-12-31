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
        "uiSprite": f"{uiPath}Slots/Hoe.png",
        "uiSpriteSelected": f"{uiPath}Slots/HoeSelected.png",
         },
    "Axe": {
        "name": "Axe",
        "uiSprite": f"{uiPath}Slots/Axe.png",
        "uiSpriteSelected": f"{uiPath}Slots/AxeSelected.png",
         },
    "WateringCan": {
        "name": "WateringCan",
        "uiSprite": f"{uiPath}Slots/WateringCan.png",
        "uiSpriteSelected":f"{uiPath}Slots/WateringCanSelected.png",
        },
    "Apple": {
        "name": "Apple",
        "costs": 5,
        "CropSprite":  f"{spritePath}/Plants/Apple/2.png",
        "uiSprite": f"{uiPath}Slots/Apple.png",
        "uiSpriteSelected": f"{uiPath}Slots/AppleSelected.png",
        "PhaseOneSprite": f"{spritePath}/Plants/Apple/1.png",
        "PhaseTwoSprite": f"{spritePath}/Plants/Apple/2.png",
        "PhaseThreeSprite": f"{spritePath}/Plants/Apple/3.png",
        "CollisionSprite": f"{spritePath}/Plants/Apple/collision.png",
         },

    "Wheat":{
        "name": "Wheat",
        "costs": 10,
        "uiSprite": f"{uiPath}Slots/Wheat.png",
        "uiSpriteSelected": f"{uiPath}Slots/WheatSelected.png",
        "PhaseOneSprite": f"{spritePath}/Plants/Wheat/1.png",
        "PhaseTwoSprite": f"{spritePath}/Plants/Wheat/2.png",
        "PhaseThreeSprite": f"{spritePath}/Plants/Wheat/3.png",
        "PhaseFourSprite": f"{spritePath}/Plants/Wheat/4.png",
        "CropSprite": f"{spritePath}/Plants/Wheat/5.png",
        "CollisionSprite": f"{spritePath}/Plants/Wheat/collision.png",

        },
    "Tomato":{
        "name": "Tomato",
        "costs": 15,
        "uiSprite": f"{uiPath}Slots/Tomato.png",
        "uiSpriteSelected": f"{uiPath}Slots/TomatoSelected.png",
        "PhaseOneSprite": f"{spritePath}Plants/Tomato/1.png",
        "PhaseTwoSprite": f"{spritePath}Plants/Tomato/2.png",
        "PhaseThreeSprite": f"{spritePath}Plants/Tomato/3.png",
        "PhaseFourSprite": f"{spritePath}/Plants/Tomato/4.png",
        "CropSprite": f"{spritePath}/Plants/Tomato/5.png",
        "CollisionSprite": f"{spritePath}/Plants/Tomato/collision.png",
    },
    "Berry":{
        "name": "Berry",
        "uiSprite": f"{uiPath}Slots/Berry.png",
        "uiSpriteSelected": f"{uiPath}Slots/BerrySelected.png",

    },
    "Wood":{
        "name": "Wood",
        "CropSprite":  f"{spritePath}/Plants/Wood/Wood.png",
        "uiSprite": f"{uiPath}Slots/Wood.png",
        "uiSpriteSelected": f"{uiPath}Slots/WoodSelected.png",
        "CollisionSprite": f"{spritePath}/Plants/Wood/collision.png",

    },

}


animalStateSprites = {
    6 : f"{uiPath}Icons/special icons/00.png",
    5 : f"{uiPath}Icons/special icons/10.png",
    4 : f"{uiPath}Icons/special icons/20.png",
    3 : f"{uiPath}Icons/special icons/30.png",
    2 : f"{uiPath}Icons/special icons/40.png",
    1 : f"{uiPath}Icons/special icons/50.png",
}

uiSprites = {
             "FaceContainer": f"{uiPath}FaceContainer.png",
             "HeartCoinContainer":f"{uiPath}CoinHeartContainer.png",
             "DefaultFace": f"{uiPath}DefaultFace.png",
             "FullHeart": f"{uiPath}Icons/Heart/Full.png",
             "HalfHeart": f"{uiPath}Icons/Heart/Half.png",
             "EmptyHeart": f"{uiPath}Icons/Heart/Empty.png",
             "DialogueBox": f"{uiPath}Dialouge UI/DialogueBox.png",
             "ChestBackground" :f"{uiPath}ChestBackground.png",
             "MenuBackground" :"Sprites/menuBg.png",
             "MenuImageOverLay" :f"{uiPath}ChestBackground.png",
             "PlayButton": f"{uiPath}PlayButton.png",
             }

animalFodders = ["Berry"]
equipmentItems = ["Hoe", "Axe", "WateringCan"]
stackAbleItems = ["Wheat","Tomato","Wood"]
sellableItems = ["Wheat","Tomato","Apple","Egg","Milk"]
seedItems = ["Wheat","Tomato"]



