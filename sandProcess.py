import pygame as pyg

from sand import *
from settings import setting

updateClock = pyg.time.Clock()

def updateSand():
    """
    让沙子下落
    """

    sandsLock.acquire() # 为 sands 加锁

    for y in reversed(range(setting.sandListSize[1]-1)): # 从下往上更新沙子，最下一行无需更新
        for x in range(setting.sandListSize[0]):
            # 尝试让沙子下落
            if sands[x][y+1]==VOID:
                sands[x][y], sands[x][y+1] = sands[x][y+1], sands[x][y]
            elif x!=setting.sandListSize[0]-1 and sands[x+1][y+1]==VOID:
                sands[x][y], sands[x+1][y+1] = sands[x+1][y+1], sands[x][y]
            elif x!=0 and sands[x-1][y+1]==VOID:
                sands[x][y], sands[x-1][y+1] = sands[x-1][y+1], sands[x][y]

    sandsLock.release() # 释放锁

def update():
    """
    更新游戏中的沙子

    只在 main.py 中的 updateThread 中被调用
    """

    # 更新循环
    while True:
        # 检查线程退出标志
        if setting.needToQuit:
            return # 退出线程
        
        updateSand()

        updateClock.tick(setting.tps)