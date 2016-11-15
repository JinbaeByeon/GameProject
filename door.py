from pico2d import *

class Door:

    LEFT_DOOR,BOTTOM_DOOR,RIGHT_DOOR,TOP_DOOR = 0,1,2,3
    OPEN,CLOSE = 1,2
    def __init__(self,name,position):
        self.lock = self.CLOSE
        self.type = name
        self.position = position

        if self.position == 'LEFT':
            self.left =40
            self.right =90
            self.top = 280
            self.bottom = 220
            self.state = self.LEFT_DOOR
        elif self.position == 'BOTTOM':
            self.left =370
            self.right =430
            self.top = 80
            self.bottom = 40
            self.state = self.BOTTOM_DOOR
        elif self.position == 'RIGHT':
            self.left =710
            self.right =760
            self.top = 280
            self.bottom = 220
            self.state = self.RIGHT_DOOR
        elif self.position == 'TOP':
            self.left =370
            self.right =430
            self.top = 460
            self.bottom = 420
            self.state = self.TOP_DOOR
        elif self.position == 'TRAP_DOOR':
            self.left = 380
            self.right = 420
            self. top = 390
            self.bottom = 350

        if self.type == 'bossroom':
            self.image = load_image('bossroom_door.png')
        if self.type == 'normal':
            self.image = load_image('normal_door.png')
        if self.type == 'treasure':
            self.image = load_image('treasure_door.png')
        if self.type == 'trapdoor':
            self.image = load_image('trap_door.png')

    def draw(self):
        if self.type == 'normal':
            self.image.clip_draw(self.lock*60,self.state*50,60,50,(self.left+self.right)/2,(self.bottom+self.top)/2)
            self.image.clip_draw(0,self.state*50,60,50,(self.left+self.right)/2,(self.bottom+self.top)/2)
        elif self.type == 'bossroom':
            if self.state == self.RIGHT_DOOR:
                self.image.clip_draw(self.lock*50,0,50,66,(self.left+self.right)/2,(self.bottom+self.top)/2)
                self.image.clip_draw(0,0,50,66,(self.left+self.right)/2,(self.bottom+self.top)/2)
            elif self.state == self.LEFT_DOOR:
                self.image.clip_draw(self.lock*50,66,50,66,(self.left+self.right)/2,(self.bottom+self.top)/2)
                self.image.clip_draw(0,66,50,66,(self.left+self.right)/2,(self.bottom+self.top)/2)
        elif self.type == 'treasure':
            if self.state == self.TOP_DOOR:
                self.image.clip_draw(self.lock*64,46,64,46,(self.left+self.right)/2,(self.bottom+self.top)/2)
                self.image.clip_draw(0,46,64,46,(self.left+self.right)/2,(self.bottom+self.top)/2)
            elif self.state == self.BOTTOM_DOOR:
                self.image.clip_draw(self.lock*64,0,64,46,(self.left+self.right)/2,(self.bottom+self.top)/2)
                self.image.clip_draw(0,0,64,46,(self.left+self.right)/2,(self.bottom+self.top)/2)
        elif self.type == 'trapdoor':
            self.image.clip_draw(0,0,49,51,(self.left+self.right)/2,(self.bottom+self.top)/2)

    def Lock(self):
        self.lock = self.CLOSE

    def unlock(self):
        self.lock = self.OPEN

    def get_bb(self):
        return self.left, self.bottom,self.right,self.top

    def draw_bb(self):
        draw_rectangle(*self.get_bb())
