
import pygame as pg
from pygame import mixer


pg.init()

coinSfx = mixer.Sound("SFX/Gold.wav")
coinSfx.set_volume(0.3)

hoeSfx = mixer.Sound("SFX/hoe.wav")

selectionSfx = mixer.Sound("SFX/Menu/Selection.wav")
itemSwapSfx = mixer.Sound("SFX/Menu/ItemSwap.mp3")
openInventorySfx = mixer.Sound("SFX/Menu/OpenInventory.mp3")
closeInventorySfx = mixer.Sound("SFX/Menu/CloseInventory.mp3")

inventorySfx = [selectionSfx,itemSwapSfx,openInventorySfx,closeInventorySfx]

for sounds in inventorySfx:
    sounds.set_volume(0.2)



equipmentSfx = [hoeSfx]


for sounds in  equipmentSfx:
    sounds.set_volume(0.1)

def playBGM(bgm):
    if bgm == "level":
        mixer.music.load("SFX/BGM/daybgm.ogg")
    elif bgm == "Menu":
        pass

    mixer.music.play(-1)
    mixer.music.set_volume(0.2)

def playSound(sound):
    player = pg.mixer.Sound

    match sound:
        case "Hoe":
            player.play(hoeSfx)
        case "Coin":
            player.play(coinSfx)
        case "Selection":
            player.play(selectionSfx)
        case "ItemSwap":
            player.play(itemSwapSfx)
        case "OpenInventory":
            player.play(openInventorySfx)
        case "CloseInventory":
            player.play(closeInventorySfx)


