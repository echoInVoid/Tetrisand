import pygame as pyg
from random import choice
from render import refreshColorHint

from sand import *
from settings import setting
from status import status

updateClock = pyg.time.Clock()

def updateSand():
    """让沙子下落"""
    for y in reversed(range(setting.sandListSize[1]-1)): # 从下往上更新沙子，最下一行无需更新
        for x in range(setting.sandListSize[0]):
            # 尝试让沙子下落
            if sands[x][y+1]==VOID:
                sands[x][y], sands[x][y+1] = sands[x][y+1], sands[x][y]
            elif x!=setting.sandListSize[0]-1 and sands[x+1][y+1]==VOID:
                sands[x][y], sands[x+1][y+1] = sands[x+1][y+1], sands[x][y]
            elif x!=0 and sands[x-1][y+1]==VOID:
                sands[x][y], sands[x-1][y+1] = sands[x-1][y+1], sands[x][y]

def putSand():
    """放置沙子"""
    curShape = status.curShape
    placement = curShape.extend()
    width = len(placement)
    height = len(placement[0])

    # 待放置的形状左上角x坐标
    x = pyg.mouse.get_pos()[0]
    x -= width*setting.sandSize//2
    x = max(setting.sandPos[0], x)
    x = min(setting.sandPos[0]+setting.sandArea.get_width() - width*setting.sandSize, x)
    x -= x % setting.sandSize
    x -= setting.sandPos[0]
    x = x//setting.sandSize

    for i in range(width):
        for j in range(height):
            if placement[i][j]:
                sands[x+i][j] = choice((SANDS_DARK[status.curType], SANDS_LIGHT[status.curType]))
    
    status.nextPlacement()
    refreshColorHint()

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
        
        sandsLock.acquire() # 为 sands 加锁

        if status.placeSand and status.placeCD==0:
            putSand()
            status.placeCD = setting.placeCD
        status.placeSand = False

        updateSand()
        status.placeCD -= 1
        status.placeCD = max(status.placeCD, 0)

        sandsLock.release() # 释放锁

        updateClock.tick(setting.tps)