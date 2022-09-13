from turtle import width
import pygame,sys,time
from settings import *

class Game:
	def __init__(self):
		
		# general setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption(GAME_NAME)

		# bg
		self.bg = self.create_bg()

	def create_bg(self):
		bg_original = pygame.image.load('../graphics/other/bg.png').convert()		
		scale_factor = WINDOW_HEIGHT / bg_original.get_height()
		scaled_w = bg_original.get_width() * scale_factor
		scaled_h = bg_original.get_height() * scale_factor
		scaled_bg = pygame.transform.scale(bg_original,(scaled_w,scaled_h))		
		return scaled_bg

	def run(self):
		last_time = time.time()
		while True:
			
			# delta time
			dt = time.time() - last_time
			last_time = time.time()

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()				

			# draw the frame
			self.display_surface.blit(self.bg,(0,0))
			
			# update window
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
