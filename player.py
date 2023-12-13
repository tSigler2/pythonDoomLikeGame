from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = P_POS
        self.angle = P_ANGLE
        self.shot = False
        self.health = P_MAX_HEALTH

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True

    def get_damage(self, damage):
        self.health -= damage
        self.game.objRenderer.player_pain()
        self.game.sound.player_damage.play()

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        speed = P_SPEED * self.game.delta_time
        dx, dy = 0, 0

        keys = pg.key.get_pressed()
        
        if keys[pg.K_LSHIFT]:
            speed *= 2
            speed *= 2
        
        speed_sin = sin_a * speed
        speed_cos = cos_a * speed

        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos

        self.check_wall_collision(dx, dy)
        
        self.angle %= math.tau

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 50, self.y * 50), (self.x * 100 + WIDTH * math.cos(self.angle), self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 50, self.y * 50), 15)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = P_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
        
    def update(self):
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
