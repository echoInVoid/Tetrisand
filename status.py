from random import choice, randint
from shape import SHAPES
from sand import SANDS_LIGHT
from pygame.image import load


class Status:
    def __init__(self):
        self.curShape = SHAPES[0] # 下一个放置的形状
        self.curType = 0 # 下一个放置的沙子种类
        self.nextType = 0 # 再下一个放置的沙子种类

        # 用于提示玩家沙子颜色
        self.prevImage = load(".\\res\\sand\\0.png")
        self.curImage = load(".\\res\\sand\\0.png")
        self.nextImage = load(".\\res\\sand\\0.png")

        self.placeSand = False # 如果为True，在下一tick放置沙子
        self.placeCD = 0 # 剩余放置冷却时间

        self.nextPlacement()
    
    def nextPlacement(self):
        """随机选取下次要放置的沙子形状与颜色"""
        self.curShape = choice(SHAPES)
        for i in range(randint(0,3)): # 随机旋转下一个形状
            self.curShape.rotate()
        
        self.prevImage = self.curImage

        self.curType = self.nextType
        self.curImage = self.nextImage

        self.nextType = randint(0, len(SANDS_LIGHT)-1)
        self.nextImage = load(".\\res\\sand\\%d.png"%self.nextType)

status = Status()