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
            if sands[x][y] == VOID or sands[x][y]==REMOVING:
                continue
            if sands[x][y+1] == VOID:
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

def markSand() -> bool:
    """标记接触左右两边的连片沙子"""

    # BFS
    sandRemoving = [] # 需要移除的标记
    mark = [[-1]*setting.sandListSize[1] for _ in range(setting.sandListSize[0])]
    for j in range(setting.sandListSize[1]):
        if sands[0][j] != VOID and sands[0][j] != REMOVING:
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

        if (
            curX-1>=0 and 
            mark[curX-1][curY]==-1 and
            sands[curX][curY]==sands[curX-1][curY]
        ):
            mark[curX-1][curY] = marker
            queue.append((curX-1, curY))
        if (
            curY-1>=0 and
            mark[curX][curY-1]==-1 and
            sands[curX][curY]==sands[curX][curY-1]
        ):
            mark[curX][curY-1] = marker
            queue.append((curX, curY-1))
        if (
            curX+1<len(sands) and
            mark[curX+1][curY]==-1 and
            sands[curX][curY]==sands[curX+1][curY]
        ):
            mark[curX+1][curY] = marker
            queue.append((curX+1, curY))
        if (
            curY+1<len(sands[0]) and
            mark[curX][curY+1]==-1 and
            sands[curX][curY]==sands[curX][curY+1]
        ):
            mark[curX][curY+1] = marker
            queue.append((curX, curY+1))
    
    return res

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
        
        updateClock.tick(setting.tps)

        if status.pausedByRemoving:
            status.pausedByRemoving -= 1
            continue

        sandsLock.acquire() # 为 sands 加锁

        if status.placeSand and status.placeCD==0:
            putSand()
            status.placeCD = setting.placeCD
        status.placeSand = False

        updateSand()
        
        if markSand():
            status.pauseBecauseRemoving()
            sandsLock.release()
            continue

        status.addScore(removeMarkedSand())

        sandsLock.release() # 释放锁

        status.placeCD -= 1
        status.placeCD = max(status.placeCD, 0)
