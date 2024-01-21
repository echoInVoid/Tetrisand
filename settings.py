import pygame as pyg

class Setting:
    def __init__(self):
        self.screenSize = (600,800)
        self.title = "Tetrisand"

        self.bgImage = pyg.image.load(".\\res\\bg.png")
        self.coverImage = pyg.image.load(".\\res\\cover.png")

        # 屏幕最上方的计分板
        self.infoArea = pyg.surface.Surface((504,112))
        self.infoPos = (48,32)
        # 主要游戏区
        self.sandArea = pyg.surface.Surface((340,560))
        self.sandPos = (44,192)
        # 显示下一个方块形状的区域
        self.shapeArea = pyg.surface.Surface((116,116))
        self.shapePos = (424,212)
        # 显示下一个方块颜色的区域
        self.colorArea = pyg.surface.Surface((52,108))
        self.colorPos = (456,540)

        self.sandSize = 4 # 单颗沙粒的边长
        self.sandListSize = (self.sandArea.get_width()//self.sandSize, self.sandArea.get_height()//self.sandSize) # 沙粒列表的尺寸
        self.blockSize = 10 # 一个块的边长，单位是沙粒
        self.hintBlockSize = 6*self.sandSize # 提示区方块的边长，单位像素

        self.fps = 30
        self.tps = 20
        self.placeCD = self.tps # 两次放置之间的冷却时间

        self.needToQuit = False

setting = Setting()