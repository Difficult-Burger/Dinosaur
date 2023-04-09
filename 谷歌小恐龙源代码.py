import pygame
import random
import pygame.freetype
from pygame.locals import *
from itertools import cycle

screenwidth = 800
screenheight = 250
fps = 40
JH = 90


def rdr(r1, r2):
    if r2.right-27 > r1.left > r2.left+27 - r1.width and r1.bottom > r2.top+20:
        return True
    return False


class Map:

    # 背景图片加载
    def __init__(self, x, y):
        self.bg = pygame.image.load("ingredients/newground.png")
        self.x = x
        self.y = y

    def maproll(self):
        global maprollspeed
        if self.x < -1490:
            self.x = 1500
        else:
            self.x -= maprollspeed

    def mapupdate(self):
        screen.blit(self.bg, (self.x, self.y))


class Dinosaur:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)  # 初始化恐龙的矩形
        self.jumpstate = False  # 跳跃状态
        self.lowest = 140  # 最低坐标
        self.dinosaurindex = 0
        self.dinosaurindexgen = cycle([0, 1, 2, 3, 4])
        self.dinosaurimage = (pygame.image.load(r"ingredients\Dino1.png").convert_alpha(),
                              pygame.image.load(r"ingredients\Dino1.png").convert_alpha(),
                              pygame.image.load(r"ingredients\Dino2.png").convert_alpha(),
                              pygame.image.load(r"ingredients\Dino2.png").convert_alpha(),
                              pygame.image.load(r"ingredients\DinoJumping.png").convert_alpha())
        self.rect.size = self.dinosaurimage[0].get_size()  # 初始化矩形
        self.x = 80
        self.y = self.lowest
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.jumpstate = True

    def move(self, s):
        if self.jumpstate:
            self.rect.y -= s
            if self.rect.y == self.lowest:
                self.jumpstate = False

    def draw(self):
        if self.jumpstate:
            dinosaurindex = 4
        else:
            dinosaurindex = next(self.dinosaurindexgen)
        screen.blit(self.dinosaurimage[dinosaurindex], (self.x, self.rect.y))


class Cacti:
    score = 0

    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.cacti = (pygame.image.load("ingredients/cacti/cactus5.png").convert_alpha(),
                      pygame.image.load("ingredients/cacti/cactus6.png").convert_alpha())

        ran = random.randint(0, 1)
        self.obstacle = self.cacti[ran]
        self.rect.size = self.obstacle.get_size()
        self.width, self.height = self.rect.size

        self.x = 1500
        self.y = 170
        self.rect.center = (self.x, self.y)

    def cactimove(self):
        global maprollspeed
        self.rect.x -= maprollspeed

    def cactidraw(self):

        screen.blit(self.obstacle, (self.rect.x, self.rect.y))


def main():
    over = False
    global screen, intervallock
    global maprollspeed
    maprollspeed = 8
    pygame.init()  # pygame初始化
    intervallock = pygame.time.Clock()  # 刷新窗口的时间锁
    screen = pygame.display.set_mode((screenwidth, screenheight))  # 窗口大小设置
    pygame.display.set_caption('dinosaur')  # 窗体标题

    bg1 = Map(0, 0)
    bg2 = Map(1500, 0)
    step = 19
    score = 1
    dinosaur = Dinosaur()
    addcactitimer = 500  # 添加cactus的间隔时间
    list = []  # cactus对象列表

    while 1:
        # 判断关闭窗口是否被执行
        for event in pygame.event.get():
            if event.type == QUIT:
                over = True
                exit()  # 关闭窗口
            if event.type == KEYDOWN and event.key == K_SPACE:  # 空格键按下判断
                if dinosaur.rect.y >= dinosaur.lowest:  # 若恐龙在地上
                    step = 19
                    dinosaur.jump()

        if not over:
            bg1.mapupdate()
            bg1.maproll()
            bg2.mapupdate()
            bg2.maproll()
            if step == -17:
                step = 19
            step -= 2
            dinosaur.move(step)
            dinosaur.draw()

            #  添加cactus时间控制
            if addcactitimer >= 600:
                ran = random.randint(0, 100)
                if ran >= 40:
                    cactus = Cacti()
                    list.append(cactus)
                addcactitimer = 0

        for i in range(len(list)):
            list[i].cactimove()
            list[i].cactidraw()
        addcactitimer += 20

        # 分数显示
        f = pygame.freetype.Font('ingredients/PressStart2P-Regular.ttf', 15)
        fsurface, frect = f.render(str(int(score)), [0, 0, 0], [255, 255, 255])
        screen.blit(fsurface, (650, 25))

        score += 0.35

        # 加速
        if int(score) % 50 == 0:
            maprollspeed += 0.5

        for i in range(len(list)):
            if rdr(dinosaur.rect, list[i].rect):
                # 显示你寄了
                f = pygame.freetype.Font('ingredients/PressStart2P-Regular.ttf', 30)
                fsurface, frect = f.render("G ! !", [0, 0, 0], [255, 255, 255])
                screen.blit(fsurface, (330, 70))
                f = pygame.freetype.Font('ingredients/PressStart2P-Regular.ttf', 15)
                fsurface, frect = f.render("Press Enter To Quit", [0, 0, 0], [255, 255, 255])
                screen.blit(fsurface, (255, 130))
                pygame.display.update()

                while 1:
                    if pygame.event.peek(KEYDOWN):
                        while 1:
                            for event in pygame.event.get():
                                if event.type == KEYDOWN and event.key == 13:
                                    over = True
                                    exit()

        pygame.display.update()  # 更新窗口
        intervallock.tick(fps)  # 更新间隔时间


if __name__ == '__main__':  # 程序入口
    main()
