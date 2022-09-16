from turtle import width
import pygame,sys,time
from settings import *
from sprites import Player, Ball, Block

class Game:
	def __init__(self):
		
		# general setup
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption(GAME_NAME)

		# bg
		self.bg = self.create_bg()		

		# sprite group setup
		self.all_sprites = pygame.sprite.Group()
		self.block_sprites = pygame.sprite.Group()
		
		# setup
		self.player = Player(self.all_sprites)
		self.stage_setup()
		self.ball = Ball(self.all_sprites, self.player, self.block_sprites)

	def create_bg(self):
		bg_original = pygame.image.load('../graphics/other/bg.png').convert()		
		scale_factor = WINDOW_HEIGHT / bg_original.get_height()
		scaled_w = bg_original.get_width() * scale_factor
		scaled_h = bg_original.get_height() * scale_factor
		scaled_bg = pygame.transform.scale(bg_original,(scaled_w,scaled_h))		
		return scaled_bg

	def stage_setup(self):
		# cycle block map
		for row_index, row in enumerate(BLOCK_MAP):
			for col_index, col in enumerate(row):
				if col != ' ':
					y = row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
					x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2						
					Block(col,(x,y),[self.all_sprites, self.block_sprites])

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
				
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.ball.active = True
						
			# update game
			self.all_sprites.update(dt)

			# draw the frame
			self.display_surface.blit(self.bg,(0,0))
			self.all_sprites.draw(self.display_surface)
			
			# update window
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
