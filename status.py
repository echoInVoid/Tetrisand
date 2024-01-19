from random import choice, randint
from shape import SHAPES
from sand import SANDS_LIGHT


class Status:
    def __init__(self):
        self.curShape = None # 下一个放置的形状
        self.curType = None # 下一个放置的沙子种类
        self.nextSand()
    
    def nextSand(self):
        self.curShape = choice(SHAPES)
        self.curType = randint(0, len(SANDS_LIGHT)-1)

status = Status()