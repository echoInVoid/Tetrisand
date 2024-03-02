from audioop import reverse
from settings import setting

class Shape:
    def __init__(self, s: str):
        self.l = []
        for i in s.split("\n"):
            self.l.append([])
            self.l[-1] = list(map(bool, map(int, i)))
    
    def extend(self) -> 'list[list[bool]]':
        """将这个形状展开成可用于放置沙子的列表"""
        sz = setting.blockSize
        w = len(self.l) * sz
        h = len(self.l[0]) * sz
        result = [ [self.l[i//sz][j//sz] for j in range(h)] for i in range(w) ]
        
        return result

    def leftRotate(self) -> None:
        """顺时针旋转自身"""
        # rows = len(self.l)
        # cols = len(self.l[0])
        # for i in range(rows):
        #     for j in range(cols):
        #         tmp[j][i] = self.l[rows-i-1][j]
        # self.l = tmp
        self.rightRotate()
        self.rightRotate()
        self.rightRotate()
    
    def rightRotate(self) -> None:
        """逆时针旋转自身"""
        w = len(self.l)
        h = len(self.l[0])
        tmp = [[False]*w for _ in range(h)]
        for i in range(w):
            self.l[i].reverse()
            for j in range(h):
                tmp[j][i] = self.l[i][j]
        self.l = tmp

SHAPE1 = Shape("10\n10\n11") # L
SHAPE2 = Shape("01\n01\n11") # 反 L
SHAPE3 = Shape("1111") # I
SHAPE4 = Shape("11\n11") # O
SHAPE5 = Shape("110\n011") # Z
SHAPE6 = Shape("011\n110") # S
SHAPE7 = Shape("111\n010") # T

SHAPES = (SHAPE1, SHAPE2, SHAPE3, SHAPE4, SHAPE5, SHAPE6, SHAPE7)