from threading import Lock

from settings import setting


class Sand:
    """
    单个沙粒
    """

    def __init__(self, typ: int, color: str):
        self.type = typ  # 沙子的颜色。0-4依次表示红、黄、绿、蓝。-1为空
        self.color = color  # 沙子实际渲染时的颜色

VOID = Sand(-1, "#000000")
SAND_RED1 = Sand(0, "#B0482F")
SAND_RED2 = Sand(0, "#8D3A26")
SAND_YELLOW1 = Sand(0, "#DA9D2F")
SAND_YELLOW2 = Sand(0, "#B98628")
SAND_GREEN1 = Sand(0, "#5D8D28")
SAND_GREEN2 = Sand(0, "#466B1F")
SAND_BLUE1 = Sand(0, "#305995")
SAND_BLUE2 = Sand(0, "#28497A")

sands = [ [ VOID for i in range(setting.sandListSize[1]) ]
         for j in range(setting.sandListSize[0]) ]

sandsLock = Lock()