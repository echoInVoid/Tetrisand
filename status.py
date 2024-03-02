from random import choice, randint
from settings import setting
from shape import SHAPES
from sand import SANDS_LIGHT
from pygame.image import load

class SandStat:
    def __init__(self):
        self.curShape = SHAPES[0] # 下一个放置的形状
        self.curType = 0 # 下一个放置的沙子种类
        self.nextType = 0 # 再下一个放置的沙子种类

        self.placeSand = False # 如果为True，在下一tick放置沙子
        self.placeCD = 0 # 剩余放置冷却时间

    def nextPlacement(self):
        self.curShape = choice(SHAPES)
        for i in range(randint(0,3)): # 随机旋转下一个形状
            self.curShape.leftRotate()
        self.curType = self.nextType
        self.nextType = randint(0, len(SANDS_LIGHT)-1)

class RenderStat:
    def __init__(self):
        # 用于提示玩家沙子颜色
        self.prevImage = load(".\\res\\sand\\0.png")
        self.curImage = load(".\\res\\sand\\0.png")
        self.nextImage = load(".\\res\\sand\\0.png")
    
    def nextPlacement(self, nextType):
        self.prevImage = self.curImage
        self.curImage = self.nextImage
        self.nextImage = load(".\\res\\sand\\%d.png"%nextType)

class GameStat:
    def __init__(self):
        self.pausedTime = 0 # 剩余暂停时间

        self.score = 0 # 当前得分
        self.highScore = self.__getHighScore() # 最高分

        self.fail = False # 当前游戏是否失败
        self.needToQuit = False # 是否需要退出游戏

    def __getHighScore(self) -> int:
        """从文件读取最高分"""
        try:
            with open("score.txt", "r") as f:
                return int(f.read())
        except Exception as e:
            print("Error: Failed to get high score:", str(e)) #TODO: 这里也许需要一个更成熟的日志方式
            return 0
        
    def saveHighScore(self):
        """将分数存储到文件"""
        try:
            with open("score.txt", "w") as f:
                f.write(str(self.highScore))
        except Exception as e:
            print("Error: Failed to save high score:", str(e)) #TODO: 这里也许需要一个更成熟的日志方式
        
    def addScore(self, score: int):
        self.score += score
        self.highScore = max(self.highScore, self.score)
    
    def pauseByRemoving(self):
        self.pausedTime = setting.removePauseTime

class Status:
    def __init__(self):
        self.sand = SandStat()
        self.render = RenderStat()
        self.game = GameStat()

        # 随机选取下次要放置的沙子形状与颜色
        self.nextPlacement()
    
    def nextPlacement(self):
        """随机选取下次要放置的沙子形状与颜色"""
        self.sand.nextPlacement()
        self.render.nextPlacement(self.sand.nextType)
    
    def reset(self):
        self.__init__()

status = Status()