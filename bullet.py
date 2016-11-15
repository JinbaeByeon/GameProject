from pico2d import *

class Bullet:

    image = None
    effect = None

    RED_BULLET,WHITE_BULLET =0,2

    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    SHOT_SPEED_KMPH = 40.0                    # Km / Hour
    SHOT_SPEED_MPM = (SHOT_SPEED_KMPH * 1000.0 / 60.0)
    SHOT_SPEED_MPS = (SHOT_SPEED_MPM / 60.0)
    SHOT_SPEED_PPS = (SHOT_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self):
        self.x, self.y = 0,0
        self.power = 0
        self.color = self.WHITE_BULLET
        self.dir_X = 0
        self.dir_Y = 0
        self.time = 0.0

        if Bullet.image ==None:
            Bullet.image = load_image('tears.png')
        if Bullet.effect == None:
            Bullet.effect = load_image('tears_effect.png')

    def update(self, frame_time):
        distance = Bullet.SHOT_SPEED_PPS * frame_time
        self.x += distance*self.dir_X
        self.y += distance*self.dir_Y
        if(self.dir_X  != 0 or self.dir_Y != 0):
            self.time += frame_time


    def draw(self):
        if self.time < 1:
            self.image.clip_draw(self.power*32, self.color*32 , 32, 32, self.x, self.y)

    def get_bb(self):
        return self.x-10,self.y-10,self.x+10,self.y+10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
