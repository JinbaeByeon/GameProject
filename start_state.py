import game_framework
from pico2d import *


import isaac

name = "StartState"
image = None
bgm = None

def enter():
    global image,bgm
    open_canvas()
    image = load_image('graphics\\titlemenu.png')
    bgm = load_music('sounds\\title_bgm.mp3')
    bgm.set_volume(64)
    bgm.repeat_play()


def exit():
    global image,bgm
    del(image)
    del(bgm)
    close_canvas()

def update(frame_time):
    pass
#    global name
#    global logo_time
#
#    if (logo_time > 0.2):
#        logo_time = 0
#        #game_framework.quit()
#    logo_time += frame_time

def draw(frame_time):
    global image
    clear_canvas()
    image.clip_draw(0,270,480, 270,400,300,800,600)
    image.clip_draw(0,0,480, 270,400,300,800,600)
    update_canvas()

def handle_events(frame_time):
    global bgm
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                del(bgm)
                game_framework.push_state(isaac)


def pause(): pass
def resume(): pass




