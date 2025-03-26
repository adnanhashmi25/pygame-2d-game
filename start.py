import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()

win = pygame.display.set_mode((500,500))
screen_width = 500

pygame.display.set_caption("Captain A")

# class Direction(Enum):
#     RIGHT = 1
#     LEFT = 2
#     SPACE = 3

# Point = namedtuple('Point', 'x, y')

# This goes outside the while loop, near the top of the program

walk = [pygame.image.load('img/sprite_'+ str(x) + '.png') for x in range(6)]

bg = pygame.image.load('img/bg.png')

clock = pygame.time.Clock()

hitSound = pygame.mixer.Sound('sound/hit.wav')
scoreSound = pygame.mixer.Sound('sound/score.wav')
music = pygame.mixer.music.load('sound/music.mp3')


class player():
    def __init__(self,x,y,height,width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 8
        self.isJump = False
        self.jumpCount = 7
        self.left =  False
        self.right = True
        self.walkCount = 0
        self.hitbox = (self.x +20, self.y, 28,60)
        self.scored = False
        self.score = 0
        self.hurt = False
        self.life = 3
        self.damage = False
        self.game_over = False
        self.scroll_speed = 3
        self.speed_up_check = False

    def draw(self,win):
        if self.walkCount + 1 >= 18:
            self.walkCount = 0
        if self.left:
            win.blit(pygame.transform.flip(walk[self.walkCount//3],True,False), (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walk[self.walkCount//3], (self.x,self.y))  
            self.walkCount += 1
        self.hitbox = (self.x +20, self.y, 28,60)

    def lifeDecre(self):
        self.life -= 1
        hitSound.play()
        if self.life == 0:
            self.game_over = True

    def Scroll(self):
        if self.score % 5 == 0 and cap_a.score != 0 and not self.speed_up_check:
            self.scroll_speed +=2
            self.speed_up_check = True
        if self.score % 5 != 0:
            self.speed_up_check = False
        if self.x > 0:
            self.x -= self.scroll_speed
        if self.x < 6:
            self.walkCount += 1
        

class obstacle():
    def __init__(self, x,y,height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.hitbox = (self.x, self.y, 32,32)
        self.obstacle_speed = 5
    
    def drawObstacle(self,win,n):
        win.blit(pygame.image.load('img/respon.png'),(self.x,self.y))
        
        if cap_a.score % 5 == 0 and cap_a.score != 0 and not cap_a.speed_up_check:
            self.obstacle_speed += 2
        if -100 < self.x < 600:
            self.x -= self.obstacle_speed
        else:
            self.x = random.randint(505, 590)
        self.hitbox = (self.x, self.y, 32,32)
    
    def score(self,cap_a):
        
        if cap_a.hitbox[1] + cap_a.hitbox[3] < self.hitbox[1]:
            if cap_a.hitbox[0] > self.hitbox[0] + self.hitbox[2] and cap_a.hitbox[0] < self.hitbox[0] + self.hitbox[2] + 10:
                if cap_a.scored == False and cap_a.hurt == False:
                    cap_a.scored = True
                    cap_a.score += 1
                    scoreSound.play()
        else:
            if cap_a.hitbox[0] + cap_a.hitbox[2] > self.hitbox[0] and cap_a.hitbox[0] < self.hitbox[0] + self.hitbox[2]:
                cap_a.hurt = True
                if cap_a.damage == False:
                    cap_a.damage = True
                    cap_a.lifeDecre()
                
            elif cap_a.hitbox[0] > self.hitbox[0] + self.hitbox[2]:
                cap_a.hurt = False
            else:
                cap_a.scored = False

        if cap_a.hitbox[0] > self.hitbox[0] + self.hitbox[2] and cap_a.hitbox[0] < self.hitbox[0] + self.hitbox[2] +10:
            cap_a.damage = False


cap_a = player(40,400,64,64)
responsibility = obstacle(200,420,32,32)
responsibility1 = obstacle(500,420,32,32)

def redrawGameWindow(n):
    text = font.render('Score: ' + str(cap_a.score), 1, (255,255,255))
    text1 = font.render('Life: ' + str(cap_a.life), 1, (255,255,255))
    win.blit(bg, (-n%1000 - 1000,0)) 
    win.blit(text, (10,10))
    win.blit(text1, (360,10))
    responsibility.drawObstacle(win,n)
    responsibility1.drawObstacle(win,n)
    cap_a.draw(win)
    pygame.display.update()

def GameOver():
    win.fill((0,0,0))
    text = font.render('Game Over' , 1 , (255,255,255))
    text1 = font.render('Press Space to Play again' , 1 , (255,255,255))
    win.blit(text,(160,20))
    win.blit(text1,(60,220))
    pygame.display.update()
    
def reset():
    cap_a.game_over = False
    cap_a.life = 3
    cap_a.score = 0
    cap_a.scroll_speed = 3
    frame_iteration = 0


run = True
#main loop
font  = pygame.font.SysFont('comicsans', 30, True)
bgScroll = 0
while run:
    bgScroll += 3
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = action
    if cap_a.game_over == False:
        
        responsibility.score(cap_a)
        responsibility1.score(cap_a)

        if keys[pygame.K_LEFT] and cap_a.x > 0:
            cap_a.x -= cap_a.vel
            cap_a.left = True
            cap_a.right = False
        elif keys[pygame.K_RIGHT] and  cap_a.x < screen_width - cap_a.width:
            cap_a.x += cap_a.vel
            cap_a.left = False
            cap_a.right = True
        elif cap_a.x >= 6:
            cap_a.walkCount = 0
        if not(cap_a.isJump):
            if keys[pygame.K_SPACE]:
                cap_a.isJump = True
                walkCount = 0
        else:
            if cap_a.jumpCount >= -7:
                neg = 1
                if cap_a.jumpCount < 0 :
                    neg = -1
                cap_a.y -= (cap_a.jumpCount ** 2) * 0.5 * neg
                cap_a.jumpCount -= 1
            elif not(keys[pygame.K_SPACE]):
                cap_a.isJump = False
                cap_a.jumpCount = 7
        cap_a.Scroll()
        redrawGameWindow(bgScroll)

    else:
        GameOver()
        pygame.mixer.music.play(-1)

        if keys[pygame.K_SPACE]:
            cap_a.game_over = False
            cap_a.life = 3
            cap_a.score = 0
            cap_a.scroll_speed = 3

pygame.quit()
