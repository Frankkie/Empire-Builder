""" This module contains the necessary GUI elements of the
      game. """

import pygame
from pygame import font

import GENERAL as GEN

class Bar():
    """ Class for a sliding bar, allowing the user to select
          integer values in a particular scale, to alter the
          value of the corresponding variable.
          The elements composing the sliding bar are the bar itself,
          and a moving point that shows the value that the variable
          associated with the bar has in a given instant."""
    def __init__(self, screen, pos, text, textpos, limits, num):
        """ (screen, pos, tetxt, textpos, limits, num)
              The init function of the class Bar initializes certain
               variables. """
        
        self.screen = screen
        self.pos = pos
        self.text = text
        self.textpos = textpos
        self.range = limits[1] - limits[0]
        # num is the value of the variable associated with
        # the Bar.
        self.prop = num/self.range

        metrics = GEN.screen_metrics()
        self.w = metrics[0]
        self.h = metrics[1]
        self.ratiow = metrics[2]
        self.ratioh = metrics[3]

        self.barsize = int(400*self.ratiow)
        self.color = (255, 255, 255)
        self.pointrect = pygame.Rect(((pos[0] - int(10*self.ratiow)) + int(self.barsize*self.prop),
                                                            pos[1] - int(15*self.ratioh), 40, 40))
        self.medfont = pygame.font.SysFont("Times", int(25*self.ratiow))
        # The drag parameter determines whether the point
        # of the Bar will be following the mouse cursor.
        self.drag = False
        

    def Draw_Bar(self, num, barimage, pointimage):
        """ (num, barimage, pointimage)
             This method draws a Bar object on the screen. """
        self.prop = num/self.range
        self.screen.blit(barimage, [self.pos[0], self.pos[1]])
        self.screen.blit(pointimage, [(self.pos[0] - int(10*self.ratiow))
                                                       + int(self.prop*self.barsize),
                                                        self.pos[1] - int(15*self.ratioh)])
        self.label = self.medfont.render(self.text+": "+str(num)+"%", 1, self.color)
        self.screen.blit(self.label, self.textpos)

        
    def Drag(self, mouse_pos):
        """ (mouse_pos), returns num
              This method is called when the self.drag method is
              called, and it manages the change in position of
              the point of the Bar and the corresponding change in
              the variable's num value. """
        point_pos = mouse_pos[0]
        if mouse_pos[0] < self.pos[0]: point_pos = self.pos[0]
        if mouse_pos[0] > self.pos[0] + self.barsize : point_pos = self.pos[0] + self.barsize
        num = int((point_pos - self.pos[0])/(self.barsize/self.range))
        self.pointrect = pygame.Rect((point_pos, self.pos[1] - 15, 40, 40))
        return num

######################################################################


class Label():
    """ This is the class for a text label. """
    def __init__(self, text, font, pos, color=(255, 255, 255)):
        """ (text, font, pos, color=(255, 255, 255))
              Initializes variables. """
        self.pos = pos
        self.label = font.render(text, 1, color)

        
    def DrawLabel(self, screen):
        """ (screen)
              This method draws the Label class object. """
        screen.blit(self.label, self.pos)
