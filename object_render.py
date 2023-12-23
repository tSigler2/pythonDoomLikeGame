import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('Assets/sky.png', (WIDTH, HALF_HEIGHT))
        self.p_pain = self.get_texture('Assets/blood_screen.png', RES)
        self.death_screen = self.get_texture('Assets/game_over.png', RES)
        self.sky_offset = 0
        self.sky_mode = 0
        self.font = pg.font.SysFont('chalkduster.ttf', 72)

    def draw(self):
        self.draw_background()
        self.render_objects()

    def draw_background(self):
        if self.sky_mode == 1:
            self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
            self.screen.blit(self.sky_image, (-self.sky_offset, 0))
            self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        elif self.sky_mode == 2:
            pg.draw.rect(self.screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        else:
            pg.draw.rect(self.screen, CEIL_COLOR, (0, 0, WIDTH, HEIGHT))
        if self.sky_mode == 2:
            pg.draw.rect(self.screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        else:
            pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def draw_end_screen(self):
        self.screen.blit(self.death_screen, (0, 0))

    def draw_win(self):
        self.draw.rect(self.screen, (255, 255, 255), (0, 0, WIDTH, HEIGHT))
        end_text = self.font.render('You win!!', True, (0, 0, 0))
        self.game.screen.blit(end_text, (WIDTH/4, HEIGHT/4))

    def render_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos, in list_objects:
            self.screen.blit(image, pos)

    def player_pain(self):
        self.screen.blit(self.p_pain, (0, 0))

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
                1: self.get_texture('Assets/BrickWall.png'),
                2: self.get_texture('Assets/WoodWall.png'),
                3: self.get_texture('Assets/BlackWall.png')
            }
