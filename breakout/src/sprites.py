from random import choice
import pygame
from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, groups) -> None:
        super().__init__(groups)

        # setup
        self.image = pygame.Surface((WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))
        self.image.fill('red')

        # position
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - WINDOW_HEIGHT // 36))        
        self.old_rect = self.rect.copy()        
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0        

    def screen_constraint(self):
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.pos.x = self.rect.x
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x

    def update(self, dt):
        self.old_rect = self.rect.copy()        
        self.input()
        self.screen_constraint()
        self.pos.x += self.speed * self.direction.x * dt
        self.rect.x = round(self.pos.x)

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, player: Player):
        super().__init__(groups)

        # collision objects
        self.player = player

        # graphics setup
        self.image = pygame.image.load('../graphics/other/ball.png').convert_alpha()

        # position setup
        self.rect = self.image.get_rect(midbottom = self.player.rect.midtop)
        self.old_rect = self.rect.copy()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2((choice((1,-1)),-1))
        self.speed = 400

        # active
        self.active = False

    def window_collision(self,direction):
        if direction == 'horizontal':
            if self.rect.right > WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
                self.pos.x = self.rect.x
                self.direction.x *= -1

            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1

        if direction == 'vertical':
            if self.rect.top < 0:
                self.direction.y *= -1
                self.rect.top = 0
                self.pos.y = self.rect.y                
            if self.rect.top > WINDOW_HEIGHT:
                self.active = False
                self.direction.y = -1
                self.rect.top = WINDOW_HEIGHT
                self.pos.y = self.rect.y


    def collision(self, direction):
        # find overlapping objects
        overlap_sprites = []
        if self.rect.colliderect(self.player.rect):
            overlap_sprites.append(self.player)

        if overlap_sprites:
            if direction == "horizontal":
                for sprite in overlap_sprites:
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left: # left to right
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right: # right to left
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x
                        self.direction.x *= -1

            if direction == "vertical":
                for sprite in overlap_sprites:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top: # top to bottom
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom: # bottom to top
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                        self.direction.y *= -1

    def update(self, dt):
        if self.active:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            # create old_rect
            self.old_rect = self.rect.copy()

            # horizontal movement + collision
            self.pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.pos.x)
            self.collision('horizontal')
            self.window_collision('horizontal')
            
            # vertical movement + collision
            self.pos.y += self.direction.y * self.speed * dt
            self.rect.y = round(self.pos.y)            
            self.collision('vertical')
            self.window_collision('vertical')
        else:
            self.rect.midbottom = self.player.rect.midtop
            self.pos = pygame.math.Vector2(self.rect.topleft)