import pygame as pyg

from settings import setting
from status import status
from sand import *

renderClock = pyg.time.Clock()

bgSign = 0 # 随帧变化，决定背景图片的移动
colorHintMove = 0 # 随帧变化，决定颜色提示的移动
colorHintY = -20

def refreshColorHint():
    global colorHintMove
    colorHintMove = setting.fps

def flipAllAreas():
    setting.sandArea.fill("#000000")
    setting.infoArea.fill("#FFFFFF")
    setting.shapeArea.fill("#000000")
    setting.colorArea.fill("#000000")

def renderBackground(screen: pyg.surface.Surface):
    """渲染游戏背景"""

    global bgSign
    bgSign += 0.2
    bgSign %= 25
    screen.blit(setting.bgImage, (-bgSign, -bgSign))
    screen.blit(setting.coverImage, (0, 0))
    screen.set_colorkey("#00000000")

def renderSand():
    """渲染沙子"""
    
    sandsLock.acquire() # 为 sands 加锁

    for x in range(setting.sandListSize[0]):
        for y in range (setting.sandListSize[1]):
            if sands[x][y] != VOID:
                sand = sands[x][y]
                pyg.draw.rect(
                    setting.sandArea, sand.color,
                    pyg.rect.Rect(
                        x*setting.sandSize, 
                        y*setting.sandSize, 
                        setting.sandSize, 
                        setting.sandSize
                    )
                )
    
    sandsLock.release() # 释放锁

def renderGhost():
    """渲染提示虚影"""

    curShape = status.curShape
    ghostWidth = len(curShape.l)*setting.blockSize*setting.sandSize

    ghostX = pyg.mouse.get_pos()[0] # 虚影左上角x坐标
    ghostX -= ghostWidth//2
    ghostX -= setting.sandPos[0]
    ghostX = max(0, ghostX)
    ghostX = min(setting.sandArea.get_width()-ghostWidth, ghostX)
    ghostX -= ghostX%setting.sandSize

    ghost = curShape.l
    ghostColor:pyg.color.Color = SANDS_LIGHT[status.curType].color
    ghostColor.a = int(128 * (1 - status.placeCD/setting.placeCD)) # 让虚影随着CD减少逐渐变得不透明

    rect = pyg.Surface(
            (setting.sandSize*setting.blockSize, setting.sandSize*setting.blockSize),
            pyg.SRCALPHA
        )
    rect.fill(ghostColor)

    for i in range(len(ghost)):
        for j in range(len(ghost[0])):
            if ghost[i][j]:
                rectPos = (
                    ghostX + i*setting.sandSize*setting.blockSize,
                    j*setting.sandSize*setting.blockSize
                )
                setting.sandArea.blit(rect, rectPos)

def renderColorHint():
    """渲染放置色彩提示"""
    global colorHintMove, colorHintY
    if colorHintMove:
        colorHintY -= 108/setting.fps
        image1 = status.prevImage
        image2 = status.curImage
        image3 = status.nextImage
        setting.colorArea.blit(image3, (0,colorHintY+108+108))
        setting.colorArea.blit(image2, (0,colorHintY+108))
        setting.colorArea.blit(image1, (0,colorHintY))
    else:
        colorHintY = -20
        image1 = status.curImage
        image2 = status.nextImage
        setting.colorArea.blit(image2, (0,colorHintY+108))
        setting.colorArea.blit(image1, (0,colorHintY))

    colorHintMove = max(0, colorHintMove-1)
    
def renderShapeHint():
    """渲染放置形状提示"""
    curShape = status.curShape
    width = len(curShape.l)*setting.hintBlockSize
    height = len(curShape.l[0])*setting.hintBlockSize
    x = setting.shapeArea.get_width()//2 - width//2
    y = setting.shapeArea.get_height()//2 - height//2
    for i in range(len(curShape.l)):
        for j in range(len(curShape.l[0])):
            if curShape.l[i][j]:
                block = pyg.rect.Rect(
                    x+setting.hintBlockSize*i, y+setting.hintBlockSize*j,
                    setting.hintBlockSize, setting.hintBlockSize
                )
                pyg.draw.rect(setting.shapeArea, "#FFFFFF", block)

def renderInfoBoard():
    """渲染屏幕上方信息栏"""
    renderLogo()
    
    text1 = "%08d"%status.score
    text2 = "%08d"%status.highScore
    surf1 = setting.renderFont.render(text1, False, "#000000")
    surf2 = setting.renderFont.render(text2, False, "#000000")
    fontX = setting.infoArea.get_width()-surf1.get_width()
    fontY = setting.infoArea.get_height()/2 - surf1.get_height()+5
    setting.infoArea.blit(surf1, (fontX, fontY))
    setting.infoArea.blit(surf2, (fontX, fontY+surf1.get_height()))

def renderLogo():
    setting.infoArea.blit(setting.logoImage, (0,0))

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
        
        flipAllAreas()
        renderBackground(screen)
        renderSand()
        renderGhost()
        renderColorHint()
        renderShapeHint()
        renderInfoBoard()
        screen.blit(setting.sandArea, setting.sandPos)
        screen.blit(setting.colorArea, setting.colorPos)
        screen.blit(setting.shapeArea, setting.shapePos)
        screen.blit(setting.infoArea, setting.infoPos)

        pyg.display.flip()
        renderClock.tick(setting.fps)
