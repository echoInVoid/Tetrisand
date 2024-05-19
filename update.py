import pygame as pyg
from random import choice

from render import stat
from sand import *
from settings import setting
from status import status

updateClock = pyg.time.Clock()

def updateSand():
    """让沙子下落"""
    for y in range(setting.sandListSize[1]-2, -1, -1): # 从下往上更新沙子，最下一行无需更新
        for x in range(setting.sandListSize[0]):
            # 尝试让沙子下落
            if not updatableSand(sands[x][y]):
                continue
            if sands[x][y+1] == VOID:
                sands[x][y], sands[x][y+1] = sands[x][y+1], sands[x][y]
            elif x!=setting.sandListSize[0]-1 and sands[x+1][y+1]==VOID:
                sands[x][y], sands[x+1][y+1] = sands[x+1][y+1], sands[x][y]
            elif x!=0 and sands[x-1][y+1]==VOID:
                sands[x][y], sands[x-1][y+1] = sands[x-1][y+1], sands[x][y]

def checkForFailing():
    """检查是否有沙子到达高度上限，如果有，结束游戏"""
    for x in range(setting.sandListSize[0]):
        for y in range(setting.sandListSize[1]-1, setting.failLine-1, -1):
            if y<=setting.failLine and updatableSand(sands[x][y]):
                status.game.fail = True
            if not updatableSand(sands[x][y]):
                break

def putSand():
    """放置沙子"""
    curShape = status.sand.curShape
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
                sands[x+i][j] = choice((SANDS_DARK[status.sand.curType], SANDS_LIGHT[status.sand.curType]))
    
    status.nextPlacement()
    stat.refreshColorHint()

def markSand() -> bool:
    """标记接触左右两边的连片沙子"""

    # BFS
    sandRemoving = [] # 需要移除的标记
    mark = [[-1]*setting.sandListSize[1] for _ in range(setting.sandListSize[0])]
    for j in range(setting.sandListSize[1]):
        if updatableSand(sands[0][j]):
            if BFSMark(0, j, mark, j):
                sandRemoving.append(j)
    
    if len(sandRemoving) == 0:
        return False
    
    replaceMarkedSand(sandRemoving, mark)

    return True

def replaceMarkedSand(sandRemoving: 'list[int]', mark: 'list[list[int]]'):
    """让被标记的沙子被渲染成白色，即替换成REMOVING"""
    for i in range(setting.sandListSize[0]):
        for j in range(setting.sandListSize[1]):
            if mark[i][j] in sandRemoving:
                sands[i][j] = REMOVING

def removeMarkedSand() -> int:
    """移除标记的沙子，返回移除的沙子数"""
    cnt = 0
    for i in range(setting.sandListSize[0]):
        for j in range(setting.sandListSize[1]):
            if sands[i][j] == REMOVING:
                sands[i][j] = VOID
                cnt += 1
    return cnt

def BFSMark(x: int, y: int, mark: 'list[list[int]]', marker: int) -> bool:
    """从(x,y)开始寻找同时接触左右边界的沙子区域，并标记为marker。返回是否有同时接触左右边界的沙子区域"""
    if mark[x][y] != -1:
        return False
    
    queue = [(x, y)]
    mark[x][y] = marker
    head = 0
    res = False
    while (head<len(queue)):
        curX, curY = queue[head]
        head += 1

        if curX == setting.sandListSize[0]-1:
            res = True
        
        for dx in (-1,1):
            if validPos(curX+dx, curY):
                if mark[curX+dx][curY] == -1:
                    if sands[curX][curY] == sands[curX+dx][curY]:
                        mark[curX+dx][curY] = marker
                        queue.append((curX+dx, curY))
        for dy in (-1,1):
            if validPos(curX, curY+dy):
                if mark[curX][curY+dy] == -1:
                    if sands[curX][curY] == sands[curX][curY+dy]:
                        mark[curX][curY+dy] = marker
                        queue.append((curX, curY+dy))
    
    return res

def update():
    """
    更新游戏中的沙子

    只在 main.py 中的 updateThread 中被调用
    """

    # 更新循环
    while True:
        # 检查线程退出标志
        if status.game.needToQuit:
            return # 退出线程
        
        updateClock.tick(setting.tps)

        if status.game.fail:
            continue

        if status.game.pausedTime:
            status.game.pausedTime -= 1
            continue

        sandsLock.acquire() # 为 sands 加锁

        if status.sand.placeSand and status.sand.placeCD==0:
            putSand()
            status.sand.placeCD = setting.placeCD
        status.sand.placeSand = False

        updateSand()
        
        if markSand():
            status.game.pauseByRemoving()
            sandsLock.release()
            continue

        status.game.addScore(removeMarkedSand())

        sandsLock.release() # 释放锁

        checkForFailing()

        status.sand.placeCD -= 1
        status.sand.placeCD = max(status.sand.placeCD, 0)
