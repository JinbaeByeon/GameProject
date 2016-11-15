from pico2d import *
from door import Door
from monster import Monster
import json

class Map:
    global player

    def __init__(self):
        self.stage = 0
        self.left,self.bottom,self.right,self.top = 80,80,720,420
        self.state = 'CENTER_ROOM'
        self.inMonster = False
        self.monster_left =[Monster('clotty','LEFT_ROOM') for i in range(3)]
        self.monster_bottom = [Monster('redhost','BOTTOM_ROOM') for i in range(3)]
        self.monster_boss ={0 : [Monster('boss1','RIGHT_ROOM') for j in range(8)],
                            1 : [Monster('boss1','RIGHT_ROOM') for j in range(8)],
                            2 : [Monster('boss1','RIGHT_ROOM') for j in range(8)]}


        self.map_image= {0:load_image('basement.png'),1:load_image('cellar.png'),2:load_image('basement.png')}
        self.bg_image = load_image('bgblack.png')

        self.left_door = Door('normal', 'LEFT')
        self.right_door =Door('bossroom','RIGHT')
        self.top_door =Door('treasure','TOP')
        self.bottom_door =Door('normal','BOTTOM')
        self.trap_door = Door('trapdoor','TRAP_DOOR')

        self.left_door.unlock()
        self.right_door.unlock()
        self.top_door.unlock()
        self.bottom_door.unlock()

    def draw(self):
        self.bg_image.draw(400,300,800,600)
        self.map_image[self.stage].draw(400,250,800,500)

    def get_bb(self):
        return self.left, self.bottom,self.right,self.top

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw_door(self):
        if self.state == 'CENTER_ROOM':
            self.left_door.draw()
            self.right_door.draw()
            self.top_door.draw()
            self.bottom_door.draw()
        elif self.state == 'LEFT_ROOM':
            self.right_door.draw()
        elif self.state == 'RIGHT_ROOM':
            self.left_door.draw()
            if self.inMonster == False:
                self.trap_door.draw()
        elif self.state == 'TOP_ROOM':
            self.bottom_door.draw()
        elif self.state == 'BOTTOM_ROOM':
            self.top_door.draw()

    def draw_door_bb(self):
        if self.state == 'CENTER_ROOM':
            self.left_door.draw_bb()
            self.right_door.draw_bb()
            self.top_door.draw_bb()
            self.bottom_door.draw_bb()
        elif self.state == 'LEFT_ROOM':
            self.right_door.draw_bb()
        elif self.state == 'RIGHT_ROOM':
            self.left_door.draw_bb()
            if self.inMonster == False:
                self.trap_door.draw_bb()
        elif self.state == 'TOP_ROOM':
            self.bottom_door.draw_bb()
        elif self.state == 'BOTTOM_ROOM':
            self.top_door.draw_bb()

    def update(self):
        if self.state == 'CENTER_ROOM':
            self.left_door = Door('normal', 'LEFT')
            self.right_door =Door('bossroom','RIGHT')
            self.top_door =Door('treasure','TOP')
            self.bottom_door =Door('normal','BOTTOM')
            self.left_door.unlock()
            self.right_door.unlock()
            self.top_door.unlock()
            self.bottom_door.unlock()

        elif self.state == 'RIGHT_ROOM':
            self.left_door = Door('bossroom', 'LEFT')
        elif self.state == 'TOP_ROOM':
            self.bottom_door = Door('treasure','BOTTOM')
        elif self.state == 'BOTTOM_ROOM':
            self.top_door = Door('normal','TOP')
        elif self.state == 'LEFT_ROOM':
            self.right_door = Door('normal','RIGHT')

        if self.inMonster == False:
            self.left_door.unlock()
            self.right_door.unlock()
            self.top_door.unlock()
            self.bottom_door.unlock()


