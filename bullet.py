from pico2d import *

class bullet:

    image = None

    RED_BULLET,WHITE_BULLET =0,2

    def __init__(self):
        self.x, self.y = 0,0
        self.power = 0
        self.color = self.WHITE_BULLET
        if bullet.image ==None:
            bullet.image = load_image('tears.png')

    def update(self, frame_time):
        pass

    def draw(self):
        self.image.clip_draw(self.power*32, self.color*32 , 32, 32, self.x, self.y)

    def get_bb(self):
        return self.x-10,self.y-10,self.x+10,self.y+10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())