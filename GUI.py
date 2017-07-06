import pygame, sys, os, random, datetime, math, gc
from pygame import font
import ctypes

class Bar():
    def __init__(self, screen, pos, text, textpos, limits, num):
        self.screen = screen
        self.color = (255, 255, 255)
        self.pos = pos
        self.text = text
        self.textpos = textpos
        self.barsize = 400
        self.range = limits[1] - limits[0]
        self.prop = num/self.range
        
        self.pointrect = pygame.Rect(((pos[0] - 20) + int(self.barsize*self.prop), pos[1] - 15, 40, 40))
        self.medfont = pygame.font.SysFont("Times", 25)
        self.drag = False
        

    def Draw_Bar(self, num, barimage, pointimage):
        self.prop = num/(self.range)
        self.screen.blit(barimage, [self.pos[0], self.pos[1]])
        self.screen.blit(pointimage, [self.pos[0] - 20 + int(self.prop*self.barsize), self.pos[1] - 15])
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
