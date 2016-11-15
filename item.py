from pico2d import *

class Item:
    def __init__(self, stage):
        self.x,self.y = 400,250
        self.on_Item = True
        self.stone_image = load_image('itemstone.png')
        if stage ==0:
            self.item_image = load_image('item_brimstone.png')
        elif stage ==1:
            self.item_image = load_image('item_brimstone.png')
        elif stage ==2:
            self.item_image = load_image('item_brimstone.png')

    def draw(self):
        self.stone_image.draw(400, 250,40,40)
        if self.on_Item:
            self.item_image.draw(400,260,30,30)

    def get_bb(self):
        return self.x -20, self.y-20, self.x+20, self.y+20

    def draw_bb(self):
        draw_rectangle(*self.get_bb())