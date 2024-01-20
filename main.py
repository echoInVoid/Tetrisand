import sys
import threading

import pygame as pyg

from render import render
from sandProcess import update
from eventHandle import eventHandler
from settings import setting


def main():
    # 初始化屏幕
    pyg.init()
    screen = pyg.display.set_mode(setting.screenSize)
    pyg.display.set_caption(setting.title)

    # 主渲染进程
    renderThread = threading.Thread(None, render, "renderThread", (screen,))
    renderThread.start()

    # 主更新进程
    updateThread = threading.Thread(None, update, "updateThread")
    updateThread.start()

    while True:
        # 监听事件
        eventHandler()
        
        # 退出
        if setting.needToQuit:
            break
    
    pyg.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()
