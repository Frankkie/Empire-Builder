""" This module contains the MenuScene class, that is called at the beginning
      of the game. """

import ctypes
import sys
import os

import pygame
from pygame import font

import MAIN1 as MAIN
import GENERAL as GEN


class MenuScene():
    def __init__(self, screen):
        """ (screen)
              Initializes variables, loads images, creates fonts,
              buttons. """
        # Variable initialization.
        self.screen = screen
        self.black = (0, 0, 0)
        self.grey = (40, 40, 40)
        self.white = (255, 255, 255)

        # Getting screen metrics.
        metrics = GEN.screen_metrics()
        self.w = metrics[0]
        self.h = metrics[1]
        self.ratiow = metrics[2]
        self.ratioh = metrics[3]

        # Images loading.
        self.background1 = pygame.image.load("half1.png")
        self.background1 = pygame.transform.scale(self.background1, (int(self.w/2 - 300*self.ratiow),
                                                                                                   self.h))
        self.background2 = pygame.image.load("half2.png")
        self.background2 = pygame.transform.scale(self.background2, (int(self.w/2 - 300*self.ratiow),
                                                                                                   self.h))

        # Labels and fonts. ###################### Change the labels with Label class objects #####################
        self.largefont = pygame.font.SysFont("times", int(75*self.ratiow))
        self.medfont = pygame.font.SysFont("times", int(40*self.ratiow))
        self.smallfont = pygame.font.SysFont("times", int(20*self.ratiow))
        self.title = self.largefont.render("Empire Builder 0.3", 1, self.white)
        self.NumPlayers = 1
        self.labelselect = self.medfont.render("Select number of players:  ", 1, self.white)


        # Buttons.
        self.button = pygame.Rect((int(self.w/2 + 200*self.ratiow), int(305*self.ratioh),
                                                     int(50*self.ratiow), int(40*self.ratioh)))
        self.startbutton = pygame.Rect((int(self.w/2 - 150*self.ratiow), int(440*self.ratioh),
                                                             int(300*self.ratiow), int(100*self.ratioh)))
        self.loadbutton = pygame.Rect((int(self.w/2 - 150*self.ratiow), int(640*self.ratioh),
                                                             int(300*self.ratiow), int(100*self.ratioh)))
        
        self.Draw(screen)
                
        
    def Draw(self, screen):
        """ (screen)
              Draws the Menu, handles events. """
        while 1:
            # Blitting images on screen.
            screen.fill(self.grey)
            screen.blit(self.background1, [0,0])
            screen.blit(self.background2, [int(self.w/2 + 300*self.ratiow),0])

            # Blitting labels on screen.
            screen.blit(self.title, (int(self.w/2 - 285*self.ratiow), int(80*self.ratioh)))
            screen.blit(self.labelselect, (int(self.w/2 - 240*self.ratiow), int(300*self.ratioh)))
            self.labelnum = self.medfont.render(str(self.NumPlayers), 1, self.white)
            screen.blit(self.labelnum, (int(self.w/2 + 170*self.ratiow), int(300*self.ratioh)))

            # Drawing buttons.
            self.DrawButton((int(self.w/2 + 200*self.ratiow), int(305*self.ratioh),
                                          int(50*self.ratiow), int(40*self.ratioh)), "^",
                                         (int(self.w/2 + 215*self.ratiow), int(310*self.ratioh)))
            self.DrawButton((int(self.w/2 - 150*self.ratiow), int(440*self.ratioh),
                                          int(300*self.ratiow), int(100*self.ratioh)), "Start Game",
                                          (int(self.w/2 - 90*self.ratiow), int(465*self.ratioh)))
            self.DrawButton((int(self.w/2 - 150*self.ratiow), int(640*self.ratioh),
                                          int(300*self.ratiow), int(100*self.ratioh)), "Load Game",
                                         (int(self.w/2 - 90*self.ratiow), int(665*self.ratioh)))

            # Event handling.
            mouse_pos = pygame.mouse.get_pos()
            if self.button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, self.white, self.button, 1)
            if self.startbutton.collidepoint(mouse_pos):
                pygame.draw.rect(screen, self.white, self.startbutton, 1)
            if self.loadbutton.collidepoint(mouse_pos):
                pygame.draw.rect(screen, self.white, self.loadbutton, 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button.collidepoint(mouse_pos):
                        self.NumPlayers += 1
                        self.NumPlayers = self.NumPlayers%6
                        if self.NumPlayers == 0:
                            self.NumPlayers = 6
                    if self.startbutton.collidepoint(mouse_pos):
                        active_scene = MAIN.MainScene(screen, self.NumPlayers, "MenuScene",
                                                                                180.9, 0)
            pygame.display.flip()


    def DrawButton(self, rect, text, textloc):
        """ (rect, text, textloc)
              Draws a button on the screen in position determined by rect,
              text determined by text and the position of text determined by textloc. """
        label = self.medfont.render(text, 1, self.white)
        self.screen.fill(self.black, rect)
        self.screen.blit(label, textloc)
