import pygame as pyg

from settings import setting
from status import status
from sand import *

renderClock = pyg.time.Clock()

bgSign = 0 # 随帧变化，决定背景图片的移动

def renderBackground(screen: pyg.surface.Surface):
    """渲染游戏背景"""

    global bgSign
    bgSign += 0.2
    bgSign %= 25
    screen.blit(setting.bgImage, (-bgSign, -bgSign))
    screen.blit(setting.coverImage, (0, 0))
    screen.set_colorkey()

def renderSand(screen: pyg.surface.Surface):
    """渲染沙子"""
    
    sandsLock.acquire() # 为 sands 加锁

    for x in range(setting.sandListSize[0]):
        for y in range (setting.sandListSize[1]):
            if sands[x][y] != VOID:
                sand = sands[x][y]
                pyg.draw.rect(
                    screen, sand.color,
                    pyg.rect.Rect(
                        setting.sandArea.left+x*setting.sandSize, 
                        setting.sandArea.top+y*setting.sandSize, 
                        setting.sandSize, 
                        setting.sandSize
                        )
                )
    
    sandsLock.release() # 释放锁

def renderGhost(screen: pyg.surface.Surface):
    """渲染提示虚影"""

    curShape = status.curShape
    ghostWidth = len(curShape.l[0])*setting.blockSize*setting.sandSize

    ghostX = pyg.mouse.get_pos()[0] # 虚影左上角x坐标
    ghostX -= ghostWidth//2
    ghostX = max(setting.sandArea.left, ghostX)
    ghostX = min(setting.sandArea.right-ghostWidth, ghostX)

    ghost = curShape.l
    ghostColor:pyg.color.Color = SANDS_LIGHT[status.curType].color
    ghostColor.a = 128

    rect = pyg.Surface(
            (setting.sandSize*setting.blockSize, setting.sandSize*setting.blockSize),
            pyg.SRCALPHA
        )
    rect.fill(ghostColor)

    for i in range(len(ghost[0])):
        for j in range(len(ghost)):
            if (ghost[j][i]):
                rectPos = (
                    ghostX + i*setting.sandSize*setting.blockSize,
                    setting.sandArea.top + j*setting.sandSize*setting.blockSize
                )
                screen.blit(rect, rectPos)

def render(screen: pyg.surface.Surface):
    """
    主渲染器，负责将游戏中的一切渲染到屏幕上

    只在 main.py 中的 renderThread 中被调用
    """

    # 渲染循环
    while True:
        # 检查线程退出标志
        if setting.needToQuit:
            return # 退出线程
        
        renderBackground(screen)
        renderSand(screen)
        renderGhost(screen)

        pyg.display.flip()
        renderClock.tick(setting.fps)
