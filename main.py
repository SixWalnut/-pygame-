#!/usr/bin/env python 3.10.2
# -*-coding:utf-8 -*-
#创建日期: 2022/03/20 23:19:49 
#创建者: SixWalnut
#文件描述: 游戏实现模块

#准备好后可以导入模块了
import sys
import pygame
import random

#全局变量定义

#此变量为uid废案遗留产物迭代后将删除
global_idlist=0
#定义敌人列表
global_aimlist=[]
#定义子弹列表
global_bulletlist=[]
#定义分数
global_score = 0
#定义游戏状态标志 0:初始屏幕 1:游戏中 2:暂停 3:gameover
global_screenflag = 0

#类定义
#定义子弹类 无父类继承关系
class bullet():
    #定义初始化方法 参数详解:
    #spawntype:     创建方      字符串型        aim 或player
    #potion：       生成位置    int型数组       任意的有效位置
    #speed:         运动速度    int型           任意有效速度
    #uid:           游戏内id    int型           全局变量global_idlist,传入后需要+1
    #pygameclass    pygame对象  pygame对象      有效的pygame对象
    def __init__(self,spawntype,potion,speed):
        #为对象设置属性
        #对象的大小 图片大小8x24 已经写死
        self.size = [8,14]
        #由于所有图片大小均写死 所以需要额外的步骤以写死子弹生成位置
        self.site = []
        self.spawntype=spawntype

        #两种弹药运动方向不同
        if spawntype == "player":
            #速度取负实现向上运动
            self.speed = speed * -1
            self.site.append(potion[0] + 45)
            self.site.append(potion[1] + 50)
        else:
            self.speed = speed
            self.site.append(potion[0] + 20)
            self.site.append(potion[1] + 18)
        self.pygameclass = pygame.image.load("./image/bullet.png").convert_alpha()
        #此属性为击中标志废案 迭代后删除
        self.attack = False

    #定义移动方法
    def move(self):
        self.site[1] += self.speed
        #此返回值为理解错误时的废案 迭代后删除
        return [self.site[0],self.site[1]]

    #定义对象表加入方法
    def listjoin(self):
        global global_bulletlist
        global_bulletlist.append(self)

    #定义对象销毁方法
    def listquite(self):
        del self
        return True

#定义敌人类 无父类继承关系
class aim():
    #定义初始化方法 参数详解:
    #hp             最大生命值          int         #此属性为废案 迭代后移除
    #speed          运动速度            int         
    #firecd         开炮冷却时间        int    
    #pygameclass    此对象的pygame对象  object     
    #spawntype      生成位置 默认随机   str
    def __init__(self,hp,speed,firecd,spawntype=None):
        #大小写死
        self.size = [49,36]
        #设置默认值 防止非法访问
        if spawntype == None:
            self.site = [random.randint(0,440),-40]
        else:
            self.site = [spawntype[0],-10]
        #此属性为废案 迭代后移除
        self.hp = hp
        self.pygameclass = pygame.image.load("./image/airplane.png").convert_alpha()
        self.speed = speed
        #下次允许开火所剩的游戏刻数
        self.maxfirecd = firecd
        #开火冷却时间
        self.nowfirecd = firecd
        #控制台输出生成消息
        print("[INFO]Spawn an aim at [{},{}]".format(self.site[0],self.site[1]))

    #定义移动方法
    def move(self):
        self.site[1] += self.speed
        #此返回值为理解错误时的废案 迭代后删除
        return [self.site[0],self.site[1]]
    
    #定义开炮方法
    def fire(self):
        newbullet = bullet("aim",[self.site[0],self.site[1]],random.randint(10,30))
        newbullet.listjoin()

    #定义受伤方法
    #此方法为废案 迭代后移除
    def getdamage(self,damage):
        self.hp = hp-1

    #定义受击方法
    #此方法为废案 迭代后移除
    def gethint(self,bullet):
        pass

    #定义对象表加入方法
    def listjoin(self):
        global global_aimlist
        global_aimlist.append(self)

    #定义对象销毁方法
    def listquite(self):
        print("del aim")
        del self
        return True

class player():
    #定义玩家类

    #定义初始化方法 pygameclass:玩家pygame对象
    #pygameclass1   玩家的pygame对象(静态与后退态)      object
    #pygameclass2   玩家的pygame对象(动态)              object
    def __init__(self,pygameclass,pygameclass2):
        self.size = [97,124]
        self.site = [200,700]
        self.speed = 5
        #持续按键标识符
        self.keyUp = False
        self.keyDown = False
        self.keyLeft = False
        self.keyRight = False
        self.keyFire = False
        
        self.quite = pygameclass
        self.move  = pygameclass2

        #开火cd相关属性
        self.firecd = 0
        self.maxfirecd = 30
    
    #定义开火方法
    def fire(self):
        #cd小于0时允许开火
        if self.firecd <= 0:
            newbullet = bullet("player",[self.site[0],self.site[1]],30)
            newbullet.listjoin()
            #cd重置
            self.firecd =self.maxfirecd 
        else:
            pass
    #定义输入事件响应方法
    def keyScan(self):
        global global_screenflag
        for event in pygame.event.get():
            #游戏关闭事件:
            if event.type== pygame.QUIT:
                sys.exit()
            
            #按键按下事件:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.keyUp = True
                if event.key == pygame.K_DOWN:
                    self.keyDown = True
                if event.key == pygame.K_LEFT:
                    self.keyLeft = True
                if event.key == pygame.K_RIGHT:
                    self.keyRight = True
                if event.key == pygame.K_SPACE:
                    self.keyFire = True
                if event.key == pygame.K_ESCAPE:
                    global_screenflag = 2

            
            #按键抬起事件:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.keyUp = False
                if event.key == pygame.K_DOWN:
                    self.keyDown = False
                if event.key == pygame.K_LEFT:
                    self.keyLeft = False
                if event.key == pygame.K_RIGHT:
                    self.keyRight = False
                if event.key == pygame.K_SPACE:
                    self.keyFire = False
        
        #根据按键标识符设置移动方向
        if self.keyUp:
            self.site[1] -= self.speed
        if self.keyDown:
            self.site[1] += self.speed
        if self.keyLeft:
            self.site[0] -= self.speed
        if self.keyRight:
            self.site[0] += self.speed
        if self.keyFire:
            self.fire()
        
        #若移动后超出边界则拉回
        if self.site[0] > 480 - self.size[0]:
            self.site[0] = 480 - self.size[0]
        if self.site[0] < 0:
            self.site[0] = 0
        if self.site[1] > 852 - self.size[1]:
            self.site[1] = 852 - self.size[1]
        if self.site[1] < 0:
            self.site[1] =0
        
        #此返回值为理解错误时的废案 迭代后删除
        return self.site

#函数定义
#敌人移动函数:
def airplanemove():
    global global_aimlist
    #流程控制变量
    loopcount = 0
    #遍历所有敌人
    for theaim in global_aimlist:
        #此式为理解错误时的废案 可直接换为global_aimlist[loopcount].move()
        global_aimlist[loopcount].site = theaim.move()

        #若移动后超出边界则销毁目标
        if global_aimlist[loopcount].site[1] >900:
            global_aimlist[loopcount].listquite()
            del global_aimlist[loopcount]
        
        #流程控制
        loopcount += 1

#定义敌人绘制函数 screen:屏幕对象
def airplanedraw(screen):
    global global_aimlist
    #流程控制变量
    loopcount = 0
    #遍历所有敌人
    for theaim in global_aimlist:
        #在屏幕上显示该对象
        screen.blit(theaim.pygameclass,(theaim.site[0],theaim.site[1]))
        #流程控制
        loopcount += 1
    #返回屏幕对象
    return screen

#定义敌人开火函数
def airplanefire():
    global global_aimlist
    #流程控制变量
    loopcount = 0
    #遍历所有敌人
    for theaim in global_aimlist:
        #所有敌人cd-1
        theaim.nowfirecd -= 1
        #cd归零时执行开火方法 同时重置cd
        if theaim.nowfirecd == 0:
            theaim.fire()
            theaim.nowfirecd = theaim.maxfirecd
    
#定义子弹绘制函数 screen:屏幕对象
def airplanefiredraw(screen):
    global global_bulletlist
    #定义流程控制变量
    loopcount = 0
    #遍历所有子弹
    for theaim in global_bulletlist:
        #在屏幕上显示该对象
        screen.blit(theaim.pygameclass,(theaim.site[0],theaim.site[1]))
        #流程控制
        loopcount +=1
    #返回屏幕对象
    return screen

#定义子弹移动函数
def bulletmove():
    global global_bulletlist
    #定义流程控制变量
    loopcount = 0
    #遍历所有子弹
    for theaim in global_bulletlist:
        #执行移动方法
        global_bulletlist[loopcount].site = theaim.move()

        #若移动后超出边界则销毁目标
        if -20>global_bulletlist[loopcount].site[1]> 900:
            global_bulletlist[loopcount].listquite()
            del global_bulletlist[loopcount]

        #流程控制
        loopcount += 1

#定义矩形重叠检测函数 site1:矩形1坐标 size1:矩形1长,宽 site2:矩形2坐标 size2:矩形2长,宽
def testareafill(site1,size1,site2,size2):
    if site1[0] + size1[0] > site2[0] and site2[0] + size2[0] > site1[0] and site1[1] + size1[1] >site2[1] and site2[1] + size2[1] > site1[1]:
        return True
    else:
        return False

#定义完犊子函数
def gameover():
    global global_aimlist
    global global_bulletlist
    global global_score
    global global_screenflag
    global_aimlist = []
    global_bulletlist = []
    global_screenflag = 3

#定义子弹命中检测函数 theplayer:玩家对象
def bulletareafill(theplayer):
    global global_aimlist
    global global_bulletlist
    global global_score
    #循环流程1控制变量
    loopcount_outsize = 0
    #遍历所有子弹
    for thebullet in global_bulletlist:
        #单个子弹流程:
        #若该子弹生成者是玩家
        if thebullet.spawntype == "player":
            #循环流程2控制变量
            loopcount_insize = 0
            #遍历所有敌人
            for theaim in global_aimlist:
                #若敌人与子弹有重叠:
                if testareafill(thebullet.site,thebullet.size,theaim.site,theaim.size):
                    #销毁敌人
                    theaim.listquite()
                    del global_aimlist[loopcount_insize]
                    #销毁子弹
                    thebullet.listquite()
                    del global_bulletlist[loopcount_outsize]
                    #控制台输出
                    print("hint target!")
                    #分数+1
                    global_score +=1
                    #此时未遍历的敌人可忽略不计 故跳出循环
                    break
                #流程控制2
                loopcount_insize +=1
        #若该子弹不是玩家射出的
        else:
            #若该子弹与玩家有重叠
            if testareafill(thebullet.site,thebullet.size,theplayer.site,theplayer.size):
                #完犊子
                gameover()
        #流程控制1
        loopcount_outsize +=1

#定义玩家与敌人相撞检测函数 theplayer:玩家对象
def planeareafill(theplayer):
    global global_aimlist
    #流程控制变量
    loopcount = 0
    #遍历所有敌人
    for theaim in global_aimlist:
        #若玩家与敌人有重叠:
        if testareafill(theaim.site,theaim.size,theplayer.site,theplayer.size):
            #销毁敌人
            theaim.listquite()
            del global_aimlist[loopcount]
            #控制台输出
            print("get crash!!!!")
            #完犊子
            gameover()
        #流程控制
        loopcount += 1


#主函数定义
def main():
    #全局变量载入
    global global_aimlist
    global global_bulletlist
    global global_idlist
    global global_score
    global global_screenflag

    #pygame初始化
    pygame.init()
    pygame.display.set_caption("全民打飞机")                    #标题栏设置
    ttf = pygame.font.Font('C:/Windows/Fonts/simsunb.ttf',35)   #字体设置
    
    #实例化游戏时钟
    clock=pygame.time.Clock()
    #绘制游戏界面
    screen = pygame.display.set_mode((480,852))

    #实例化玩家对象
    theplayer1 = pygame.image.load("./image/hero1.png").convert_alpha ()
    theplayer2 = pygame.image.load("./image/hero0.png").convert_alpha ()
    theplayer = player(theplayer1,theplayer2)

    #载入背景
    background = pygame.image.load("./image/background.png").convert_alpha ()
    startmenu = pygame.image.load("./image/start.png").convert_alpha ()
    #游戏内变量定义
    #定义生成时间cd
    spawncd = random.randint(60,240)
    clicktostart = ttf.render("press any key to continue", True, (0,0,0),(255,255,255))
    clicktostart.set_colorkey((255,255,255))
    pausemenu = pygame.image.load("./image/pause.png").convert_alpha ()
    gameovermenu = pygame.image.load("./image/gameover.png").convert_alpha ()
    #游戏循环
    while True:
        #设置帧率
        clock.tick(60)
        #绘制背景
        screen.blit(background,(0,0))
        #cd-1
        if global_screenflag == 0:
            screen.blit(startmenu,(0,0))
            screen.blit(clicktostart,(15,750))
            for event in pygame.event.get():
                #按键检测:
                if event.type== pygame.QUIT:
                    sys.exit()
                if event.type== pygame.KEYDOWN:
                    global_screenflag = 1
                    theplayer = player(theplayer1,theplayer2)
        elif global_screenflag == 1:
            spawncd -= 1
            theplayer.firecd -= 1

            #当生成敌人cd归零时生成一名敌人
            if spawncd == 0:
                theaim = aim(1,2,60)
                theaim.listjoin()
                #重置生成cd
                spawncd = random.randint(60,240)
            #计算敌人移动后位置
            airplanemove()
            #执行一轮敌人开火检测
            airplanefire()
            #探测子弹是否击中
            bulletareafill(theplayer)
            #探测敌人是否与玩家相撞
            planeareafill(theplayer)

            #若子弹列表为空时跳过子弹移动 防止 列表索引错误
            if global_bulletlist == []:
                pass
            else:
                #子弹移动
                bulletmove()
            
            #传入并传回屏幕对象以绘制敌人
            screen = airplanedraw(screen)
            #传入并传回屏幕对象以绘制子弹
            screen = airplanefiredraw(screen)

            #扫描输入
            theplayer.keyScan()

            #若移动方向为上左右，则玩家显示为动态，否则为静态
            if theplayer.keyUp or theplayer.keyLeft or theplayer.keyRight:
                screen.blit(theplayer.move,(theplayer.site[0],theplayer.site[1]))
            else:
                screen.blit(theplayer.quite,(theplayer.site[0],theplayer.site[1]))
            
            #获得的分数实例化
            score = ttf.render(str(global_score), True, (0,0,0),(255,255,255))
            score.set_colorkey((255,255,255))
            scoreRect = score.get_rect()
            #显示获得的分数
            screen.blit(score,scoreRect)
            #该帧绘制完毕，显示在主界面上
        elif global_screenflag == 2:
            screen.blit(pausemenu,(0,0))
            screen.blit(clicktostart,(15,750))
            for event in pygame.event.get():
                #按键检测:
                if event.type== pygame.QUIT:
                    sys.exit()
                if event.type== pygame.KEYDOWN:
                    global_screenflag = 1
        elif global_screenflag == 3:
            screen.blit(gameovermenu,(0,0))
            screen.blit(clicktostart,(15,750))
            score = ttf.render(str(global_score), True, (0,0,0),(255,255,255))
            score.set_colorkey((255,255,255))
            scoreRect = score.get_rect()
            screen.blit(score,scoreRect)
            for event in pygame.event.get():
                #按键检测:
                if event.type== pygame.QUIT:
                    sys.exit()
                if event.type== pygame.KEYDOWN:
                    global_screenflag = 0
                    global_score = 0
        pygame.display.flip()


#测试模块
if __name__ == "__main__":
    main()
