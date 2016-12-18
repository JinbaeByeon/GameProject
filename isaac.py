import random
import json
import os

from pico2d import *
import math
import start_state
import game_framework

from bullet import Bullet
from map import Map
from item import Item
from monster import Monster

name = "MainState"

player = None
map =None
font = None


class Isaac:
    global map,items

    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.7
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 10

    PLAYER_SIZE = 50

    head = None
    body = None

    MOVE_LEFT, MOVE_RIGHT= 0,3
    MOVE_UP,MOVE_DOWN,NOT_MOVE = 1,4,7
    HEAD_LEFT,HEAD_RIGHT,HEAD_UP,HEAD_DOWN,NOT_SHOT =2,5,8,11,14

    def __init__(self):
        self.x, self.y = 400, 250
        self.max_hp = 3
        self.hp = 3
        self.shot_speed =3
        self.power =1
        self.head_frame = 0
        self.head_total_frames = 0.0
        self.body_frame =0
        self.body_total_frames = 0.0
        self.dir_X = 0
        self.dir_Y = 0
        self.head_state = self.NOT_SHOT
        self.body_state = self.NOT_MOVE
        self.shot_Enable = True
        self.gauge = 0.0
        self.laser = False
        self.laser_enable = False
        self.laser_shot = False
        self.laser_dir = 0
        self.rad = 0

        self.bullets = [Bullet() for i in range(8)]
        self.current = 0

        if Isaac.head == None:
            Isaac.head_image = load_image('isaac.png')
        if Isaac.body == None:
            Isaac.body_image = load_image('isaac.png')

        self.laser_image = load_image('laser.png')
        self.laser_swirling = load_image('laser_swirl.png')
        self.laser_impact = load_image('laser_impact.png')
        self.ui_image = load_image('ui_hearts.png')

    def update(self, frame_time):
        distance = Isaac.RUN_SPEED_PPS * frame_time

        if self.head_state is not self.NOT_SHOT and self.laser == False:
            self.head_total_frames += 2*self.shot_speed * frame_time
            if self.head_state == self.HEAD_DOWN:
                self.head_frame = 0
            if self.head_state == self.HEAD_RIGHT:
                self.head_frame = 2
            if self.head_state == self.HEAD_UP:
                self.head_frame = 4
            if self.head_state == self.HEAD_LEFT:
                self.head_frame = 6
            self.head_frame += int(self.head_total_frames) % 2

            if self.head_frame%2 == 1 and self.shot_Enable:
                self.bullets[self.current].x=self.x
                self.bullets[self.current].y=self.y

                if self.head_state == self.HEAD_LEFT:
                    self.bullets[self.current].dir_X = -1
                if self.head_state == self.HEAD_RIGHT:
                    self.bullets[self.current].dir_X = 1
                if self.head_state == self.HEAD_UP:
                    self.bullets[self.current].dir_Y = 1
                if self.head_state == self.HEAD_DOWN:
                    self.bullets[self.current].dir_Y = -1

                self.bullets[self.current].dir_X += self.dir_X/10
                self.bullets[self.current].dir_Y += self.dir_Y/10

                self.current = (self.current +1)%8
                self.shot_Enable = False

            elif self.head_frame%2 == 0:
                self.shot_Enable = True
        else:
            self.head_frame = 0

        if self.laser and self.head_state is not self.NOT_SHOT:
            if self.head_state == self.HEAD_DOWN:
                self.head_frame = 0
            if self.head_state == self.HEAD_RIGHT:
                self.head_frame = 2
            if self.head_state == self.HEAD_UP:
                self.head_frame = 4
            if self.head_state == self.HEAD_LEFT:
                self.head_frame = 6
            if self.gauge <2 :
                self.gauge += frame_time
            else:
                self.laser_enable = True
                self.rad += math.pi/70

        if self.laser and self.head_state is self.NOT_SHOT:
            if self.laser_enable == False:
                self.gauge = 0
            else:
                self.laser_shot =True
        if(self.laser_shot):
            self.rad += math.pi/70
            if self.laser_dir == self.HEAD_DOWN:
                self.head_frame = 0
            if self.laser_dir == self.HEAD_RIGHT:
                self.head_frame = 2
            if self.laser_dir == self.HEAD_UP:
                self.head_frame = 4
            if self.laser_dir == self.HEAD_LEFT:
                self.head_frame = 6
            self.gauge+= frame_time
            if self.gauge > 3:
                self.gauge = 0
                self.laser_enable = False
                self.laser_shot = False

        if self.body_state is not self.NOT_MOVE:
            self.body_total_frames += Isaac.FRAMES_PER_ACTION * Isaac.ACTION_PER_TIME * frame_time
            self.body_frame = int(self.body_total_frames) % 10

        else:
            self.body_frame = 0

        self.x += self.dir_X*distance
        self.y += self.dir_Y*distance

        self.collision(frame_time)

    def collision(self,frame_time):
        if collide(self,map):
            if self.x-self.PLAYER_SIZE/2+10 < map.left:
                self.x = map.left + self.PLAYER_SIZE/2-10
            if self.x+self.PLAYER_SIZE/2-10 > map.right:
                self.x = map.right - self.PLAYER_SIZE/2+10
            if self.y-self.PLAYER_SIZE/2 < map.bottom:
                self.y = map.bottom + self.PLAYER_SIZE/2
            if self.y > map.top:
                self.y = map.top

        if collide(self,items[map.stage]) and map.state == 'TOP_ROOM':
            items[map.stage].on_Item = False

            # 상태변화
            self.laser = True

            if self.dir_X != 0:
                if self.y-self.PLAYER_SIZE/2 > items[map.stage].y+15:
                    self.y=items[map.stage].y+20+self.PLAYER_SIZE/2
                elif self.y < items[map.stage].y - 15:
                    self.y = items[map.stage].y -20
                elif self.dir_X ==1:
                    self.x=items[map.stage].x-20-self.PLAYER_SIZE/2+10
                elif self.dir_X == -1:
                    self.x =items[map.stage].x+20+self.PLAYER_SIZE/2-10
            if self.dir_Y != 0:
                if self.x -self.PLAYER_SIZE/2 +10 >items[map.stage].x+15:
                    self.x = items[map.stage].x+20 + self.PLAYER_SIZE/2 -10
                elif self.x +self.PLAYER_SIZE/2 - 10 <items[map.stage].x-15:
                    self.x = items[map.stage].x-20 - self.PLAYER_SIZE/2 +10
                elif self.dir_Y ==1:
                    self.y=items[map.stage].y-20
                elif self.dir_Y == -1:
                    self.y =items[map.stage].y+20+self.PLAYER_SIZE/2

        if self.laser_shot == True:
            if map.state == 'LEFT_ROOM':
                if self.laser_dir == self.HEAD_LEFT and self.y-50 < map.monster_left[map.stage].y and map.monster_left[map.stage].y<self.y+50:
                    map.monster_left[map.stage].hp -= frame_time*20
                if self.laser_dir == self.HEAD_DOWN and self.x-50 < map.monster_left[map.stage].x and map.monster_left[map.stage].x<self.x+50:
                    map.monster_left[map.stage].hp -= frame_time*20
                if self.laser_dir == self.HEAD_RIGHT and self.y-50 < map.monster_left[map.stage].y and map.monster_left[map.stage].y<self.y+50:
                    map.monster_left[map.stage].hp -= frame_time*20
                if self.laser_dir == self.HEAD_UP and self.x-50 < map.monster_left[map.stage].x and map.monster_left[map.stage].x<self.x+50:
                    map.monster_left[map.stage].hp -= frame_time*20

                if map.monster_left[map.stage].hp <= 0:
                    map.inMonster = False
                    map.update()
            if map.state == 'BOTTOM_ROOM':
                if self.laser_dir == self.HEAD_LEFT and self.y-50 < map.monster_bottom[map.stage].y and map.monster_bottom[map.stage].y<self.y+50:
                    map.monster_bottom[map.stage].hp -= frame_time*20
                if self.laser_dir == self.HEAD_DOWN and self.x-50 < map.monster_bottom[map.stage].x and map.monster_bottom[map.stage].x<self.x+50:
                    map.monster_bottom[map.stage].hp -= frame_time*20
                if self.laser_dir == self.HEAD_RIGHT and self.y-50 < map.monster_bottom[map.stage].y and map.monster_bottom[map.stage].y<self.y+50:
                    map.monster_bottom[map.stage].hp -= frame_time*20
                if self.laser_dir == self.HEAD_UP and self.x-50 < map.monster_bottom[map.stage].x and map.monster_bottom[map.stage].x<self.x+50:
                    map.monster_bottom[map.stage].hp -= frame_time*20

                if map.monster_bottom[map.stage].hp <=0:
                    map.inMonster = False
                    map.update()
            if map.state == 'RIGHT_ROOM':
                #for boss in map.monster_boss[map.stage]:
                #    if self.laser_dir == self.HEAD_LEFT and self.y-25 -boss.size < boss.y and boss.y<self.y+25+boss.size:
                #        boss.hp -= frame_time*20
                #    if self.laser_dir == self.HEAD_DOWN and self.x-25 -boss.size < boss.x and boss.x<self.x+25+boss.size:
                #        boss.hp -= frame_time*20
                #    if self.laser_dir == self.HEAD_RIGHT and self.y-25 -boss.size < boss.y and boss.y<self.y+25+boss.size:
                #        boss.hp -= frame_time*20
                #    if self.laser_dir == self.HEAD_UP and self.x-25 -boss.size < boss.x and boss.x<self.x+25+boss.size:
                #        boss.hp -= frame_time*20
#
                #    if boss.hp <=0:
                #        map.inMonster = False
                #        map.update()

                map.inMonster = False
                for i in range(8):
                    if ((self.laser_dir == self.HEAD_UP and self.x - 25 - map.monster_boss[map.stage][i].size < map.monster_boss[map.stage][i].x and map.monster_boss[map.stage][i].x < self.x + 25 + map.monster_boss[map.stage][i].size) or
                        (self.laser_dir == self.HEAD_RIGHT and self.y - 25 - map.monster_boss[map.stage][i].size < map.monster_boss[map.stage][i].y and map.monster_boss[map.stage][i].y < self.y + 25 + map.monster_boss[map.stage][i].size) or
                        (self.laser_dir == self.HEAD_DOWN and self.x - 25 - map.monster_boss[map.stage][i].size < map.monster_boss[map.stage][i].x and map.monster_boss[map.stage][i].x < self.x + 25 + map.monster_boss[map.stage][i].size) or
                        (self.laser_dir == self.HEAD_LEFT and self.y - 25 - map.monster_boss[map.stage][i].size < map.monster_boss[map.stage][i].y and map.monster_boss[map.stage][i].y < self.y + 25 + map.monster_boss[map.stage][i].size)):
                        if map.monster_boss[map.stage][i].hp > 16:
                            map.monster_boss[map.stage][7].hp -= frame_time*2
                            map.monster_boss[map.stage][6].hp -= frame_time*2
                            map.monster_boss[map.stage][5].hp -= frame_time*2
                            map.monster_boss[map.stage][4].hp -= frame_time*2
                            map.monster_boss[map.stage][3].hp -= frame_time*2
                            map.monster_boss[map.stage][2].hp -= frame_time*2
                            map.monster_boss[map.stage][1].hp -= frame_time*2
                            map.monster_boss[map.stage][0].hp -= frame_time*2
                        elif map.monster_boss[map.stage][i].hp > 8:
                            if i >= 4:
                                map.monster_boss[map.stage][7].hp -= frame_time*4
                                map.monster_boss[map.stage][6].hp -= frame_time*4
                                map.monster_boss[map.stage][5].hp -= frame_time*4
                                map.monster_boss[map.stage][4].hp -= frame_time*4
                            else:
                                map.monster_boss[map.stage][3].hp -= frame_time*4
                                map.monster_boss[map.stage][2].hp -= frame_time*4
                                map.monster_boss[map.stage][1].hp -= frame_time*4
                                map.monster_boss[map.stage][0].hp -= frame_time*4
                        elif map.monster_boss[map.stage][i].hp > 4:
                            if i >= 6:
                                map.monster_boss[map.stage][6].hp -= frame_time*6
                                map.monster_boss[map.stage][7].hp -= frame_time*6
                            elif i >= 4:
                                map.monster_boss[map.stage][4].hp -= frame_time*6
                                map.monster_boss[map.stage][5].hp -= frame_time*6
                            elif i >= 2:
                                map.monster_boss[map.stage][2].hp -= frame_time*6
                                map.monster_boss[map.stage][3].hp -= frame_time*6
                            else:
                                map.monster_boss[map.stage][0].hp -= frame_time*6
                                map.monster_boss[map.stage][1].hp -= frame_time*6
                        else:
                            map.monster_boss[map.stage][i].hp -= frame_time*8
                        if (int)(map.monster_boss[map.stage][i].hp) == 16 and map.monster_boss[map.stage][i].split == False:
                            for j in range(8):
                                map.monster_boss[map.stage][j].split = True
                        if (int)(map.monster_boss[map.stage][i].hp)==15 and map.monster_boss[map.stage][i].split == True:
                            for j in range(8):
                                map.monster_boss[map.stage][j].split = False
                            map.monster_boss[map.stage][7].dir_X = -map.monster_boss[map.stage][7].dir_X
                            map.monster_boss[map.stage][6].dir_X = -map.monster_boss[map.stage][6].dir_X
                            map.monster_boss[map.stage][5].dir_X = -map.monster_boss[map.stage][5].dir_X
                            map.monster_boss[map.stage][4].dir_X = -map.monster_boss[map.stage][4].dir_X
                            map.monster_boss[map.stage][7].dir_Y = -map.monster_boss[map.stage][7].dir_Y
                            map.monster_boss[map.stage][6].dir_Y = -map.monster_boss[map.stage][6].dir_Y
                            map.monster_boss[map.stage][5].dir_Y = -map.monster_boss[map.stage][5].dir_Y
                            map.monster_boss[map.stage][4].dir_Y = -map.monster_boss[map.stage][4].dir_Y
                        if (int)(map.monster_boss[map.stage][i].hp) == 9 and map.monster_boss[map.stage][i].split == False:
                            if i >= 4:
                                for j in range(4):
                                    map.monster_boss[map.stage][j+4].split = True
                            else:
                                for j in range(4):
                                    map.monster_boss[map.stage][j].split = True
                        if (int)(map.monster_boss[map.stage][i].hp) == 8 and map.monster_boss[map.stage][i].split==True:
                            if i >= 4:
                                for j in range(4):
                                    map.monster_boss[map.stage][j+4].split = False
                                map.monster_boss[map.stage][7].dir_X = -map.monster_boss[map.stage][7].dir_X
                                map.monster_boss[map.stage][6].dir_X = -map.monster_boss[map.stage][6].dir_X
                                map.monster_boss[map.stage][7].dir_Y = -map.monster_boss[map.stage][7].dir_Y
                                map.monster_boss[map.stage][6].dir_Y = -map.monster_boss[map.stage][6].dir_Y
                            else:
                                for j in range(4):
                                    map.monster_boss[map.stage][j].split = False
                                map.monster_boss[map.stage][3].dir_X = -map.monster_boss[map.stage][3].dir_X
                                map.monster_boss[map.stage][2].dir_X = -map.monster_boss[map.stage][2].dir_X
                                map.monster_boss[map.stage][3].dir_Y = -map.monster_boss[map.stage][3].dir_Y
                                map.monster_boss[map.stage][2].dir_Y = -map.monster_boss[map.stage][2].dir_Y

                        if (int)(map.monster_boss[map.stage][i].hp) == 5 and map.monster_boss[map.stage][i].split==False:
                            if i>=6:
                                    map.monster_boss[map.stage][7].split = True
                                    map.monster_boss[map.stage][6].split = True
                            elif i>=4:
                                    map.monster_boss[map.stage][5].split = True
                                    map.monster_boss[map.stage][4].split = True
                            elif i>=2:
                                    map.monster_boss[map.stage][3].split = True
                                    map.monster_boss[map.stage][2].split = True
                            else:
                                    map.monster_boss[map.stage][1].split = True
                                    map.monster_boss[map.stage][0].split = True
                        if (int)(map.monster_boss[map.stage][i].hp) == 4 and map.monster_boss[map.stage][i].split==True:
                            if i >= 6:
                                map.monster_boss[map.stage][7].split = False
                                map.monster_boss[map.stage][6].split = False
                                map.monster_boss[map.stage][7].dir_X = -map.monster_boss[map.stage][7].dir_X
                                map.monster_boss[map.stage][7].dir_Y = -map.monster_boss[map.stage][7].dir_Y
                            elif i >= 4:
                                map.monster_boss[map.stage][5].split = False
                                map.monster_boss[map.stage][4].split = False
                                map.monster_boss[map.stage][5].dir_X = -map.monster_boss[map.stage][5].dir_X
                                map.monster_boss[map.stage][5].dir_Y = -map.monster_boss[map.stage][5].dir_Y
                            elif i >= 2:
                                map.monster_boss[map.stage][3].split = False
                                map.monster_boss[map.stage][2].split = False
                                map.monster_boss[map.stage][3].dir_X = -map.monster_boss[map.stage][3].dir_X
                                map.monster_boss[map.stage][3].dir_Y = -map.monster_boss[map.stage][3].dir_Y
                            else:
                                map.monster_boss[map.stage][1].split = False
                                map.monster_boss[map.stage][0].split = False
                                map.monster_boss[map.stage][1].dir_X = -map.monster_boss[map.stage][1].dir_X
                                map.monster_boss[map.stage][1].dir_Y = -map.monster_boss[map.stage][1].dir_Y

                if map.monster_boss[map.stage][i].hp > 0:
                    map.inMonster = True

                if map.inMonster == False:
                    map.update()
    def draw(self):
        if self.laser_shot and self.laser_dir == self.HEAD_UP:
            self.laser_image.clip_draw_to_origin(0,0,112,256,self.x-25,self.y+10,50,map.top-self.y)
            self.laser_impact.clip_draw(math.floor(self.rad%2)*64,math.floor((self.rad/2)%2)*64,64,64,self.x,map.top+10,80,80)
        Isaac.body_image.clip_draw(self.body_frame * 32, 320-32*3+self.body_state%3*32 , 32, 32, self.x, self.y-10,self.PLAYER_SIZE,self.PLAYER_SIZE)
        Isaac.head_image.clip_draw(self.head_frame * 32, 320-32*3+self.head_state%3*32 , 32, 32, self.x, self.y+5,self.PLAYER_SIZE,self.PLAYER_SIZE)
        if self.laser_enable and self.laser_shot is False:
            if self.head_state == self.HEAD_DOWN:
                self.laser_swirling.rotate_draw(self.rad,self.x,self.y-10,30,30)
            if self.head_state == self.HEAD_UP:
                self.laser_swirling.rotate_draw(self.rad,self.x,self.y+30,30,30)
            if self.head_state == self.HEAD_RIGHT:
                self.laser_swirling.rotate_draw(self.rad,self.x+20,self.y,30,30)
            if self.head_state == self.HEAD_LEFT:
                self.laser_swirling.rotate_draw(self.rad,self.x-20,self.y,30,30)
        if self.laser_shot:
            if self.laser_dir == self.HEAD_DOWN:
                self.laser_image.clip_draw_to_origin(0,0,112,256,self.x-25,map.bottom-10,50,self.y-map.bottom)
                self.laser_impact.clip_draw((4+math.floor(self.rad%2))*64,math.floor((self.rad/2)%2)*64,64,64,self.x,map.bottom-10,80,80)
            if self.laser_dir == self.HEAD_RIGHT:
                self.laser_image.clip_draw_to_origin(128,0,256,112,self.x+10,self.y-25,map.right-self.x,50)
                self.laser_impact.clip_draw((2+math.floor(self.rad%2))*64,math.floor((self.rad/2)%2)*64,64,64,map.right+10,self.y,80,80)
            if self.laser_dir == self.HEAD_LEFT:
                self.laser_image.clip_draw_to_origin(127,0,256,112,map.left-10,self.y-25,self.x-map.left-10,50)
                self.laser_impact.clip_draw((6+math.floor(self.rad%2))*64,math.floor((self.rad/2)%2)*64,64,64,map.left-10,self.y,80,80)

        for i in range(self.max_hp):
            self.ui_image.clip_draw(32,16,16,16,600+i*25,550,30,30)
        for i in range(math.floor(self.hp)):
            self.ui_image.clip_draw(0,16,16,16,600+i*25,550,30,30)



    def get_bb(self):
        return self.x-self.PLAYER_SIZE/2+10,self.y-self.PLAYER_SIZE/2,self.x + self.PLAYER_SIZE/2-10,self.y

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


def enter():
    global player,map,items

    player =Isaac()
    map = Map()
    items = [Item(i) for i in range(3)]

def exit():
    global player,map,items

    del(player)
    del(map)
    del(items)

def pause():
    pass


def resume():
    pass

def collide(a, b):
    left_a,bottom_a,right_a,top_a=a.get_bb()
    left_b,bottom_b,right_b,top_b=b.get_bb()

    if left_a >right_b : return False
    if right_a < left_b : return False
    if top_a <bottom_b : return False
    if bottom_a > top_b : return False

    return True

def handle_events(frame_time):
    global player
    global map

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(start_state)
            if event.type == SDL_KEYDOWN:
                if event.key ==SDLK_1:
                    player.power =20
                if event.key ==SDLK_2:
                    player.power =1
                    player.laser = False


                if event.key == SDLK_a:
                    player.body_state = player.MOVE_LEFT
                    player.dir_X = -1
                if event.key == SDLK_s:
                    player.body_state = player.MOVE_DOWN
                    player.dir_Y = -1
                if event.key == SDLK_d:
                    player.body_state = player.MOVE_RIGHT
                    player.dir_X = 1
                if event.key == SDLK_w:
                    player.body_state = player.MOVE_UP
                    player.dir_Y = 1

                if event.key == SDLK_LEFT:
                    player.head_state = player.HEAD_LEFT
                elif event.key == SDLK_RIGHT:
                    player.head_state = player.HEAD_RIGHT
                elif event.key == SDLK_UP:
                    player.head_state = player.HEAD_UP
                elif event.key == SDLK_DOWN:
                    player.head_state = player.HEAD_DOWN

            if event.type == SDL_KEYUP:
                if event.key == SDLK_a and player.dir_X == -1:
                    if player.dir_Y == 0:
                        player.body_state = player.NOT_MOVE
                    player.dir_X = 0
                if event.key == SDLK_s and player.dir_Y == -1:
                    if player.dir_X == 0:
                        player.body_state = player.NOT_MOVE
                    player.dir_Y = 0
                if event.key == SDLK_d and player.dir_X == 1:
                    if player.dir_Y == 0:
                        player.body_state = player.NOT_MOVE
                    player.dir_X = 0
                if event.key == SDLK_w and player.dir_Y == 1:
                    if player.dir_X == 0:
                        player.body_state = player.NOT_MOVE
                    player.dir_Y = 0

                if event.key == SDLK_LEFT and player.head_state == player.HEAD_LEFT:
                    player.head_state = player.NOT_SHOT
                    player.laser_dir = player.HEAD_LEFT
                elif event.key == SDLK_RIGHT and player.head_state == player.HEAD_RIGHT:
                    player.head_state = player.NOT_SHOT
                    player.laser_dir = player.HEAD_RIGHT
                elif event.key == SDLK_UP and player.head_state == player.HEAD_UP:
                    player.head_state = player.NOT_SHOT
                    player.laser_dir = player.HEAD_UP
                elif event.key == SDLK_DOWN and player.head_state == player.HEAD_DOWN:
                    player.head_state = player.NOT_SHOT
                    player.laser_dir = player.HEAD_DOWN


def update(frame_time):
    global player, map
    player.update(frame_time)
    if map.state == 'LEFT_ROOM':
        map.monster_left[map.stage].update(frame_time)
    elif map.state == 'BOTTOM_ROOM':
        map.monster_bottom[map.stage].update(frame_time)
    elif map.state == 'RIGHT_ROOM':
        for boss in map.monster_boss[map.stage]:
            boss.update(frame_time)

    for bullet in player.bullets:
        bullet.update(frame_time)
        if not collide(bullet,map):
            bullet.collision = True
        elif collide(bullet,items[map.stage]) and map.state == 'TOP_ROOM':
            bullet.collision = True
        elif collide(bullet,map.monster_left[map.stage]) and bullet.collision==False and map.state == 'LEFT_ROOM'and (bullet.dir_X !=0 or bullet.dir_Y !=0) and map.monster_left[map.stage].hp >0:
            bullet.collision = True
            map.monster_left[map.stage].hp -=player.power
            if map.monster_left[map.stage].hp <=0:
                map.inMonster = False
                map.update()
        elif collide(bullet,map.monster_bottom[map.stage]) and bullet.collision==False and map.state == 'BOTTOM_ROOM'and (bullet.dir_X !=0 or bullet.dir_Y !=0)and map.monster_bottom[map.stage].hp >0:
            bullet.collision = True
            map.monster_bottom[map.stage].hp -=player.power
            if map.monster_bottom[map.stage].hp <=0:
                map.inMonster = False
                map.update()

        # 보스1 충돌알고리즘
        if map.state == 'RIGHT_ROOM':
            map.inMonster = False
            for i in range(8):
                if collide(bullet,map.monster_boss[map.stage][i]) and bullet.collision==False and (bullet.dir_X !=0 or bullet.dir_Y !=0)and map.monster_boss[map.stage][i].hp >0:
                    bullet.collision = True
                    if map.monster_boss[map.stage][i].hp>16:
                        map.monster_boss[map.stage][7].hp -=player.power
                        map.monster_boss[map.stage][6].hp -=player.power
                        map.monster_boss[map.stage][5].hp -=player.power
                        map.monster_boss[map.stage][4].hp -=player.power
                        map.monster_boss[map.stage][3].hp -=player.power
                        map.monster_boss[map.stage][2].hp -=player.power
                        map.monster_boss[map.stage][1].hp -=player.power
                        map.monster_boss[map.stage][0].hp -=player.power
                    elif map.monster_boss[map.stage][i].hp>8:
                        if i>=4:
                            map.monster_boss[map.stage][7].hp -=player.power
                            map.monster_boss[map.stage][6].hp -=player.power
                            map.monster_boss[map.stage][5].hp -=player.power
                            map.monster_boss[map.stage][4].hp -=player.power
                        else:
                            map.monster_boss[map.stage][3].hp -=player.power
                            map.monster_boss[map.stage][2].hp -=player.power
                            map.monster_boss[map.stage][1].hp -=player.power
                            map.monster_boss[map.stage][0].hp -=player.power

                    elif map.monster_boss[map.stage][i].hp>4:
                        if i>=6:
                            map.monster_boss[map.stage][6].hp -=player.power
                            map.monster_boss[map.stage][7].hp -=player.power
                        elif i>=4:
                            map.monster_boss[map.stage][4].hp -=player.power
                            map.monster_boss[map.stage][5].hp -=player.power
                        elif i>=2:
                            map.monster_boss[map.stage][2].hp -=player.power
                            map.monster_boss[map.stage][3].hp -=player.power
                        else:
                            map.monster_boss[map.stage][0].hp -=player.power
                            map.monster_boss[map.stage][1].hp -=player.power

                    else:
                        map.monster_boss[map.stage][i].hp-=1

                    if map.monster_boss[map.stage][i].hp == 16:
                            map.monster_boss[map.stage][7].dir_X =-map.monster_boss[map.stage][7].dir_X
                            map.monster_boss[map.stage][6].dir_X =-map.monster_boss[map.stage][6].dir_X
                            map.monster_boss[map.stage][5].dir_X =-map.monster_boss[map.stage][5].dir_X
                            map.monster_boss[map.stage][4].dir_X =-map.monster_boss[map.stage][4].dir_X
                            map.monster_boss[map.stage][7].dir_Y =-map.monster_boss[map.stage][7].dir_Y
                            map.monster_boss[map.stage][6].dir_Y =-map.monster_boss[map.stage][6].dir_Y
                            map.monster_boss[map.stage][5].dir_Y =-map.monster_boss[map.stage][5].dir_Y
                            map.monster_boss[map.stage][4].dir_Y =-map.monster_boss[map.stage][4].dir_Y
                    if map.monster_boss[map.stage][i].hp == 8:
                        if i>=4:
                            map.monster_boss[map.stage][7].dir_X =-map.monster_boss[map.stage][7].dir_X
                            map.monster_boss[map.stage][6].dir_X =-map.monster_boss[map.stage][6].dir_X
                            map.monster_boss[map.stage][7].dir_Y =-map.monster_boss[map.stage][7].dir_Y
                            map.monster_boss[map.stage][6].dir_Y =-map.monster_boss[map.stage][6].dir_Y
                        else:
                            map.monster_boss[map.stage][3].dir_X =-map.monster_boss[map.stage][3].dir_X
                            map.monster_boss[map.stage][2].dir_X =-map.monster_boss[map.stage][2].dir_X
                            map.monster_boss[map.stage][3].dir_Y =-map.monster_boss[map.stage][3].dir_Y
                            map.monster_boss[map.stage][2].dir_Y =-map.monster_boss[map.stage][2].dir_Y
                    if map.monster_boss[map.stage][i].hp == 4:
                        if i>=6:
                            map.monster_boss[map.stage][7].dir_X =-map.monster_boss[map.stage][7].dir_X
                            map.monster_boss[map.stage][7].dir_Y =-map.monster_boss[map.stage][7].dir_Y
                        if i>=4:
                            map.monster_boss[map.stage][5].dir_X =-map.monster_boss[map.stage][5].dir_X
                            map.monster_boss[map.stage][5].dir_Y =-map.monster_boss[map.stage][5].dir_Y
                        elif i>=2:
                            map.monster_boss[map.stage][3].dir_X =-map.monster_boss[map.stage][3].dir_X
                            map.monster_boss[map.stage][3].dir_Y =-map.monster_boss[map.stage][3].dir_Y
                        else:
                            map.monster_boss[map.stage][1].dir_X =-map.monster_boss[map.stage][1].dir_X
                            map.monster_boss[map.stage][1].dir_Y =-map.monster_boss[map.stage][1].dir_Y

                if map.monster_boss[map.stage][i].hp > 0:
                    map.inMonster = True

            if map.inMonster == False:
                map.update()


    if map.state == 'CENTER_ROOM':
        if collide(player, map.left_door) and map.left_door.lock==map.left_door.OPEN:
            map.state = 'LEFT_ROOM'
            player.x = map.right-50
            if map.monster_left[map.stage].hp>0:
                map.inMonster=True
            map.update()
            for bullet in player.bullets:
                bullet.reset()
        if collide(player, map.right_door) and map.right_door.lock==map.right_door.OPEN:
            map.state = 'RIGHT_ROOM'
            player.x = map.left+50
            map.inMonster=False
            for boss in map.monster_boss[map.stage]:
                if boss.hp>0:
                    map.inMonster=True
            map.update()
            for bullet in player.bullets:
                bullet.reset()
        if collide(player, map.bottom_door) and map.bottom_door.lock==map.bottom_door.OPEN:
            map.state = 'BOTTOM_ROOM'
            player.y= map.top-50
            if map.monster_bottom[map.stage].hp>0:
                map.inMonster=True
            map.update()
            for bullet in player.bullets:
                bullet.reset()
        if collide(player, map.top_door) and map.top_door.lock==map.top_door.OPEN:
            map.state = 'TOP_ROOM'
            player.y= map.bottom+50
            map.update()
            for bullet in player.bullets:
                bullet.reset()

    if map.state == 'LEFT_ROOM' and map.right_door.lock==map.right_door.OPEN:
        if collide(player, map.right_door):
            map.state = 'CENTER_ROOM'
            player.x = map.left+50
            map.update()
            for bullet in player.bullets:
                bullet.reset()
    if map.state == 'RIGHT_ROOM' and map.left_door.lock==map.left_door.OPEN:
        if collide(player, map.left_door):
            map.state = 'CENTER_ROOM'
            player.x = map.right-50
            map.update()
            for bullet in player.bullets:
                bullet.reset()
        if collide(player,map.trap_door):
            map.stage +=1

            map.state = 'CENTER_ROOM'
            player.x,player.y= 400,250
            map.update()
            for bullet in player.bullets:
                bullet.reset()

    if map.state == 'TOP_ROOM' and map.bottom_door.lock==map.bottom_door.OPEN:
        if collide(player, map.bottom_door):
            map.state = 'CENTER_ROOM'
            player.y= map.top-50
            map.update()
            for bullet in player.bullets:
                bullet.reset()
    if map.state == 'BOTTOM_ROOM' and map.top_door.lock==map.top_door.OPEN:
        if collide(player, map.top_door):
            map.state = 'CENTER_ROOM'
            player.y= map.bottom+50
            map.update()
            for bullet in player.bullets:
                bullet.reset()

    for boss in map.monster_boss[map.stage]:
        if collide(boss,map):
            if boss.x - boss.size/2 < map.left:
                boss.dir_X = 1
            if boss.x + boss.size/2 > map.right:
                boss.dir_X = -1
            if boss.y - boss.size/2 < map.bottom:
                boss.dir_Y = 1
            if boss.y + boss.size/2 > map.top:
                boss.dir_Y = -1






def draw(frame_time):
    global player,map,items

    clear_canvas()

    map.draw()
    map.draw_door()
    for bullet in player.bullets:
        bullet.draw()
    if map.state == 'TOP_ROOM':
        items[map.stage].draw()
    if map.state == map.monster_left[map.stage].room:
        map.monster_left[map.stage].draw()
    if map.state == map.monster_bottom[map.stage].room:
        map.monster_bottom[map.stage].draw()
    if map.state == 'RIGHT_ROOM':
        for boss in map.monster_boss[map.stage]:
            boss.draw()
    player.draw()

    player.draw_bb()
    for bullet in player.bullets:
        bullet.draw_bb()
    if map.state == 'TOP_ROOM':
        items[map.stage].draw_bb()
    map.draw_bb()
    map.draw_door_bb()
    if map.state == map.monster_left[map.stage].room:
        map.monster_left[map.stage].draw_bb()
    if map.state == map.monster_bottom[map.stage].room:
        map.monster_bottom[map.stage].draw_bb()
    if map.state == 'RIGHT_ROOM':
        for boss in map.monster_boss[map.stage]:
            boss.draw_bb()

    update_canvas()





