import pygame
from settings import *
from player import Player

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        # conver weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():            
            weapon = pygame.image.load(weapon["graphic"]).convert_alpha()
            self.weapon_graphics.append(weapon)
        
        # conver magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():            
            magic = pygame.image.load(magic["graphic"]).convert_alpha()
            self.magic_graphics.append(magic)            

    def show_bar(self, current: int, max_amount: int, bg_rect: pygame.Rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # draw current
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
    
    def show_exp(self, exp):
        text_surface = self.font.render(str(int(exp)),False,TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surface.get_rect(bottomright = (x,y))
        
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,15))
        self.display_surface.blit(text_surface,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,15),3)

    def selection_box(self,left,top, has_switched):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if not has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched):
        bg_rect = self.selection_box(20, self.display_surface.get_size()[1] - (20+ITEM_BOX_SIZE),has_switched) # weapon        
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surf,weapon_rect)

    def magic_overlay(self,magic_index,has_switched):
        bg_rect = self.selection_box(18 + ITEM_BOX_SIZE, self.display_surface.get_size()[1] - (15+ITEM_BOX_SIZE), has_switched) # magic
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(magic_surf,magic_rect)

    def display(self, player: Player):
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)
        self.weapon_overlay(player.weapon_index,player.can_switch_weapon)
        self.magic_overlay(player.magic_index,player.can_switch_magic)        
        self.show_exp(player.exp)
        