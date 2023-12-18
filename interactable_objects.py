from sprite_object import *
from npc import *

class Interactable_No_Key(Animated_Sprite):
    def __init__(self, game, path, pos, scale, shift, animation_time, pick_up_dist):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.pick_up_dist = pick_up_dist

    def check_player(self):
        p_pos = self.game.player.pos

        if (self.x - self.pick_up_dist) <= p_pos[0] <= (self.x + self.pick_up_dist) and (self.y - self.pick_up_dist) <= p_pos[1] <= (self.y + self.pick_up_dist):
            return True
        return False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.animate(self.images)
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y)

class Portal(Interactable_No_Key):
    def __init__(self, game, path='Assets/Animated_Sprites/Portal/0.png', pos=(16.5, 7.9), scale=1, shift=0, animation_time=100, teleport_location=(2.0, 12.0), pick_up_dist=0.4):
        super().__init__(game, path, pos, scale, shift, animation_time, pick_up_dist)
        self.teleport_location = teleport_location

    def teleport(self):
        for npc in self.game.object_handler.npc_list:
            npc.player_search = False
        self.game.player.x = self.teleport_location[0]
        self.game.player.y = self.teleport_location[1]

    def update(self):
        super().update()

        if self.check_player():
            self.teleport()

class SwitchablePortal(Interactable_No_Key):
    def __init__(self, game, path='Assets/Animated_Sprites/Portal/0.png', pos=(1.5, 1.5), scale=1, shift=0, animation_time=100, orig_location=(1, 1), alt_location=(1, 1), tag=0, pick_up_dist=0.4):
        super().__init__(game, path, pos, scale, shift, animation_time, pick_up_dist)
        self.orig_location = orig_location
        self.alt_location = alt_location
        self.tag = tag
        self.orig_location = orig_location
        self.alt_location = alt_location

    def teleport(self):
        self.check_list = []
        alt_ready = True
        
        for npc in self.game.object_handler.npc_list:
            npc.player_search = False
            if isinstance(npc, TaggedNPC):
                if (npc.tag == self.tag):
                    self.check_list.append(npc)

        for npc in self.check_list:
            if npc.alive:
                alt_ready = False

        if alt_ready:
            self.game.player.x, self.game.player.y = self.alt_location[0], self.alt_location[1]
            if self.tag == 3:
                self.game.objRenderer.sky_mode = 1
                pg.mixer.music.stop()
                pg.mixer.music.unload()
                pg.mixer.music.load(self.game.sound.path + 'Music_box.ogg')
                pg.mixer.music.set_endevent(self.game.END_MUSIC_BOX)
        else:
            self.game.player.x, self.game.player.y = self.orig_location[0], self.orig_location[1]

    def update(self):
        super().update()

        if self.check_player():
            self.teleport()

class BlackHole(Portal):
    def __init__(self, game, path='Assets/Animated_Sprites/BlackHole/0.png', pos=(16.5, 7.9), scale=1, shift=0, animation_time=100, teleport_location=(2.0, 12.0), pick_up_dist=0.1):
        super().__init__(game, path, pos, scale, shift, animation_time, teleport_location, pick_up_dist)

    def update():
        if self.check_player():
            pg.mixer.music.play()
        
        super().update()


    

        
            
