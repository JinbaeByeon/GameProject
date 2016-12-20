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
                            1 : [Monster('boss2','RIGHT_ROOM') for i in range(4)],
                            2 : [Monster('boss1','RIGHT_ROOM') for j in range(8)]}


        self.map_image= {0:load_image('graphics\\basement.png'),1:load_image('graphics\\cellar.png'),2:load_image('graphics\\basement.png')}
        self.bg_image = load_image('graphics\\bgblack.png')
        self.shade_image=load_image('graphics\\shading.png')
        self.left_door = Door('normal', 'LEFT')
        self.right_door =Door('bossroom','RIGHT')
        self.top_door =Door('treasure','TOP')
        self.bottom_door =Door('normal','BOTTOM')
        self.trap_door = Door('trapdoor','TRAP_DOOR')

        self.left_door.unlock()
        self.right_door.unlock()
        self.top_door.unlock()
        self.bottom_door.unlock()

        self.ui_image =load_image('graphics\\progress.png')

        self.bgm=load_music('sounds\\bgm.mp3')
        self.bgm.set_volume(64)

        self.bgm_bossroom = {0:load_music('sounds\\bossroom1.mp3'),1:load_music('sounds\\bossroom2.ogg'),2:load_music('sounds\\bossroom3.mp3')}
        self.bgm_bossroom[self.stage].set_volume(30)
        self.state_bgm = None

        self.sound_door = load_wav('sounds\\unlock.wav')
        self.sound_door.set_volume(30)

    ui_x={'LEFT_ROOM':-32,
          'CENTER_ROOM':0,
          'TOP_ROOM':0,
          'BOTTOM_ROOM':0,
          'RIGHT_ROOM':32}

    ui_y = {'LEFT_ROOM': 0,
            'CENTER_ROOM': 0,
            'TOP_ROOM': 20,
            'BOTTOM_ROOM': -20,
            'RIGHT_ROOM': 0}

    def play_bgm(self):
        if self.state_bgm != 'normal':
            self.state_bgm = 'normal'
            self.bgm.repeat_play()

    def play_bgm_boss(self):
        if self.state_bgm != 'bossroom':
            self.state_bgm = 'bossroom'
            self.bgm.pause()
            self.bgm_bossroom[self.stage].repeat_play()

    def draw(self):
        self.bg_image.draw(400,300,800,600)
#        self.ui_image.clip_draw(0,160,32,32,100,590,300,600)
        self.map_image[self.stage].draw(400,250,800,500)
        self.shade_image.draw(400,250,800,500)

        self.ui_image.clip_draw(0,160,32,32,68,550,50,50)
        self.ui_image.clip_draw(0,160,32,32,132,550,50,50)
        self.ui_image.clip_draw(64,128,32,32,132,540)
        self.ui_image.clip_draw(0,160,32,32,100,530,50,50)
        self.ui_image.clip_draw(0,160,32,32,100,570,50,50)
        self.ui_image.clip_draw(64,32,32,32,100,570)
        self.ui_image.clip_draw(0,160,32,32,100,550,50,50)
        self.ui_image.clip_draw(0,160,32,32,100,550,50,50)
        self.ui_image.clip_draw(32,128,32,32,100+self.ui_x[self.state],540+self.ui_y[self.state])

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


