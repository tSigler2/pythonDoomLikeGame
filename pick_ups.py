from sprite_object import *

class PickUp(Animated_Sprite):
    def __init__(self, game, path, pos, scale, shift, animation_time):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.pick_up_dist = 1
        self.picked_up = False
        
    def check_player(self):
        p_pos = self.game.player.pos

        if (self.x - self.pick_up_dist) <= p_pos[0] <= (self.x + self.pick_up_dist) and (self.y - self.pick_up_dist) <= p_pos[1] <= (self.y + self.pick_up_dist):
            return True
        return False
    

class HealthPickUp(PickUp):
    def __init__(self, game, path='Assets/Animated_Sprites/Heart/0.png', pos=(17, 7.5), scale=0.35, shift=0.8, animation_time=180, health_amount=20):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.health_amount = health_amount

    def add_health(self):
        self.game.player.health += self.health_amount
        self.picked_up = True

        if self.game.player.health > 100:
            self.game.player.health = 100
        

    def update(self):
        if not self.picked_up:
            self.check_animation_time()
            self.get_sprite()
            self.animate(self.images)

            if self.check_player():
                self.add_health()
                print(self.game.player.health)
        
        
    @property
    def map_pos(self):
        return int(self.x), int(self.y)
