import pygame as pyg

from settings import setting

renderClock = pyg.time.Clock()

bgSign = 0 # 随帧变化，决定背景图片的移动

def renderBackground(screen: pyg.surface.Surface):
    global bgSign
    bgSign += 0.2
    bgSign %= 25
    screen.blit(setting.bgImage, (-bgSign, -bgSign))
    screen.blit(setting.coverImage, (0, 0))

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

        pyg.display.flip()
        renderClock.tick(setting.fps)
