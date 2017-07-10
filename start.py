""" This is the starting module of the game. It contains the playgame function. """

import os
import gc

import pygame
from pygame import font

import MENU
import GENERAL as GEN

gc.enable()
      
def playgame():
    """ Changes working directory, creates pygame display, creates an object of the MenuScene class. """
    os.chdir(".\\InitGame")
    pygame.init()
    pygame.font.init()
    metrics = GEN.screen_metrics()
    screen = pygame.display.set_mode((metrics[0], metrics[1]), pygame.FULLSCREEN)
    active_scene = MENU.MenuScene(screen)

playgame()
