import pygame, os, gc
from pygame import font
import MENU
import GENERAL as GEN

gc.enable()
      
def playgame():
    os.chdir(".\\InitGame")
    pygame.init()
    pygame.font.init()
    metrics = GEN.screen_metrics()
    screen = pygame.display.set_mode((metrics[0], metrics[1]), pygame.FULLSCREEN)
    active_scene = MENU.MenuScene(screen)

playgame()
