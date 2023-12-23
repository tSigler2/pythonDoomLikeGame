import pygame as pg
import time
import math
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_render import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.glob_trigger = False
        self.glob_event = pg.USEREVENT + 0
        pg.time.set_timer(self.glob_event, 40)
        self.new_game()
        self.music_swap = 0
        self.END_MUSIC_BOX = pg.USEREVENT + 616
        self.end_game = False

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.objRenderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)
        
    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick()
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        #self.screen.fill('black')
        self.objRenderer.draw()
        self.weapon.draw()
        self.player.draw_health_bar()
        self.player.draw_ammo_count()
        #self.map.draw()
        #self.player.draw()

    def check_events(self):
        self.glob_trigger = False
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif e.type == self.glob_event:
                self.glob_trigger = True
            elif e.type == pg.KEYDOWN and e.key == pg.K_m and pg.mixer.music.get_busy():
                pg.mixer.music.pause()
            elif e.type == pg.KEYDOWN and e.key == pg.K_m and not pg.mixer.music.get_busy():
                pg.mixer.music.unpause()
            self.player.single_fire_event(e)
            if e.type == self.END_MUSIC_BOX and self.music_swap == 0:
                pg.mixer.music.unload()
                pg.mixer.music.load(self.sound.path + 'theme.mp3')
                pg.mixer.music.play(-1)
                self.music_swap = 1
                self.player.x = 16.5
                self.player.y = 17.5
    
    def run(self):
        while not self.end_game:
            self.check_events()
            self.update()
            self.draw()
            if self.player.health <= 0:
                break
        if self.player.health <= 0:
            self.objRenderer.draw_end_screen()
        else:
            self.objRender.draw_win()
        pg.mixer.music.stop()
        pg.display.flip()
        time.sleep(3)
        self.sound.shotgun.play()
        while True:
            self.check_events()
if __name__ == '__main__':
    game = Game()
    game.run()
