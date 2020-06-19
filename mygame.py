import pygame
from pygame.locals import *
import sys
import pygame.time as time
import pygame.font as font
import random as random
import math 

dict = {K_w: False, K_a: False, K_s: False, K_d: False}
dir = {K_w: [0,-10], K_a: [-10,0], K_s: [0,10], K_d: [10,0]}

class mySprite():
    def __init__(self, image, name='', x=0, y=0):
        self.image = image
        self.rect = image.get_rect()
        self.rect = self.rect.move(x,y)
        self.name = name
        self.x = x
        self.y = y

class myEnemy(mySprite):
    def __init__(self, vector=[0,0]):
        super().__init__(image=pygame.image.load("images/goomba.png").convert_alpha())
        self.vector = vector
        self.user = [0,0]
        self.collided = False
        self.move()


    def control(self, event):
        xdir = self.isLeft()
        ydir = self.isUp()
        self.vector = [xdir,ydir]
        for elem in dir:
            if dict[elem]:
                self.user[0] = self.user[0] + dir[elem][0]
                self.user[1] = self.user[1] + dir[elem][1]
        self.move()

    def move(self):
        self.rect = self.rect.move(self.vector)
        self.x = self.x + self.vector[0]
        self.y = self.y + self.vector[1]

    def backtrack(self, dist, event, dif=1 ):
        tempd = dist
        for i in range(dif): # change range for difficulty
            if tempd < 125:
                self.collided = True
            # elif tempd < dist:
            self.control(event)
                # bool = backtrack(self, tempd, event, enemy)
            tempd = self.tempd()

    def tempd(self):
        return math.sqrt((self.x - self.user[0]) * (self.x - self.user[0])
                            + (self.y - self.user[1]) * (self.y - self.user[1]))

    def isLeft(self):
        if (self.x - self.user[0]) > 0: # left
            return random.randrange(-5, -1, 1)
        else: # right
            return random.randrange(1, 5, 1)

    def isUp(self):
        if (self.y - self.user[1]) > 0: # up
            return random.randrange(-5, -1, 1)
        else: # down
            return random.randrange(1, 5, 1)

class myPlayer(mySprite):
    def __init__(self, ):
        super().__init__(image=pygame.image.load("images/mario.png").convert_alpha())
        
        
    def control(self, event):
        try:
            if event.type == pygame.KEYDOWN:
                dict[event.key] = True
            elif event.type == pygame.KEYUP:
                dict[event.key] = False
            self.move()
        except (KeyError):
            print("use W-A-S-D")
    
    def move(self):
        for elem in dict:
            if dict[elem]:
                self.rect = self.rect.move(dir[elem])
                self.x = self.x + dir[elem][0]
                self.y = self.y + dir[elem][1]

class myFinish(mySprite):
    def __init__(self, vector=[0, 0]):
        super().__init__(image=pygame.image.load("images/finish.jpg").convert_alpha())
        self.vector = vector
        self.user = [0,0]
        self.rect = self.rect.move(self.vector)
        self.collide = False

    def collide(self, Dist, event):
        tempD = Dist
        while 1:
            if tempD < 129:
                self.collide = True
            tempD = self.tempD()
    
    def tempD(self):
        return math.sqrt((self.x - self.user[0]) * (self.x - self.user[0])
                            + (self.y - self.user[1]) * (self.y - self.user[1]))

def main():

    pygame.init()
    size = width, height = 1280, 720
    black = 0,0,0
    red = 255,0,0
    sprites = []
    X = 400
    Y = 400
    levelnum = 2
    lmax = -1
    umax = -1
    rmax = 1       
    dmax = 1 
   
    lmin = -1 
    umin = -1
    rmin = 1
    dmin = 1
    print("Game is starting...")

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Best game ever')

    sprites.append(myEnemy)
    enemy = myEnemy(vector=[700, 300])
    player = myPlayer()
    sprites.append(player)
    finish = myFinish(vector=[1150, 300])
    sprites.append(finish)



    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            player.control(event)

            #finish.collide(Dist=finish.tempD(), event=event)
            if finish.collide:
                print('Level' + levelnum)
                levelnum = levelnum + 1
                if levelnum < 4:
                    lmax-= 1
                    umax-= 1
                    rmax+= 1       
                    dmax+= 1
                else:
                    lmax-= 1
                    umax-= 1
                    rmax+= 1       
                    dmax+= 1
                    lmin-= 1 
                    umin-= 1
                    rmin+= 1
                    dmin+= 1

                enemy.backtrack(dist=enemy.tempd(), event=event)
                if enemy.collided:
                    print("you lose")
                    return

        screen.fill(black) # makes screen black       
        screen.blit(player.image, player.rect)
        screen.blit(enemy.image, enemy.rect)
        screen.blit(finish.image, finish.rect)        
        pygame.display.flip() # writes the next image to the window
        
        time.delay(100)

if __name__ == "__main__":
    main()
    print("game over")

