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
        self.input()
        self.screen_constraint()
        self.pos.x += self.speed * self.direction.x * dt
        self.rect.x = round(self.pos.x)