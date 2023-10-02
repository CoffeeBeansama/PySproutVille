import pickle
import os
from settings import *
from plants import *
from tree import *
from npc import *

class SaveLoadSystem:
    def __init__(self,fileExtension,folder,player,treesList,chestInventory,plantList,appleList,soilList,animalsList,pickAbleItemSprites,
                 visibleSprites,timeManager,soilTileSprites,animalCollider
                 ):

        self.fileExtension = fileExtension
        self.folder = folder

        self.player = player
        self.treeList = treesList
        self.chestInventory = chestInventory
        self.plantList = plantList
        self.appleList = appleList
        self.soilList = soilList
        self.animalsList = animalsList
        self.pickAbleItemSprites = pickAbleItemSprites
        self.visibleSprites = visibleSprites
        self.timeManager = timeManager
        self.soilTileSprites = soilTileSprites
        self.animalCollider = animalCollider

        self.gameState = {
            "Player": self.player.data,
            "Plants": {},
            "Trees": {},
            "Apples": {},
            "Soil": {},
            "PickableItems": {},
            "Animals": {},
            "PlayerInventorySlots": {},
            "ItemChestItems": {},
            "ItemChestSlots": {"itemName": {}},

        }

        self.defaultGameState = {
            "Player": player.defaultData,
            "Plants": {},
            "Trees": {},
            "Apples": {},
            "Soil": {},
            "PickableItems": {},
            "Animals": {},
            "PlayerInventorySlots": {},
            "ItemChestItems": {},
            "ItemChestSlots": {"itemName": {}}

        }

#region saving game data
    def savePlayerData(self):
        player = self.player
        player.currentItemsHolding.clear()
        player.data["Position"] = player.hitbox.center
        player.data["Coins"] = player.coins

        for items in player.inventory.currentItems:
            player.currentItemsHolding.append(items["name"] if items is not None else None)
            player.data["Items"] = player.currentItemsHolding
        for index, slots in enumerate(player.inventory.slotList):
            self.gameState["PlayerInventorySlots"][index] = slots.stackNum
        self.gameState["Player"] = player.data

    def saveTreeData(self):
        for index, trees in enumerate(self.treeList):
            self.gameState["Trees"][index] = trees.cuttedDown

    def savePickableSprites(self):
        for index, items in enumerate(self.pickAbleItemSprites):
            if items.type == "Apple":
                savedApple = self.gameState["PickableItems"][f"{items.type}{index}"] = {}
                savedApple["Name"] = items.data["name"]
                savedApple["Position"] = items.rect.topleft

    def saveSoilData(self):
        for index, soil in enumerate(self.soilList):
            savedSoil = self.gameState["Soil"][f"{soil.type}{index}"] = {}
            savedSoil["Position"] = soil.rect.topleft
            savedSoil["CurrentState"] = soil.currentState
            savedSoil["Watered"] = soil.watered
            savedSoil["Tilted"] = soil.tilted
            savedSoil["IndexId"] = soil.indexId
            savedSoil["Planted"] = soil.planted

    def savePlantData(self):
        for index, plants in enumerate(self.plantList):
            if plants.type == "Plants":
                savedPlant = self.gameState["Plants"][f"{plants.type}{index}"] = {}
                savedPlant["Name"] = plants.data["name"]
                savedPlant["Position"] = plants.rect.topleft
                savedPlant["CurrentPhase"] = plants.currentPhase

        for index, apples in enumerate(self.appleList):
            if apples.type == "Apple":
                savedApple = self.gameState["Apples"][f"{apples.type}{index}"] = {}
                savedApple["Name"] = apples.data["name"]
                savedApple["IndexId"] = apples.IndexId
                savedApple["Position"] = apples.rect.topleft
                savedApple["CurrentPhase"] = apples.currentPhase

    def saveAnimalData(self):
        for index, animals in enumerate(self.animalsList):
            savedAnimal = self.gameState["Animals"][f"{animals.type}{index}"] = {}
            savedAnimal["Name"] = animals.type
            savedAnimal["Position"] = animals.rect.topleft

    def saveItemChestData(self):
        itemChest = self.chestInventory
        for index, items in enumerate(itemChest.currentItemHolding):
            self.gameState["ItemChestItems"][index] = items["name"] if items is not None else None

        for index, slots in enumerate(itemChest.slotList.values()):
            savedSlots = self.gameState["ItemChestSlots"][slots.index] = {}
            savedSlots["index"] = slots.index
            savedSlots["stack"] = slots.stackNum



    def saveGameState(self):
        for items in self.gameState.values():
            items.clear()

        self.savePlayerData()
        self.saveTreeData()
        self.savePickableSprites()
        self.saveSoilData()
        self.savePlantData()
        self.saveAnimalData()
        self.saveItemChestData()

        self.saveGameData(self.gameState,"gameState")
#endregion


#region loading game data

    def loadPlantData(self):
        for plantIndex, plants in enumerate(self.gameState["Plants"].values()):
            if plants["Name"] in seedItems:
                plant = PlantTile(plants["Position"], [self.visibleSprites], itemData[plants["Name"]],
                                  self.pickAbleItemSprites, self.timeManager, self.soilTileSprites)
                plant.LoadPhase(plants["CurrentPhase"])
                self.plantList.append(plant)

        for appleIndex, apple in enumerate(self.gameState["Apples"].values()):
            self.appleList[appleIndex].rect.topleft = apple["Position"]
            self.appleList[appleIndex].currentPhase = apple["CurrentPhase"]
            self.appleList[appleIndex].loadState()

    def loadTreeData(self):
        for index, treeData in enumerate(self.gameState["Trees"].values()):
            self.treeList[index].loadState(treeData)

    def loadSoilData(self):
        for index, soil in enumerate(self.gameState["Soil"].values()):
            currentSoil = self.soilList[soil["IndexId"]]
            currentSoil.rect.topleft = soil["Position"]
            currentSoil.currentState = soil["CurrentState"]
            currentSoil.tilted = soil["Tilted"]
            currentSoil.watered = soil["Watered"]
            currentSoil.indexId = soil["IndexId"]
            currentSoil.planted = soil["Planted"]
            currentSoil.loadState()

    def loadPickableSprites(self):
        for itemIndex, item in enumerate(self.gameState["PickableItems"].values()):
            if item["Name"] == "Apple":
                self.pickAbleItemSprites.add(
                    AppleItem(item["Position"], self.visibleSprites, itemData["Apple"], self.pickAbleItemSprites))

    def loadAnimalData(self):
        for index, animals in enumerate(self.gameState["Animals"].values()):
            if animals["Name"] == "Chicken":
                newChicken = Chicken(animals["Name"], animals["Position"], [self.visibleSprites], self.animalCollider,
                                     self.pickAbleItemSprites)
                self.animalsList.append(newChicken)
            if animals["Name"] == "Cow":
                newCow = Cow(animals["Name"], animals["Position"], [self.visibleSprites], self.animalCollider,
                             self.pickAbleItemSprites)
                self.animalsList.append(newCow)

    def loadItemChestData(self):
        for index, item in enumerate(self.gameState["ItemChestItems"].values()):
            self.chestInventory.loadCurrentItems(index, item)
        self.chestInventory.loadSlotsData()
        try:
            for index, data in enumerate(self.gameState["ItemChestSlots"].keys()):
                self.chestInventory.loadSlotsStack(data, self.gameState["ItemChestSlots"][data]["stack"])
        except:
            pass

    def loadPlayerData(self):
        player = self.player
        player.coins = self.gameState["Player"]["Coins"]
        player.hitbox.center = self.gameState["Player"]["Position"]
        try:
            for index, items in enumerate(self.gameState["Player"]["Items"]):
                player.inventory.loadItems(index, items)
            for index, data in enumerate(self.gameState["PlayerInventorySlots"].values()):
                player.inventory.loadSlotStacks(index, data)
        except:
            pass


    def loadGameState(self):
        self.gameState = self.loadGameData("gameState", self.defaultGameState)
        self.loadPlantData()
        self.loadTreeData()
        self.loadSoilData()
        self.loadPickableSprites()
        self.loadAnimalData()
        self.loadItemChestData()
        self.loadPlayerData()

#endregion


    def saveData(self,data,name):
        dataFile = open(f"{self.folder}/{name}{self.fileExtension}","wb")
        pickle.dump(data,dataFile)

    def loadData(self,name):
        dataFile = open(f"{self.folder}/{name}{self.fileExtension}", "rb")
        data = pickle.load(dataFile)
        return data

    def checkFileExists(self,name):
        return os.path.exists(f"{self.folder}/{name}{self.fileExtension}")

    def loadGameData(self,fileToLoad,defaultData):
        if self.checkFileExists(fileToLoad):
            return self.loadData(fileToLoad)
        else:return defaultData


    def saveGameData(self,dataToSave,fileNames):
        self.saveData(dataToSave,fileNames)