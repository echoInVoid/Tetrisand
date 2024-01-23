from random import choice, randint
from settings import setting
from shape import SHAPES
from sand import SANDS_LIGHT
from pygame.image import load


class Status:
    def __init__(self):
        self.curShape = SHAPES[0] # 下一个放置的形状
        self.curType = 0 # 下一个放置的沙子种类
        self.nextType = 0 # 再下一个放置的沙子种类

        # 用于提示玩家沙子颜色
        self.prevImage = load(".\\res\\sand\\0.png")
        self.curImage = load(".\\res\\sand\\0.png")
        self.nextImage = load(".\\res\\sand\\0.png")

        self.placeSand = False # 如果为True，在下一tick放置沙子
        self.placeCD = 0 # 剩余放置冷却时间

        self.pausedByRemoving = 0 # 剩余暂停时间

        self.score = 0 # 当前得分
        self.highScore = self.__getHighScore() # 最高分

        self.nextPlacement()

    def __getHighScore(self) -> int:
        """从文件读取最高分"""
        try:
            with open("score.txt", "r") as f:
                return int(f.read())
        except Exception as e:
            print("Error: Failed to get high score:", str(e)) #TODO: 这里也许需要一个更成熟的日志方式
            return 0
    
    def addScore(self, score: int):
        self.score += score
        self.highScore = max(self.highScore, self.score)
    
    def saveHighScore(self):
        """将分数存储到文件"""
        try:
            with open("score.txt", "w") as f:
                f.write(str(self.highScore))
        except Exception as e:
            print("Error: Failed to save high score:", str(e)) #TODO: 这里也许需要一个更成熟的日志方式
    
    def nextPlacement(self):
        """随机选取下次要放置的沙子形状与颜色"""
        self.curShape = choice(SHAPES)
        for i in range(randint(0,3)): # 随机旋转下一个形状
            self.curShape.rotate()
        
        self.prevImage = self.curImage

        self.curType = self.nextType
        self.curImage = self.nextImage

        self.nextType = randint(0, len(SANDS_LIGHT)-1)
        self.nextImage = load(".\\res\\sand\\%d.png"%self.nextType)
    
    def pauseBecauseRemoving(self):
        self.pausedByRemoving = setting.removePauseTime

status = Status()