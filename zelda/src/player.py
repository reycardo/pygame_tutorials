from typing import List, Tuple
import pygame 
from settings import *
from debug import debug
from support import import_folder

class Player(pygame.sprite.Sprite):
	def __init__(
		self, 
		pos: Tuple[int,int],
		groups: List[pygame.sprite.Group], 
		obstacle_sprites: pygame.sprite.Group,
		create_attack,
		destroy_attack
	):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)
		
		# graphics setup
		self.import_player_assets()
		self.status = "down"
		self.frame_index = 0
		self.animation_speed = 0.15

		# movement
		self.speed = 8
		self.direction = pygame.math.Vector2()
		self.attacking = False
		self.attack_cd = 400
		self.attack_time = None

		# weapon
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]
		self.can_switch_weapon = False
		self.switch_duration_cd = 400
		self.weapon_switch_time = 0

		# obstacles
		self.obstacle_sprites = obstacle_sprites

	def import_player_assets(self):
		character_path = '../graphics/player/'
		self.animations = {
			'up': [], 'up_idle': [], 'up_attack': [],
			'down': [], 'down_idle': [], 'down_attack': [],
			'left': [], 'left_idle': [], 'left_attack': [],
			'right': [], 'right_idle': [], 'right_attack': [],
		}

		for animation in self.animations:
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def get_input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			# movement input
			if keys[pygame.K_RIGHT]:
				self.direction.x = 1			
				self.status = 'right'			
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'	
			else:
				self.direction.x = 0
			
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0	

			# attack input
			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()			
				self.create_attack()
			
			if keys[pygame.K_LCTRL]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()			
			
			if keys[pygame.K_q] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()
				if self.weapon_index < len(list(weapon_data.keys())) - 1:
					self.weapon_index += 1
				else:
					self.weapon_index = 0
				self.weapon = list(weapon_data.keys())[self.weapon_index]

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

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if self.attacking:		
			if current_time - self.attack_time >= self.attack_cd:
				self.attacking = False		
				self.destroy_attack()
		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= self.switch_duration_cd:
				self.can_switch_weapon = True				

	def get_status(self):
		# idle
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'
		
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','_idle')

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)		

	def update(self):
		self.get_input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)		