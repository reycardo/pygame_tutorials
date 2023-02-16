import pygame
from support import import_folder
from settings import *

class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf: pygame.surface.Surface, groups, z = LAYERS['main']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z

class Water(Generic):
	def __init__(self, pos, frames, groups):

		# animation setup
		self.frames = frames
		self.frame_index = 0

		#sprite setup
		super().__init__(
			pos = pos, 
			surf = self.frames[self.frame_index], 
			groups = groups, 
			z = LAYERS['water']
		)

	def import_assets(self):		
		self.animations = {
			 'up': [], 'down': [], 'left': [], 'right': [],
			 'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
			 'up_hoe': [], 'down_hoe': [], 'left_hoe': [], 'right_hoe': [],
			 'up_axe': [], 'down_axe': [], 'left_axe': [], 'right_axe': [],
			 'up_water': [], 'down_water': [], 'left_water': [], 'right_water': []
		}

		for animation in self.animations:
			full_path = '../graphics/character/' + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self, dt):
		self.frame_index += 5 *dt
		if self.frame_index >= len(self.frames):
			self.frame_index = 0

		self.image = self.frames[int(self.frame_index)]

	def update(self, dt):
		self.animate(dt)
		
class WildFlower(Generic):
	def __init__(self, pos, surf, groups):
		super().__init__(pos = pos, surf = surf, groups = groups)	

class Tree(Generic):
	def __init__(self, pos, surf, groups, name):
		super().__init__(
			pos = pos, 
			surf = surf, 
			groups = groups			
		)	