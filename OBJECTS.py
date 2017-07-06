import pygame, sys, os, random, datetime, math, gc
from pygame import font
import ctypes
import GUI

class Area():
    def __init__(self, arealist):
        screen = arealist[0]
        self.name = arealist[1]
        self.location = arealist[2]
        self.population = arealist[3] * 1000000
        self.resources = arealist[4]
        self.country = arealist[5]
        self.moral = arealist[6]
        self.neighbors = arealist[7]
        self.income_capita = arealist[9]
        self.tax = arealist[10]
        self.buildings = arealist[11]
        
        if type(self.neighbors) == list: self.sea = True
        if type(self.neighbors) == int: self.sea = False
        self.index = arealist[8]

        self.area_point = pygame.image.load(self.country+".png")
        
        self.button = pygame.Rect(self.location[0], self.location[1], 20, 20)
        self.myfont = pygame.font.SysFont("times", 30)
        self.medfont = pygame.font.SysFont("times", 22)
        self.mysmallfont = pygame.font.SysFont("times", 18)
        

        size = 225
        if len(self.name) > 11:
            size = int(17.5*len(self.name))

        infoObject = pygame.display.Info()
        w = int(infoObject.current_w/1)
        h = int(infoObject.current_h/1)
        self.ratio = 285/size
        rect = [self.location[0] + 20, self.location[1] + 20, size, int(size*self.ratio)]
        self.rect = rect

        if rect[0] + rect[2] > w - 100: rect[0] = self.location[0] - 20 - size
        if rect[1] + rect[3] > h - 100: rect[1] = self.location[1] - 20 - int(size*self.ratio)
        
        if self.buildings[0]: capital = "***"
        else: capital = ""
        if self.country == "c": player = "Computer"
        if self.country[0] == "p": player = "Player "+self.country[1]
        if self.country == "o": player = "Unclaimed waters"
        
        self.LabelList = [GUI.Label(self.name+capital, self.myfont, (rect[0] + 10, rect[1] + 5)), GUI.Label(player, self.medfont, (rect[0] + 10, rect[1] + 38)),
                          GUI.Label("Population: "+str(self.population/1000000)[:5]+" million", self.mysmallfont, (rect[0] + 10, rect[1] + 74)),
                          GUI.Label("Moral: "+str(int(self.moral))+"%", self.mysmallfont, (rect[0] + 10, rect[1] + 96)),
                          GUI.Label("Food: "+str(int(self.resources[5][0])), self.mysmallfont, (rect[0] + 10, rect[1] + 118)),
                          GUI.Label("Metal: "+str(int(self.resources[0][0])), self.mysmallfont, (rect[0] + 10, rect[1] + 140)),
                          GUI.Label("Timber: "+str(int(self.resources[1][0])), self.mysmallfont, (rect[0] + 10, rect[1] + 162)),
                          GUI.Label("Fossil fuels: "+str(int(self.resources[2][0])), self.mysmallfont, (rect[0] + 10, rect[1] + 184)),
                          GUI.Label("Uranium: "+str(int(self.resources[3][0])), self.mysmallfont, (rect[0] + 10, rect[1] + 206)),
                          GUI.Label("Renewables: "+(self.resources[4][0]+1)*"#", self.mysmallfont, (rect[0] + 10, rect[1] + 228)),
                          GUI.Label("Income: "+str(int(self.income_capita)), self.mysmallfont, (rect[0] + 10, rect[1] + 250))]

    def draw_area(self, screen):
        screen.blit(self.area_point, self.location)
        
    def hover_display(self, screen, rect):
        screen.fill([50, 50, 50, 50], tuple(rect))
        pygame.draw.rect(screen, [0, 0, 0, 0], tuple(rect), 3)

        for label in self.LabelList:
            label.DrawLabel(screen)

class Troop():
    def __init__(self, trooplist, loc):
        screen = trooplist[0]
        self.index = trooplist[1]
        self.name = trooplist[2]
        self.player = trooplist[3]
        self.area = trooplist[4]
        self.units = trooplist[5]
        self.moral = trooplist[6]
        self.location = [loc[0], loc[1] + 20]
        self.troop_point = pygame.image.load(self.player+"troop.png")
        
        self.button = pygame.Rect(self.location[0], self.location[1], 20, 20)
        self.fi = 31/50
        self.myfont = pygame.font.SysFont("times", 28)
        self.mysmallfont = pygame.font.SysFont("times", 18)
        self.click = False

    def draw_troop(self, screen):
        screen.blit(self.troop_point, self.location)

    def hover_display(self, screen):
        size = 200
        if len(self.name) == 4: size = 215
        if len(self.name) == 5: size = 230
        infoObject = pygame.display.Info()
        w = int(infoObject.current_w/1)
        h = int(infoObject.current_h/1)

        rect = [self.location[0] + 20, self.location[1] + 20, size, 280]

        if rect[0] + rect[2] > w - 100: rect[0] = self.location[0] - 20 - size
        if rect[1] + rect[3] > h - 100: rect[1] = self.location[1] - 20 - 280
        if rect[3] < 200: rect[3] = 200
        
        screen.fill([50, 50, 50, 50], tuple(rect))
        pygame.draw.rect(screen, [0, 0, 0, 0], tuple(rect), 3)
        label = self.myfont.render("Battalion: "+self.name, 1, (255,255,255))
        screen.blit(label, (rect[0] + 20, rect[1] + 20))
        infantry = "Infantry: "+str(self.units[0])
        artillery = "Artillery: "+str(self.units[1])
        tanks = "Tanks: "+str(self.units[2])
        ships = "Ships: "+str(self.units[3])
        submarines = "Submarines: "+str(self.units[4])
        carriers = "Aircraft Carriers: "+str(self.units[5])
        bombers = "Bombers: "+str(self.units[6])
        cruisers = "Cruisers: "+str(self.units[7])
        moral = "Moral: "+str(self.moral)+"%"
        label2 = self.mysmallfont.render(infantry, 1, (255,255,255))
        label3 = self.mysmallfont.render(artillery, 1, (255,255,255))
        label4 = self.mysmallfont.render(tanks, 1, (255,255,255))
        label5 = self.mysmallfont.render(ships, 1, (255,255,255))
        label6 = self.mysmallfont.render(submarines, 1, (255,255,255))
        label7 = self.mysmallfont.render(carriers, 1, (255,255,255))
        label8 = self.mysmallfont.render(bombers, 1, (255,255,255))
        label9 = self.mysmallfont.render(cruisers, 1, (255,255,255))
        label10 = self.mysmallfont.render(moral, 1, (255, 255, 255))
        screen.blit(label2, (rect[0] + 10, rect[1] + 65))
        screen.blit(label3, (rect[0] + 10, rect[1] + 85))
        screen.blit(label4, (rect[0] + 10, rect[1] + 105))
        screen.blit(label5, (rect[0] + 10, rect[1] + 125))
        screen.blit(label6, (rect[0] + 10, rect[1] + 145))
        screen.blit(label7, (rect[0] + 10, rect[1] + 165))
        screen.blit(label8, (rect[0] + 10, rect[1] + 185))
        screen.blit(label9, (rect[0] + 10, rect[1] + 205))
        screen.blit(label10, (rect[0] + 10, rect[1] + 230))
          
class Troop_Display():
    pass       

class Player():
    def __init__(self, playerlist, pause):
        screen = playerlist[0]
        self.index = playerlist[1]
        self.name = playerlist[2]
        self.areas = playerlist[3]
        self.resources = playerlist[4]
        self.coins = playerlist[5]
        self.population = playerlist[6]
        self.troops = playerlist[7]
        self.total_energy = self.resources[2] + self.resources[3]*20 + self.resources[4]*3

        rect = [0, 500, 260, 500]
        screen.fill([50, 50, 50, 50], tuple(rect))
        pygame.draw.rect(screen, [255, 255, 255, 255], tuple(rect), 3)
        if self.name[0] == "p": self.full_name = "Player "+self.name[1]
        if self.name[0] == "c": self.full_name = "Computer"
        self.myfont = pygame.font.SysFont("times", 30)
        self.mysmallfont = pygame.font.SysFont("times", 18)
        label = self.myfont.render(self.full_name, 1, (255, 255, 255))
        screen.blit(label, (rect[0] + 15, rect[1] + 15))
        self.area_point = pygame.image.load(self.name+".png")
        screen.blit(self.area_point, [220, 515])
        label2 = self.mysmallfont.render("Coins: "+str(int(self.coins/1000000)/1000)+" billion", 1, (255, 255, 255))
        label3 = self.mysmallfont.render("Population: "+str(self.population)[:7]+" million", 1, (255, 255, 255))
        label4 = self.mysmallfont.render("Metal: "+str(self.resources[0]), 1, (255, 255, 255))
        label5 = self.mysmallfont.render("Timber: "+str(self.resources[1]), 1, (255, 255, 255))
        label6 = self.mysmallfont.render("Fossil Fuels: "+str(self.resources[2]), 1, (255, 255, 255))
        label7 = self.mysmallfont.render("Uranium: "+str(self.resources[3]), 1, (255, 255, 255))
        label8 = self.mysmallfont.render("Renewables: "+str(self.resources[4]), 1, (255, 255, 255))
        label9 = self.mysmallfont.render("Food: "+str(self.resources[5])[:8], 1, (255, 255, 255))
        label10 = self.mysmallfont.render("Total Energy: "+str(self.total_energy), 1, (255, 255, 255))
        screen.blit(label2, (rect[0] + 15, rect[1] + 60))
        screen.blit(label3, (rect[0] + 15, rect[1] + 80))
        screen.blit(label4, (rect[0] + 15, rect[1] + 100))
        screen.blit(label5, (rect[0] + 15, rect[1] + 120))
        screen.blit(label6, (rect[0] + 15, rect[1] + 140))
        screen.blit(label7, (rect[0] + 15, rect[1] + 160))
        screen.blit(label8, (rect[0] + 15, rect[1] + 180))
        screen.blit(label9, (rect[0] + 15, rect[1] + 200))
        screen.blit(label10, (rect[0] + 15, rect[1] + 220))
       
        pygame.draw.rect(screen, [255, 255, 255, 255], (50, 770, 180, 80), 3)
        self.button1 = pygame.Rect(50, 770, 180, 80)
        label11 = self.myfont.render("Next Player", 1, (255, 255, 255))
        screen.blit(label11, (70, 790))

        pygame.draw.rect(screen, [255, 255, 255, 255], (50, 880, 180, 80), 3)
        self.button2 = pygame.Rect(50, 880, 180, 80)
        label12 = self.myfont.render("Save & quit", 1, (255, 255, 255))
        screen.blit(label12, (66, 902))

        pygame.draw.rect(screen, [255, 255, 255, 255], (1490, 10, 150, 50), 3)
        self.button3 = pygame.Rect(1490,  10, 150, 50)
        screen.fill([50, 50, 50], (1490, 10, 150, 50))

        if pause: label13 = self.myfont.render("Play", 1, (255, 255, 255))
        if not pause: label13 = self.myfont.render("Pause", 1, (255, 255, 255))
        screen.blit(label13, (1529, 17))
