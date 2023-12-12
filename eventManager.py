import pygame as pg


class EventHandler(object):
    
    pressingUp = False
    pressingDown = False
    pressingRight = False
    pressingLeft = False
    
    pressingInteract = False
    
    pressingInventoryUp = False
    pressingInventoryDown = False
    pressingInventoryLeft = False
    pressingInventoryRight = False


    @staticmethod
    def handleKeyBoardInput():
        keys = pg.key.get_pressed()
        
        EventHandler.pressingUp = True if keys[pg.K_UP] else False
        EventHandler.pressingDown = True if keys[pg.K_DOWN] else False
        EventHandler.pressingLeft = True if keys[pg.K_LEFT] else False
        EventHandler.pressingRight = True if keys[pg.K_RIGHT] else False

        EventHandler.pressingInteract = True if keys[pg.K_x] else False

        EventHandler.pressingInventoryUp = True if keys[pg.K_w] else False
        EventHandler.pressingInventoryDown = True if keys[pg.K_s] else False
        EventHandler.pressingInventoryLeft = True if keys[pg.K_a] else False
        EventHandler.pressingInventoryRight = True if keys[pg.K_d] else False
             

    def pressingUpKey():
        return EventHandler.pressingUp
    
    def pressingDownKey():
        return EventHandler.pressingDown

    def pressingLeftKey():
        return EventHandler.pressingLeft

    def pressingRightKey():
        return EventHandler.pressingRight
    
    def pressingInteractKey():
        return EventHandler.pressingInteract

    def pressingInventoryUpKey():
        return EventHandler.pressingInventoryUp

    def pressingInventoryDownKey():
        return EventHandler.pressingInventoryDown

    def pressingInventoryLeftKey():
        return EventHandler.pressingInventoryLeft

    def pressingInventoryRightKey():
        return EventHandler.pressingInventoryRight
