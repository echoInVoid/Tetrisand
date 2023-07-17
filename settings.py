import pygame as pyg

class Setting:
    def __init__(self):
        self.screenSize = (600,800)
        self.title = "Tetrisand"

        self.bgImage = pyg.image.load(".\\res\\bg.png")
        self.coverImage = pyg.image.load(".\\res\\cover.png")

        self.infoArea = pyg.rect.Rect(48,32,504,112) # 屏幕最上方的计分板
        self.sandArea = pyg.rect.Rect(44,192,340,560) # 主要游戏区
        self.shapeArea = pyg.rect.Rect(424,212,116,116) # 显示下一个方块形状的区域
        self.colorArea = pyg.rect.Rect(456,540,52,108) # 显示下一个方块颜色的区域

        self.sandSize = 4 # 单颗沙粒的边长
        self.sandListSize = (self.sandArea.width//self.sandSize, self.sandArea.height//self.sandSize) # 沙粒列表的尺寸

        self.fps = 30
        self.tps = 20

        self.needToQuit = False

setting = Setting()