import pygame, os, gc, ctypes
from pygame import font
import MENU
gc.enable()

                
def playgame():
    os.chdir(".\\InitGame")
    pygame.init()
    pygame.font.init()
    ctypes.windll.user32.SetProcessDPIAware()
    user32 = ctypes.windll.user32
    w = int(user32.GetSystemMetrics(0))
    h = int(user32.GetSystemMetrics(1))
    screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
    pygame.display.set_caption("Empire Builder 0.2")
    active_scene = MENU.MenuScene(screen)

playgame()
