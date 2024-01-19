from settings import setting

class Shape:
    def __init__(self, s: str):
        self.l = []
        for i in s.split("\n"):
            self.l.append([])
            self.l[-1] = list(map(bool, map(int, i)))
    
    def _extend(self) -> 'list[list[bool]]':
        """将这个形状展开成可用于放置沙子的列表"""
        width = len(self.l) * setting.blockSize
        height = len(self.l[0]) * setting.blockSize
        result = [[None for j in range(height)] for i in range(width)]

        for i in range(width):
            for j in range(height):
                result[i][j] = self.l[i//setting.blockSize][j//setting.blockSize]
        
        return result


SHAPE1 = Shape("10\n10\n11") # L
SHAPE2 = Shape("01\n01\n11") # 反 L
SHAPE3 = Shape("1111") # I
SHAPE4 = Shape("11\n11") # O
SHAPE5 = Shape("110\n011") # Z
SHAPE6 = Shape("011\n110") # S
SHAPE7 = Shape("111\n010") # T

SHAPES = (SHAPE1, SHAPE2, SHAPE3, SHAPE4, SHAPE5, SHAPE6, SHAPE7)