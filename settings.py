import pygame as pyg

class Setting:
    def __init__(self):
        self.screenSize = (600,800)
        self.title = "Tetrisand"

        self.bgImage = pyg.image.load(".\\res\\bg.bmp")

        self.fps = 30
        self.tps = 20

        self.needToQuit = False

setting = Setting()