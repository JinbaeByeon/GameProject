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
        self.hp = 10
        self.name = name
        self.room = room
        self.die = False
        if self.name == 'clotty':
            self.image = load_image('monster_clotty.png')
        if self.name == 'redhost':
            self.image = load_image('monster_redhost.png')

    def update(self,frame_time):
        if self.name == 'clotty':
            self.frame +=  frame_time*15
            self.frame %= 11
        if self.name == 'redhost':
            pass


    def draw(self):
        if self.hp >0:
            if self.name =='clotty':
                self.image.clip_draw((int)(self.frame%4)*64,(2-floor(self.frame/4))*64,64,64,self.x,self.y,80,80)
            if self.name == 'redhost':
                self.image.clip_draw(0,0,32,64,self.x,self.y,50,100)


    def get_bb(self):
        if self.name == 'clotty':
            return self.x-self.SIZE/2, self.y-self.SIZE/2,self.x+self.SIZE/2,self.y+self.SIZE/2
        if self.name == 'redhost':
            return self.x-self.SIZE/2, self.y-self.SIZE/2-30,self.x+self.SIZE/2,self.y+self.SIZE/2-30

    def draw_bb(self):
        if self.hp>0:
            draw_rectangle(*self.get_bb())
