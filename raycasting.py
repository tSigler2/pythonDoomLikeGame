import pygame as pg
import math
from settings import *
import random

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_cast_result = []
        self.objects_to_render = []
        self.textures = self.game.objRenderer.wall_textures

    def get_objs_to_render(self):
        self.objects_to_render = []

        for ray, vals, in enumerate(self.ray_cast_result):
            depth, projection_height, texture, offset = vals

            if projection_height < HEIGHT:
                wall_col = self.textures[texture].subsurface(offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE)
                wall_col = pg.transform.scale(wall_col, (SCALE, projection_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - projection_height//2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT/projection_height
                wall_col = self.textures[texture].subsurface(offset * (TEXTURE_SIZE - SCALE), (HALF_TEXTURE_SIZE - texture_height//2), SCALE, texture_height)
                wall_col = pg.transform.scale(wall_col, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)
            self.objects_to_render.append((depth, wall_col, wall_pos))

    def ray_cast(self):
        self.ray_cast_result = []
        px, py = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_hor = 1, 1
        
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001

        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - py)/sin_a
            x_hor = px + depth_hor*cos_a

            delta_depth = dy/sin_a
            dx = delta_depth*cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            delta_depth = dx/cos_a

            depth_vert = (x_vert - px)/cos_a
            y_vert = py + depth_vert * sin_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1-x_hor) if sin_a > 0 else x_hor
                

            depth *= math.cos(self.game.player.angle - ray_angle)
            projection_height = SCREEN_DIST/(depth + 0.0001)

            self.ray_cast_result.append((depth, projection_height, texture, offset))
            
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objs_to_render()
