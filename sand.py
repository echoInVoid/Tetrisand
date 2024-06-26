from threading import Lock
from pygame.color import Color

from settings import setting


class Sand:
    """
    单个沙粒
    """

    def __init__(self, typ: int, color: str):
        self.type = typ  # 沙子的颜色。0-4依次表示红、黄、绿、蓝。-1为空
        self.color = color  # 沙子实际渲染时的颜色
    
    def __eq__(self, __value) -> bool:
        if type(__value) != Sand:
            raise ValueError("Cannot compare Sand and %s."%__value.__class__.__name__)
        
        return self.type==__value.type

VOID = Sand(-1, "#000000")
SAND_RED1 = Sand(0, "#B0482F")
SAND_RED2 = Sand(0, "#8D3A26")
SAND_YELLOW1 = Sand(1, "#DA9D2F")
SAND_YELLOW2 = Sand(1, "#B98628")
SAND_GREEN1 = Sand(2, "#5D8D28")
SAND_GREEN2 = Sand(2, "#466B1F")
SAND_BLUE1 = Sand(3, "#305995")
SAND_BLUE2 = Sand(3, "#28497A")
REMOVING = Sand(4, "#FFFFFF") # 即将被删除

SANDS_LIGHT = (SAND_RED1, SAND_YELLOW1, SAND_GREEN1, SAND_BLUE1)
SANDS_DARK = (SAND_RED2, SAND_YELLOW2, SAND_GREEN2, SAND_BLUE2)

sandsLock = Lock()

def updatableSand(s:Sand) -> bool:
    return s != VOID and s != REMOVING

def validPos(x:int, y:int) -> bool:
    """验证(x,y)是否在sands内"""
    return (
        x >= 0 and
        x < setting.sandListSize[0] and
        y >= 0 and
        y < setting.sandListSize[1]
    )