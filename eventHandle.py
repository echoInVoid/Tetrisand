import pygame as pyg
from status import status
from sand import resetSand

def eventHandler():
    """处理所有收到的事件"""
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            status.game.saveHighScore()
            
            # 命令所有线程退出
            status.game.needToQuit = True

        # 键盘事件
        if event.type == pyg.KEYDOWN:
            if status.game.fail: # 如果游戏结束，重新开始，重置所有数据
                status.game.saveHighScore()
                status.reset()
                resetSand()
            # 旋转当前形状
            if event.key == pyg.K_RIGHT:
                status.sand.curShape.leftRotate()
            elif event.key == pyg.K_LEFT:
                status.sand.curShape.rightRotate()
        
        if event.type == pyg.MOUSEBUTTONDOWN:
            # 放置沙子
            status.sand.placeSand = True
