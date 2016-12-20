from pico2d import *
import math

class Bullet:

    image = None
    effect = None

    RED_BULLET,WHITE_BULLET =0,2

    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    SHOT_SPEED_KMPH = 40.0                    # Km / Hour
    SHOT_SPEED_MPM = (SHOT_SPEED_KMPH * 1000.0 / 60.0)
    SHOT_SPEED_MPS = (SHOT_SPEED_MPM / 60.0)
    SHOT_SPEED_PPS = (SHOT_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 16

    def __init__(self):
        self.x, self.y = 400, 300
        self.power = 0
        self.color = self.WHITE_BULLET
        self.dir_X = 0
        self.dir_Y = 0
        self.time = 0.0
        self.effect_frame = 0
        self.isEffect = False
        self.collision = False

        if Bullet.image ==None:
            Bullet.image = load_image('graphics\\tears.png')
        if Bullet.effect == None:
            Bullet.effect = load_image('graphics\\tears_effect.png')

    def reset(self):
        self.x, self.y = 400,300
        self.dir_X = 0
        self.dir_Y = 0
        self.time = 0.0
        self.effect_frame = 0
        self.isEffect = False
        self.collision = False

    def update(self, frame_time):
        distance = Bullet.SHOT_SPEED_PPS * frame_time
        self.x += distance*self.dir_X
        self.y += distance*self.dir_Y
        if(self.dir_X  != 0 or self.dir_Y != 0):
            self.time += frame_time
        if self.time >= 1 or self.collision:
            self.isEffect = True
            self.dir_X = 0
            self.dir_Y = 0
            self.effect_frame += Bullet.FRAMES_PER_ACTION * Bullet.ACTION_PER_TIME *frame_time
            if self.effect_frame >= 15:
                self.reset()



    def draw(self):
        if (self.time < 1 and (self.dir_X != 0 or self.dir_Y != 0)):
            self.image.clip_draw(self.power*32, self.color*32 , 32, 32, self.x, self.y)
        elif self.isEffect:
            self.effect.clip_draw(((int)(self.effect_frame)%4)*64,(3-math.floor(self.effect_frame/4))*64,64,64,self.x,self.y)


    def get_bb(self):
        return self.x-10,self.y-10,self.x+10,self.y+10

    def draw_bb(self):
        if self.dir_X !=0 or self.dir_Y != 0 or self.isEffect:
            draw_rectangle(*self.get_bb())
