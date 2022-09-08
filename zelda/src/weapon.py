import pygame
from player import Player
from typing import List
from debug import debug

class Weapon(pygame.sprite.Sprite):
    def __init__(
        self,
        player: Player,
        groups: List[pygame.sprite.Group]
    ):
        super().__init__(groups)
        
        self.direction = player.status.split('_')[0]

        # graphic
        full_path = f'../graphics/weapons/{player.weapon}/{self.direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        # placement
        match self.direction:
            case "right":        
                self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
            case 'left':
                self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
            case 'down':
                self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
            case _:
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))