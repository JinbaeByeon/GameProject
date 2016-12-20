from pico2d import *
from bullet import Bullet
from math import floor

class Monster:
    SIZE = 50
    def __init__(self,name,room):
        self.x,self.y = 400,250
        self.dir_Y = 0
        self.dir_X = 0
        self.frame = 0.0
        self.bullets = [Bullet() for i in range(4)]
        self.name = name
        self.room = room
        self.die = False
        if self.name == 'clotty':
            self.image = load_image('graphics\\monster_clotty.png')
            self.hp = 10
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

    def update(self,frame_time):
        if self.name == 'clotty':
            self.frame +=  frame_time*15
            self.frame %= 11
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

    def draw(self):
        if self.hp >0:
            if self.name =='clotty':
                self.image.clip_draw((int)(self.frame%4)*64,(2-floor(self.frame/4))*64,64,64,self.x,self.y,80,80)
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


    def get_bb(self):
        if self.name == 'clotty':
            return self.x-self.SIZE/2, self.y-self.SIZE/2,self.x+self.SIZE/2,self.y+self.SIZE/2
        if self.name == 'redhost':
            return self.x-self.SIZE/2, self.y-self.SIZE/2-30,self.x+self.SIZE/2,self.y+self.SIZE/2-30

        if self.name == 'boss1':
            return self.x-self.size/2,self.y-self.size/2,self.x+self.size/2,self.y+self.size/2

    def draw_bb(self):
        if self.hp>0:
            draw_rectangle(*self.get_bb())
