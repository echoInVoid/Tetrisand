import pygame as pyg
from settings import setting
from status import status

def eventHandler():
    """处理所有收到的事件"""
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            status.saveHighScore()
            
            # 命令所有线程退出
            setting.needToQuit = True

        # 键盘事件
        if event.type == pyg.KEYDOWN:
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
