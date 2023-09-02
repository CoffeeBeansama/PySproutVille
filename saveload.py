import pickle
import os

class SaveLoadSystem:
    def __init__(self,fileExtension,folder):

        self.fileExtension = fileExtension
        self.folder = folder

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
