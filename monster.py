from pico2d import *
from bullet import Bullet
from math import floor
from random import randint

class Monster:
    SIZE = 50
    def __init__(self,name,room):
        self.x,self.y = 400,250
        self.dir_Y = 0
        self.dir_X = 0
        self.frame = 0.0
        self.bullets = [Bullet(1,'red') for i in range(4)]
        self.name = name
        self.room = room
        self.die = False
        self.gauge = 2.0
        self.sound_shot = load_wav('sounds\\tear_fire.wav')

        if self.name == 'clotty':
            self.image = load_image('graphics\\monster_clotty.png')
            self.hp = 10
            self.dir_X = 1
            self.dir_Y = -1
            self.speed = 10
            self.size = 50
        if self.name == 'redhost':
            self.image = load_image('graphics\\monster_redhost.png')
            self.hp = 10
        if self.name == 'boss1':
            self.image = load_image('graphics\\boss1.png')
            self.hp = 32
            self.size=80
            self.num = 1
            self.dir_X = 1
            self.dir_Y = 1
            self.speed = 10
            self.split = False
        if self.name == 'boss2':
            self.image = load_image('graphics\\boss2.png')
            self.hp =15
            self.x = randint(100,700)
            self.y = randint(100,500)
            self.speed =10
            self.dir_X = randint(-1,1)
            if self.dir_X == 0:
                self.dir_Y = 1
            self.frame_X =0
            self.frame_Y =0
            self.size = 50

    def update(self,frame_time):
        if self.name == 'clotty':
            self.x += self.dir_X*frame_time*10*self.speed
            self.y += self.dir_Y*frame_time*10*self.speed

            self.frame +=  frame_time*15
            self.frame %= 11

            self.gauge -= frame_time
            if self.gauge <= 0:
                self.sound_shot.play()
                self.gauge=2.0
                self.bullets[0].dir_X = -1
                self.bullets[1].dir_X = 1
                self.bullets[2].dir_Y = -1
                self.bullets[3].dir_Y = 1
                for bullet in self.bullets:
                    bullet.x=self.x
                    bullet.y=self.y
                self.dir_X= randint(-1,1)
                self.dir_Y= randint(-1,1)

            for bullet in self.bullets:
                bullet.update(frame_time)

        if self.name == 'redhost':
            pass
        if self.name =='boss1':
            self.x += self.dir_X*frame_time*10*self.speed
            self.y += self.dir_Y*frame_time*10*self.speed

            if self.hp > 16:
                self.size = 80
                self.speed =10
            elif self.hp > 8:
                self.size = 40
                self.speed = 13
            elif self.hp > 4:
                self.size = 36
                self.speed = 16
            else:
                self.size = 30
                self.speed = 20
        if self.name == 'boss2':
            self.x += self.dir_X*frame_time*10*self.speed
            self.y += self.dir_Y*frame_time*10*self.speed
            if self.dir_X ==1:
                self.frame_X = 0
                self.frame_Y = 0
            elif self.dir_X == -1:
                self.frame_X = 2
                self.frame_Y = 0
            elif self.dir_Y == 1:
                self.frame_X = 2
                self.frame_Y = 1
            elif self.dir_Y == -1:
                self.frame_X = 0
                self.frame_Y = 1


    def draw(self):
        if self.hp >0:
            if self.name =='clotty':
                self.image.clip_draw((int)(self.frame%4)*64,(2-floor(self.frame/4))*64,64,64,self.x,self.y,80,80)
                for bullet in self.bullets:
                    bullet.draw()
            if self.name == 'redhost':
                self.image.clip_draw(0,0,32,64,self.x,self.y,50,100)
            if self.name == 'boss1':
                if self.hp>16:
                    self.image.clip_draw(0,38,80,90,self.x,self.y)
                elif self.hp>8:
                    self.image.clip_draw(100,64,50,64,self.x,self.y)
                elif self.hp>4:
                    self.image.clip_draw(160,64 ,60,64,self.x,self.y)
                else:
                    self.image.clip_draw(100,0,60,64,self.x,self.y)
            if self.name == 'boss2':
                if self.dir_Y ==1:
                    self.image.clip_draw(64*self.frame_X,64*self.frame_Y,64,64,self.x+self.dir_X*10,self.y+self.dir_Y*10)
                    self.image.clip_draw(192,0,64,64,self.x-3,self.y+12)
                else:
                    self.image.clip_draw(192,0,64,64,self.x-3,self.y+8)
                    self.image.clip_draw(64*self.frame_X,64*self.frame_Y,64,64,self.x+self.dir_X*10,self.y+self.dir_Y*10)


    def get_bb(self):
        if self.name == 'clotty':
            return self.x-self.SIZE/2, self.y-self.SIZE/2,self.x+self.SIZE/2,self.y+self.SIZE/2
        if self.name == 'redhost':
            return self.x-self.SIZE/2, self.y-self.SIZE/2-30,self.x+self.SIZE/2,self.y+self.SIZE/2-30

        if self.name == 'boss1' or self.name == 'boss2':
            return self.x-self.size/2,self.y-self.size/2,self.x+self.size/2,self.y+self.size/2

    def draw_bb(self):
        if self.hp>0:
            draw_rectangle(*self.get_bb())
