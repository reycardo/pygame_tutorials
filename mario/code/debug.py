import pygame

pygame.init()
font = pygame.font.Font('../graphics/ui/ARCADEPI.ttf',25)

def debug(info,x=10,y=10):
    display_surface = pygame.display.get_surface()
    
    # create some text
    debug_surface = font.render(str(info),False,"White")
    # create a rect with a pos
    debug_rect = debug_surface.get_rect(topleft = (x,y))
    # bg
    pygame.draw.rect(display_surface,'Black',debug_rect)
    # blit all that
    display_surface.blit(debug_surface,debug_rect)