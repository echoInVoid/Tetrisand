from random import choice, randint
from shape import SHAPES
from sand import SANDS_LIGHT


class Status:
    def __init__(self):
        self.curShape = choice(SHAPES) # 下一个放置的形状
        self.curType = randint(0, len(SANDS_LIGHT)-1) # 下一个放置的沙子种类
        self.placeSand = False # 如果为True，在下一tick放置沙子
        self.placeCD = 0 # 剩余放置冷却时间
    
    def nextPlacement(self):
        """随机选取下次要放置的沙子形状与颜色"""
        self.curShape = choice(SHAPES)
        for i in range(randint(0,3)): # 随机旋转下一个形状
            self.curShape.rotate()
        self.curType = randint(0, len(SANDS_LIGHT)-1)

status = Status()