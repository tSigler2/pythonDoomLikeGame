from sprite_object import *
from npc import *
from pick_ups import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.pick_up_list = []
        self.npc_sprite_path = 'Assets/NPCs'
        self.static_sprite_path = 'Assets/static_sprites/'
        self.anim_sprite_path = 'Assets/Animated_Sprites'

        add_sprite = self.add_sprite
        add_npc = self.add_npc
        add_pick_up = self.add_pick_up
        self.npc_pos = {}

        add_sprite(SpriteObj(game))
        add_sprite(Animated_Sprite(game, pos=(14.5, 2.5)))
        add_sprite(Animated_Sprite(game, pos=(14.5, 6)))

        add_npc(NPC(game))
        add_npc(NPC(game, pos=(11.5, 4.5)))
        add_npc(NPC(game, pos=(16.5, 7.5)))
        add_npc(NPC(game, path='Assets/NPCs/glass_cannon/0.png', pos=(2, 19), speed=0.5, health=500))
        add_npc(NPC(game, path='Assets/NPCs/glass_cannon/0.png', pos=(15, 19), speed=0.5, health=500))

        add_pick_up(HealthPickUp(game, pos=(3, 11)))

    def update(self):
        self.npc_pos = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        [pick_up.update() for pick_up in self.pick_up_list]
    
    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_pick_up(self, pu):
        self.pick_up_list.append(pu)
