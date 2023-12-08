import pygame as pg

class EventHandler(object):
    
    pressingEquipment = False

    @staticmethod
    def handleKeyBoardInput():
        keys = pg.key.get_pressed()
        
        print("this")
        pressingUp = True if keys[pg.K_UP] else False
        pressingDown = True if keys[pg.K_DOWN] else False
        pressingLeft = True if keys[pg.K_LEFT] else False
        pressingRight = True if keys[pg.K_RIGHT] else False

        pressingEquipment = True if keys[pg.K_SPACE] else False
        
    
    @staticmethod
    def pressingUpButton():
        return EventHandler.pressingUp
    
    @staticmethod
    def pressingDownButton():
        return EventHandler.pressingDown

    @staticmethod
    def pressingLeftButton(self):
        return EventHandler.pressingLeft

    @staticmethod
    def pressingRightButton():
        return EventHandler.pressingRight
    
    @staticmethod
    def pressingEquipmentButton():
        return EventHandler.pressingEquipment
