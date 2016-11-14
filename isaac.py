import random
import json
import os

from pico2d import *

import game_framework


name = "MainState"

player = None
map =None
font = None






class Isaac:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    RUN_SPEED_KMPH = 20.0                    # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.7
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 10

    PLAYER_SIZE = 60

    head = None
    body = None

    MOVE_LEFT, MOVE_RIGHT= 0,3
    MOVE_UP,MOVE_DOWN,NOT_MOVE = 1,4,7
    HEAD_LEFT,HEAD_RIGHT,HEAD_UP,HEAD_DOWN,NOT_SHOT =2,5,8,11,14

    def __init__(self):
        self.x, self.y = 400, 300
        self.shot_speed =3
        self.head_frame = 0
        self.head_total_frames = 0.0
        self.body_frame =0
        self.body_total_frames = 0.0
        self.dir_X = 0
        self.dir_Y = 0
        self.head_state = self.NOT_SHOT
        self.body_state = self.NOT_MOVE
        if Isaac.head == None:
            Isaac.head_image = load_image('isaac.png')
        if Isaac.body == None:
            Isaac.body_image = load_image('isaac.png')

    def update(self, frame_time):
        distance = Isaac.RUN_SPEED_PPS * frame_time
        if self.head_state is not self.NOT_SHOT:
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
        else:
            self.head_frame = 0

        if self.body_state is not self.NOT_MOVE:
            self.body_total_frames += Isaac.FRAMES_PER_ACTION * Isaac.ACTION_PER_TIME * frame_time
            self.body_frame = int(self.body_total_frames) % 10

        else:
            self.body_frame = 0

        self.x += self.dir_X*distance
        self.y += self.dir_Y*distance




    def draw(self):
        self.body_image.clip_draw(self.body_frame * 32, 320-32*3+self.body_state%3*32 , 32, 32, self.x, self.y-10,self.PLAYER_SIZE,self.PLAYER_SIZE)
        self.head_image.clip_draw(self.head_frame * 32, 320-32*3+self.head_state%3*32 , 32, 32, self.x, self.y+5,self.PLAYER_SIZE,self.PLAYER_SIZE)

    def get_bb(self):
        return self.x-self.PLAYER_SIZE/2,self.y-self.PLAYER_SIZE/2,self.x + self.PLAYER_SIZE/2,self.y + self.PLAYER_SIZE/2

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


def enter():
    global player,map

    player =Isaac()

def exit():
    global player,map

    del(player)
    del(map)

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

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                # game_framework.change_state(title_state)
                pass
            if event.type == SDL_KEYDOWN:
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
                elif event.key == SDLK_RIGHT and player.head_state == player.HEAD_RIGHT:
                    player.head_state = player.NOT_SHOT
                elif event.key == SDLK_UP and player.head_state == player.HEAD_UP:
                    player.head_state = player.NOT_SHOT
                elif event.key == SDLK_DOWN and player.head_state == player.HEAD_DOWN:
                    player.head_state = player.NOT_SHOT


def update(frame_time):
    global player
    player.update(frame_time)


def draw(frame_time):
    global player,map

    clear_canvas()
    player.draw()

    player.draw_bb()

    update_canvas()





