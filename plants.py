import pygame as pg
from settings import *
from enum import Enum
from abc import ABC,abstractmethod


class PlantTileState(Enum):
    PhaseOne: 0
    PhaseTwo: 1
    PhaseThree: 3
    PhaseFour: 4


class StateCache:
    def __init__(self,main):
        self.main = main
        self.plantStates = PlantTileState

        self.states = {
            self.plantStates.PhaseOne: PlantTilePhaseOne(self,self.main),
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
        pass

    def UpdateState(self):
        pass

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


class PlantTile(pg.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)

        self.type = "object"
        self.untiledSprite = plantTileSprites["Soil"]["untiledSprite"].convert()
        self.tiledSprite = plantTileSprites["Soil"]["tiledSprite"].convert()
        self.image = self.untiledSprite
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)

        self.currentPlant = None

        self.stateCache = StateCache(self)
        self.currentState = self.stateCache.PhaseOne()
        self.currentState.EnterState()