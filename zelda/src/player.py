from typing import List, Tuple
import pygame 
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(
		self, 
		pos: Tuple[int,int],
		groups: List[pygame.sprite.Group], 
		obstacle_sprites: pygame.sprite.Group
	):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)
		
		# movement
		self.speed = 8
		self.direction = pygame.math.Vector2()
		
		# obstacles
		self.obstacle_sprites = obstacle_sprites

	def get_input(self):
		keys = pygame.key.get_pressed()

		# horizontal
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1			
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1	
		else:
			self.direction.x = 0

		# vertical
		if keys[pygame.K_UP]:
			self.direction.y = -1
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0	
	
	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()
		
		self.hitbox.x += self.direction.x * speed
		self.collision("horziontal")
		self.hitbox.y += self.direction.y * speed		
		self.collision("vertical")
		self.rect.center = self.hitbox.center

	def collision(self,direction):
		if direction == 'horziontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom

	def update(self):
		self.get_input()
		self.move(self.speed)		