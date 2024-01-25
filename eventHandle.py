import pygame as pyg
from status import status, resetStatus
from sand import resetSand

def eventHandler():
    """处理所有收到的事件"""
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            status.saveHighScore()
            
            # 命令所有线程退出
            status.needToQuit = True

        # 键盘事件
        if event.type == pyg.KEYDOWN:
            if status.fail: # 如果游戏结束，重新开始，重置所有数据
                status.saveHighScore()
                resetStatus()
                resetSand()
            # 旋转当前形状
            if event.key == pyg.K_RIGHT:
                status.curShape.rotate()
            elif event.key == pyg.K_LEFT:
                status.curShape.rotate()
                status.curShape.rotate()
                status.curShape.rotate()
        
        if event.type == pyg.MOUSEBUTTONDOWN:
            # 放置沙子
            status.placeSand = True
