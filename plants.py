import pygame as pg
from settings import *
from enum import Enum
from abc import ABC, abstractmethod


class PlantTileState(Enum):
    PhaseOne = 1
    PhaseTwo = 2
    PhaseThree = 3
    PhaseFour = 4


class StateCache:
    def __init__(self, main):
        self.main = main
        self.plantStates = PlantTileState

        self.states = {
            self.plantStates.PhaseOne: PlantTilePhaseOne(self, self.main),
            self.plantStates.PhaseTwo: PlantTilePhaseTwo(self, self.main),
            self.plantStates.PhaseThree: PlantTilePhaseThree(self, self.main),
            self.plantStates.PhaseFour: PlantTilePhaseFour(self, self.main)
        }

    def PhaseOne(self):
        return self.states[self.plantStates.PhaseOne]

    def PhaseTwo(self):
        return self.states[self.plantStates.PhaseTwo]

    def PhaseThree(self):
        return self.states[self.plantStates.PhaseThree]

    def PhaseFour(self):
        return self.states[self.plantStates.PhaseFour]


class BaseState(ABC):

    @abstractmethod
    def EnterState(self):
        pass

    @abstractmethod
    def UpdateState(self):
        pass

    @abstractmethod
    def CheckSwitchState(self):
        pass

    @abstractmethod
    def ExitState(self):
        pass

    def __init__(self, stateCache, main):
        self.stateCache = stateCache
        self.main = main

    def SwitchState(self, newState):
        self.ExitState()
        newState.EnterState()
        self.main.currentState = newState


class PlantTilePhaseOne(BaseState):

    def EnterState(self):
        self.main.currentPhase = "PhaseOne"

    def UpdateState(self):
        if self.main.currentPlant is not None:
            self.main.image = self.main.currentPlant[f"{self.main.currentPhase}Sprite"]

    def CheckSwitchState(self):
        pass

    def ExitState(self):
        pass


class PlantTilePhaseTwo(BaseState):

    def EnterState(self):
        pass

    def UpdateState(self):
        pass

    def CheckSwitchState(self):
        pass

    def ExitState(self):
        pass


class PlantTilePhaseThree(BaseState):

    def EnterState(self):
        pass

    def UpdateState(self):
        pass

    def CheckSwitchState(self):
        pass

    def ExitState(self):
        pass


class PlantTilePhaseFour(BaseState):

    def EnterState(self):
        pass

    def UpdateState(self):
        pass

    def CheckSwitchState(self):
        pass

    def ExitState(self):
        pass


class SoilTile(pg.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.type = "Soil"
        self.untiledSprite = plantTileSprites["Soil"]["untiledSprite"].convert()
        self.tiledSprite = plantTileSprites["Soil"]["tiledSprite"].convert()
        self.wateredSprite = plantTileSprites["Soil"]["WateredSprite"].convert_alpha()
        self.image = self.untiledSprite
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.currentPlant = None
        self.currentPhase = None
        self.tilted = False
        self.watered = False

    def update(self):
        self.currentPlant.NextPhase()
        self.watered = False
        self.image = self.tiledSprite


class PlantTile(pg.sprite.Sprite):
    def __init__(self, pos, group, data,soil):
        super().__init__(group)

        self.type = "Plants"
        self.data = data
        self.image = self.data["PhaseOneSprite"]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.soil = soil

        self.currentPhase = 1

        self.phases = {
            1: self.PhaseOne,
            2: self.PhaseTwo,
            3: self.PhaseThree,
            4: self.PhaseFour
        }

    def NextPhase(self):
        self.currentPhase += 1
        if self.currentPhase <= len(self.phases):
            getCurrentPhase = self.phases.get(self.currentPhase)
            getCurrentPhase()
        else:
            self.ProduceCrop()

    def PhaseOne(self):
        self.image = self.data["PhaseOneSprite"]

    def PhaseTwo(self):
        self.image = self.data["PhaseTwoSprite"]

    def PhaseThree(self):
        self.image = self.data["PhaseThreeSprite"]

    def PhaseFour(self):
        self.image = self.data["PhaseFourSprite"]

    def ProduceCrop(self):
        self.soil.currentPlant = None
        self.kill()


