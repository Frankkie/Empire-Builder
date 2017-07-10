import pygame
from pygame import font

import GENERAL as GEN

class Bar():
    def __init__(self, screen, pos, text, textpos, limits, num):
        self.screen = screen
        self.color = (255, 255, 255)
        self.pos = pos
        self.text = text
        self.textpos = textpos
        metrics = GEN.screen_metrics()
        self.w = metrics[0]
        self.h = metrics[1]
        self.ratiow = metrics[2]
        self.ratioh = metrics[3]
        self.barsize = int(400*self.ratiow)
        self.range = limits[1] - limits[0]
        self.prop = num/self.range
        
        self.pointrect = pygame.Rect(((pos[0] - int(10*self.ratiow)) + int(self.barsize*self.prop), pos[1] - int(15*self.ratioh), 40, 40))
        self.medfont = pygame.font.SysFont("Times", int(25*self.ratiow))
        self.drag = False
        

    def Draw_Bar(self, num, barimage, pointimage):
        self.prop = num/(self.range)
        self.screen.blit(barimage, [self.pos[0], self.pos[1]])
        self.screen.blit(pointimage, [(self.pos[0] - int(10*self.ratiow))  + int(self.prop*self.barsize), self.pos[1] - int(15*self.ratioh)])
        self.label = self.medfont.render(self.text+": "+str(num)+"%", 1, self.color)
        self.screen.blit(self.label, self.textpos)
        
    def Drag(self, mouse_pos):
        point_pos = mouse_pos[0]
        if mouse_pos[0] < self.pos[0]: point_pos = self.pos[0]
        if mouse_pos[0] > self.pos[0] + self.barsize : point_pos = self.pos[0] + self.barsize
        num = int((point_pos - self.pos[0])/(self.barsize/self.range))
        self.pointrect = pygame.Rect((point_pos, self.pos[1] - 15, 40, 40))
        return num

class Label():
    def __init__(self, text, font, pos, color = (255, 255, 255)):
        self.pos = pos
        self.label = font.render(text, 1, color)
    def DrawLabel(self, screen):
        screen.blit(self.label, self.pos)
