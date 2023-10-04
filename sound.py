
import pygame as pg
from pygame import mixer


pg.init()

sfx = {
    "Coin": mixer.Sound("SFX/Gold.wav"),
    "Hoe": mixer.Sound("SFX/hoe.wav"),
    "Axe": mixer.Sound("SFX/axe.wav"),
    "Purchase": mixer.Sound("SFX/purchase.wav"),
    "No Cash": mixer.Sound("SFX/noCash.wav"),
    "Chest": mixer.Sound("SFX/chest.wav"),
    "Door Open": mixer.Sound("SFX/Door Open.mp3"),
    "Door Close": mixer.Sound("SFX/Door Close.mp3"),
    "Seed": mixer.Sound("SFX/seed.mp3"),
    "WateringCan": mixer.Sound("SFX/watering.mp3"),
    "Selection" : mixer.Sound("SFX/Menu/Selection.wav"),
    "ItemSwap": mixer.Sound("SFX/Menu/ItemSwap.mp3"),
    "OpenInventory": mixer.Sound("SFX/Menu/OpenInventory.mp3"),
    "CloseInventory": mixer.Sound("SFX/Menu/CloseInventory.mp3"),
    "Berry": mixer.Sound("SFX/seed.mp3"),

}

for sounds in sfx.values():
    sounds.set_volume(0.3)

sfx["Chest"].set_volume(0.05)
sfx["Door Open"].set_volume(0.1)
sfx["Door Close"].set_volume(0.1)

inventorySfx = [sfx["Selection"],sfx["ItemSwap"],sfx["OpenInventory"],sfx["CloseInventory"]]

for i in inventorySfx:
    i.set_volume(0.3)


def playBGM(bgm):
    if bgm == "level":
        mixer.music.load("SFX/BGM/daybgm.ogg")
    elif bgm == "Menu":
        pass

    mixer.music.play(-1)
    mixer.music.set_volume(0.2)

def playSound(sound):
    player = pg.mixer.Sound
    player.play(sfx[sound])
