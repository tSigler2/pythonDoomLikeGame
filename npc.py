from sprite_object import *
from random import randint, random, choice

class NPC(Animated_Sprite):
    def __init__(self, game, path='Assets/NPCs/soldier/0.png', pos=(10.5, 5.5), scale=0.6, shift=0.38, animation_time=180, speed=0.03, health=100):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/Attack')
        self.death_images = self.get_images(self.path + '/Death')
        self.idle_images = self.get_images(self.path + '/Idle')
        self.pain_images = self.get_images(self.path + '/Pain')
        self.walk_images = self.get_images(self.path + '/Walk')
        self.attack_dist = randint(3, 6)
        self.speed = speed
        self.size = 10
        self.health = health
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_val = False
        self.player_search = False

        self.frame_counter = 0

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run()
        #self.draw_raycast()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy
    
    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        #pg.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
        if next_pos not in self.game.object_handler.npc_pos:
            angle = math.atan2(next_y + 0.5 - self.y, next_x+0.5-self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_attack.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)
    
    def animate_death(self):
        if not self.alive:
            if self.game.glob_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1
    
    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_shot(self):
        if self.game.player.shot and self.ray_cast_npc():
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health <= 0:
            self.alive = False
            self.game.sound.npc_death.play()
    
    def run(self):
        if self.alive:
            self.check_shot()
            if self.pain:
                self.animate_pain()
            elif self.ray_cast_npc():
                self.player_search = True

                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_search:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    def ray_cast_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        p_dist_v, p_dist_h = 0, 0
        
        px, py = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_hor = 1, 1
        
        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - py)/sin_a
        x_hor = px + depth_hor*cos_a

        delta_depth = dy/sin_a
        dx = delta_depth*cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                p_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
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
            if tile_vert == self.map_pos:
                p_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        p_dist = max(p_dist_v, p_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < p_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_raycast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_npc():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y), (100 * self.x, 100 * self.y), 2)

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
