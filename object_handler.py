from sprite_object import *
from npc import *
from pick_ups import *
from interactable_objects import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.pick_up_list = []
        self.interactable_list = []
        self.npc_sprite_path = 'Assets/NPCs'
        self.static_sprite_path = 'Assets/static_sprites/'
        self.anim_sprite_path = 'Assets/Animated_Sprites'

        add_sprite = self.add_sprite
        add_npc = self.add_npc
        add_pick_up = self.add_pick_up
        add_interactable = self.add_interactable
        self.npc_pos = {}

        add_sprite(SpriteObj(game))
        add_sprite(Animated_Sprite(game, pos=(14.5, 2.5)))
        add_sprite(Animated_Sprite(game, pos=(14.5, 6)))

        add_npc(NPC(game))
        add_npc(NPC(game, pos=(11.5, 4.5)))
        add_npc(NPC(game, pos=(16.5, 7.5)))
        add_npc(NPC(game, path='Assets/NPCs/glass_cannon/0.png', pos=(2, 19), speed=0.5, health=500))
        add_npc(NPC(game, path='Assets/NPCs/glass_cannon/0.png', pos=(15, 19), speed=0.5, health=500))
        add_npc(TaggedNPC(game, pos=(22.5, 5.5), tag=0))
        add_npc(TaggedNPC(game, pos=(24.5, 11.5), tag=1))
        add_npc(TaggedNPC(game, pos=(22.5, 17.5), tag=2))
        add_npc(TaggedNPC(game, pos=(24.5, 23.5), tag=3))

        add_pick_up(HealthPickUp(game, pos=(3, 11)))
        add_pick_up(AmmoPickUp(game))

        add_pick_up(HealthPickUp(game, pos=(22.5, 1.61)))
        add_pick_up(HealthPickUp(game, pos=(22.5, 9.39)))
        add_pick_up(HealthPickUp(game, pos=(24.5, 15.39)))
        add_pick_up(HealthPickUp(game, pos=(24.5, 7.61)))
        add_pick_up(HealthPickUp(game, pos=(22.5, 21.39)))
        add_pick_up(HealthPickUp(game, pos=(22.5, 13.61)))
        add_pick_up(HealthPickUp(game, pos=(24.5, 27.39)))
        add_pick_up(HealthPickUp(game, pos=(24.5, 19.61)))

        add_pick_up(AmmoPickUp(game, pos=(26.39, 5.5)))
        add_pick_up(AmmoPickUp(game, pos=(18.61, 5.5)))
        add_pick_up(AmmoPickUp(game, pos=(28.39, 11.5)))
        add_pick_up(AmmoPickUp(game, pos=(20.61, 11.5)))
        add_pick_up(AmmoPickUp(game, pos=(26.39, 17.5)))
        add_pick_up(AmmoPickUp(game, pos=(18.61, 17.5)))
        add_pick_up(AmmoPickUp(game, pos=(28.39, 23.5)))
        add_pick_up(AmmoPickUp(game, pos=(20.61, 23.5)))

        add_interactable(Portal(game, pos=(16.5, 7.9), teleport_location=(22.5, 1.61)))
        add_interactable(Portal(game, path='Assets/Animated_Sprites/BlackHole/0.png', pos=(29.5, 18.5), teleport_location=(31.5, 5.5)))
        add_interactable(SwitchablePortal(game, pos = (22.5, 1.2), orig_location=(22.5, 9.39), alt_location=(24.5, 15.39), tag=0))
        add_interactable(SwitchablePortal(game, pos=(22.5, 9.8), orig_location=(22.5, 1.61), alt_location=(24.5, 7.61), tag=0))
        add_interactable(SwitchablePortal(game, pos=(18.2, 5.5), orig_location=(26.39, 5.5), alt_location=(28.39, 11.5), tag=0))
        add_interactable(SwitchablePortal(game, pos=(26.8, 5.5), orig_location=(18.61, 5.5), alt_location=(20.61, 11.5), tag=0))
        add_interactable(SwitchablePortal(game, pos=(24.5, 7.2), orig_location=(24.5, 15.39), alt_location=(22.5, 21.39), tag=1))
        add_interactable(SwitchablePortal(game, pos=(24.5, 15.8), orig_location=(24.5, 7.61), alt_location=(22.5, 13.61), tag=1))
        add_interactable(SwitchablePortal(game, pos=(20.2, 11.5), orig_location=(28.39, 11.5), alt_location=(26.39, 17.5), tag=1))
        add_interactable(SwitchablePortal(game, pos=(28.8, 11.5), orig_location=(20.61, 11.5), alt_location=(18.61, 17.5), tag=1))
        add_interactable(SwitchablePortal(game, pos=(22.5, 13.2), orig_location=(22.5, 21.39), alt_location=(24.5, 27.39), tag=2))
        add_interactable(SwitchablePortal(game, pos=(22.5, 21.8), orig_location=(22.5, 13.61), alt_location=(24.5, 19.61), tag=2))
        add_interactable(SwitchablePortal(game, pos=(18.2, 17.5), orig_location=(26.39, 17.5), alt_location=(28.39, 23.5), tag=2))
        add_interactable(SwitchablePortal(game, pos=(26.8, 17.5), orig_location=(18.61, 17.5), alt_location=(20.61, 23.5), tag=2))
        add_interactable(SwitchablePortal(game, pos=(24.5, 19.2), orig_location=(24.5, 27.39), alt_location=(28.5, 19.5), tag=3))
        add_interactable(SwitchablePortal(game, pos=(24.5, 27.8), orig_location=(24.5, 19.61), alt_location=(28.5, 17.5), tag=3))
        add_interactable(SwitchablePortal(game, pos=(20.2, 23.5), orig_location=(28.39, 23.5), alt_location=(27.5, 18.5), tag=3))
        add_interactable(SwitchablePortal(game, pos=(28.8, 23.5), orig_location=(20.61, 23.5), alt_location=(29.5, 18.5), tag=3))
        
        

    def update(self):
        self.npc_pos = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        [pick_up.update() for pick_up in self.pick_up_list]
        [interactable.update() for interactable in self.interactable_list]
    
    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_pick_up(self, pu):
        self.pick_up_list.append(pu)

    def add_interactable(self, interactable):
        self.interactable_list.append(interactable)
