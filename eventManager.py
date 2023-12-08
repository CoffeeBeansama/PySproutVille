import pygame as pg

class EventHandler:
    def handleKeyBoardInput(self):
        keys = pg.key.get_pressed()
        
        self.pressingUp = True if keys[pg.K_UP] else False
        self.pressingDown = True if keys[pg.K_DOWN] else False
        self.pressingLeft = True if keys[pg.K_LEFT] else False
        self.pressingRight = True if keys[pg.K_RIGHT] else False

        self.pressingEquipment = True if keys[pg.K_SPACE] else False


    def pressingUpButton(self):
        return self.pressingUp

    def pressingDownButton(self):
        return self.pressingDown

    def pressingLeftButton(self):
        return self.pressingLeft

    def pressingRightButton(self):
        return self.pressingRight

    def pressingEquipmentButton(self):
        return self.pressingEquipment
