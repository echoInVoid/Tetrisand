from sand import VOID
from settings import setting


sands = [ [ VOID for i in range(setting.sandListSize[1]) ]
         for j in range(setting.sandListSize[0]) ]

def resetSand():
    global sands
    for i in range(setting.sandListSize[0]):
        for j in range(setting.sandListSize[1]):
            sands[i][j] = VOID