from settings import *
from npc import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = P_POS
        self.angle = P_ANGLE
        self.shot = False
        self.health = P_MAX_HEALTH
        self.ammo = P_AMMO
        self.ammo_font = pg.font.SysFont('chalkduster.ttf', 36)

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.ammo > 0:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.ammo -= 1
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

    def draw_health_bar(self):
        ratio = self.health/P_MAX_HEALTH
        if ratio < 0:
            ratio = 0
        
        pg.draw.rect(self.game.screen, 'black', (50, 50, 300, 40))
        pg.draw.rect(self.game.screen, 'green', (50, 50, 300 * ratio, 40))
        
    def draw_ammo_count(self):
        ammo_img = self.ammo_font.render('Ammo: ' + str(self.ammo), True, (0, 0, 0))
        self.game.screen.blit(ammo_img, (50, 95))

    def check_npcs(self):
        self.check_list = []
        end_game = True

        for npc in self.game.object_handler.npc_list:
            if isinstance(npc, TaggedNPC):
                if npc.tag == 4:
                    self.check_list.append(npc)

        for npc in self.check_list:
            if npc.alive:
                end_game = False

        if end_game:
            self.x = 32.5
            self.y = 27.5
        
    def update(self):
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
