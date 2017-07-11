import pygame
from pygame import font

import GUI
import GENERAL as GEN

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
        metrics = GEN.screen_metrics()
        self.w = metrics[0]
        self.h = metrics[1]
        self.ratiow = metrics[2]
        self.ratioh = metrics[3]
        if type(self.neighbors) == list: self.sea = True
        if type(self.neighbors) == int: self.sea = False
        self.index = arealist[8]

        self.area_point = pygame.image.load(self.country+".png")
        
        self.button = pygame.Rect(self.location[0], self.location[1], 20, 20)
        self.myfont = pygame.font.SysFont("times", int(30*self.ratiow))
        self.medfont = pygame.font.SysFont("times", int(22*self.ratiow))
        self.mysmallfont = pygame.font.SysFont("times", int(18*self.ratiow))
        

        size = int(225*self.ratiow)
        if len(self.name) > 11:
            size = int(17.5*len(self.name)*self.ratiow)

        w = self.w
        h = self.h
        self.ratio = 285/size*self.ratioh
        rect = [self.location[0] + 20, self.location[1] + 20, size, int(size*self.ratio)]
        self.rect = rect

        if rect[0] + rect[2] > w - 100: rect[0] = self.location[0] - 20 - size
        if rect[1] + rect[3] > h - 100: rect[1] = self.location[1] - 20 - int(size*self.ratio)
        
        if self.buildings[0]: capital = "***"
        else: capital = ""
        if self.country == "c": player = "Computer"
        if self.country[0] == "p": player = "Player "+self.country[1]
        if self.country == "o": player = "Unclaimed waters"
        marg = int(10*self.ratiow)
        self.LabelList = [GUI.Label(self.name+capital, self.myfont, (rect[0] + marg,
                                                     rect[1] + int(5*self.ratioh))),
                                    GUI.Label(player, self.medfont, (rect[0] + marg, rect[1]
                                                                                          + int( 38*self.ratioh))),
                                    GUI.Label("Population: "+str(self.population/1000000)[:5]
                                                       + " million", self.mysmallfont,
                                                       (rect[0] + marg, rect[1] + int(74*self.ratioh))),
                                    GUI.Label("Moral: "+str(int(self.moral))+"%", self.mysmallfont,
                                                      (rect[0] + marg, rect[1] + int(96*self.ratioh))),
                                    GUI.Label("Food: "+str(int(self.resources[5][0])), self.mysmallfont,
                                                       (rect[0] + marg, rect[1] + int(118*self.ratioh))),
                                    GUI.Label("Metal: "+str(int(self.resources[0][0])), self.mysmallfont,
                                                      (rect[0] + marg, rect[1] + int(140*self.ratioh))),
                                    GUI.Label("Timber: "+str(int(self.resources[1][0])),
                                                      self.mysmallfont,
                                                      (rect[0] + marg, rect[1] + int(162*self.ratioh))),
                                    GUI.Label("Fossil fuels: "+str(int(self.resources[2][0])),
                                                       self.mysmallfont,
                                                       (rect[0] + marg, rect[1] + int(184*self.ratioh))),
                                    GUI.Label("Uranium: "+str(int(self.resources[3][0])),
                                                     self.mysmallfont,
                                                      (rect[0] + marg, rect[1] + int(206*self.ratioh))),
                                    GUI.Label("Renewables: "+(self.resources[4][0]+1)*"#",
                                                      self.mysmallfont,
                                                      (rect[0] + marg, rect[1] + int(228*self.ratioh))),
                                    GUI.Label("Income: "+str(int(self.income_capita)), self.mysmallfont,
                                                      (rect[0] + marg, rect[1] + int(250*self.ratioh)))]

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
        metrics = GEN.screen_metrics()
        self.w = metrics[0]
        self.h = metrics[1]
        self.ratiow = metrics[2]
        self.ratioh = metrics[3]
        self.button = pygame.Rect(self.location[0], self.location[1], 20, 20)
        self.fi = 31/50
        self.myfont = pygame.font.SysFont("times", int(28*self.ratiow))
        self.mysmallfont = pygame.font.SysFont("times", int(18*self.ratiow))
        self.click = False

    def draw_troop(self, screen):
        screen.blit(self.troop_point, self.location)

    def hover_display(self, screen):
        size = int(200*self.ratiow)
        if len(self.name) == 4: size = int(215*self.ratiow)
        if len(self.name) == 5: size = int(230*self.ratiow)
        
        w = self.w
        h = self.h
        marg = int(self.ratiow*20)
        rect = [self.location[0] + marg, self.location[1] + marg, size, int(280*self.ratioh)]

        if rect[0] + rect[2] > w - 100: rect[0] = self.location[0] - marg - size
        if rect[1] + rect[3] > h - 100: rect[1] = self.location[1] - marg - int(280*self.ratioh)
        if rect[3] < 200: rect[3] = 200
        
        screen.fill([50, 50, 50, 50], tuple(rect))
        pygame.draw.rect(screen, [0, 0, 0, 0], tuple(rect), 3)
        label = self.myfont.render("Battalion: "+self.name, 1, (255,255,255))
        screen.blit(label, (rect[0] + marg, rect[1] + marg))
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
        screen.blit(label2, (rect[0] + marg//2, rect[1] + int(65*self.ratioh)))
        screen.blit(label3, (rect[0] + marg//2, rect[1] + int(85*self.ratioh)))
        screen.blit(label4, (rect[0] + marg//2, rect[1] + int(105*self.ratioh)))
        screen.blit(label5, (rect[0] + marg//2, rect[1] + int(125*self.ratioh)))
        screen.blit(label6, (rect[0] + marg//2, rect[1] + int(145*self.ratioh)))
        screen.blit(label7, (rect[0] + marg//2, rect[1] + int(165*self.ratioh)))
        screen.blit(label8, (rect[0] + marg//2, rect[1] + int(185*self.ratioh)))
        screen.blit(label9, (rect[0] + marg//2, rect[1] + int(205*self.ratioh)))
        screen.blit(label10, (rect[0] + marg//2, rect[1] + int(230*self.ratioh)))
          
class TroopDisplay():
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
        metrics = GEN.screen_metrics()
        self.w = metrics[0]
        self.h = metrics[1]
        self.ratiow = metrics[2]
        self.ratioh = metrics[3]
        marg = int(15*self.ratiow)
        rect = [0, int(500*self.ratioh), int(260*self.ratiow), int(500*self.ratioh)]
        screen.fill([50, 50, 50, 50], tuple(rect))
        pygame.draw.rect(screen, [255, 255, 255, 255], tuple(rect), 3)
        if self.name[0] == "p": self.full_name = "Player "+self.name[1]
        if self.name[0] == "c": self.full_name = "Computer"
        self.myfont = pygame.font.SysFont("times", int(30*self.ratiow))
        self.mysmallfont = pygame.font.SysFont("times", int(18*self.ratiow))
        label = self.myfont.render(self.full_name, 1, (255, 255, 255))
        screen.blit(label, (rect[0] + marg, rect[1] + marg))
        self.area_point = pygame.image.load(self.name+".png")
        screen.blit(self.area_point, [int(220*self.ratiow), int(515*self.ratioh)])
        label2 = self.mysmallfont.render("Coins: "+str(int(self.coins/1000000)/1000)
                                                                                      +" billion", 1, (255, 255, 255))
        label3 = self.mysmallfont.render("Population: "+str(self.population)[:7]+
                                                               " million", 1, (255, 255, 255))
        label4 = self.mysmallfont.render("Metal: "+str(self.resources[0]), 1, (255, 255, 255))
        label5 = self.mysmallfont.render("Timber: "+str(self.resources[1]), 1, (255, 255, 255))
        label6 = self.mysmallfont.render("Fossil Fuels: "+str(self.resources[2]), 1,
                                                              (255, 255, 255))
        label7 = self.mysmallfont.render("Uranium: "+str(self.resources[3]), 1,
                                                              (255, 255, 255))
        label8 = self.mysmallfont.render("Renewables: "+str(self.resources[4]), 1,
                                                               (255, 255, 255))
        label9 = self.mysmallfont.render("Food: "+str(self.resources[5])[:8], 1,
                                                               (255, 255, 255))
        label10 = self.mysmallfont.render("Total Energy: "+str(self.total_energy), 1,
                                                                (255, 255, 255))
        
        screen.blit(label2, (rect[0] + marg, rect[1] + int(60*self.ratioh)))
        screen.blit(label3, (rect[0] + marg, rect[1] + int(80*self.ratioh)))
        screen.blit(label4, (rect[0] + marg, rect[1] + int(100*self.ratioh)))
        screen.blit(label5, (rect[0] + marg, rect[1] + int(120*self.ratioh)))
        screen.blit(label6, (rect[0] + marg, rect[1] + int(140*self.ratioh)))
        screen.blit(label7, (rect[0] + marg, rect[1] + int(160*self.ratioh)))
        screen.blit(label8, (rect[0] + marg, rect[1] + int(180*self.ratioh)))
        screen.blit(label9, (rect[0] + marg, rect[1] + int(200*self.ratioh)))
        screen.blit(label10, (rect[0] + marg, rect[1] + int(220*self.ratioh)))
       
        pygame.draw.rect(screen, [255, 255, 255, 255], (int(50*self.ratiow),
                                                                                         int(770*self.ratioh),
                                        int(180*self.ratiow), int(80*self.ratioh)), 3)
        self.button1 = pygame.Rect(int(50*self.ratiow), int(770*self.ratioh),
                                                       int(180*self.ratiow), int(80*self.ratioh))
        label11 = self.myfont.render("Next Player", 1, (255, 255, 255))
        screen.blit(label11, (int(70*self.ratiow), int(790*self.ratioh)))

        pygame.draw.rect(screen, [255, 255, 255, 255], (int(50*self.ratiow),
                                      int(880*self.ratioh), int(180*self.ratiow), int(80*self.ratioh)), 3)
        self.button2 = pygame.Rect(int(50*self.ratiow), int(880*self.ratioh),
                                                       int(180*self.ratiow), int(80*self.ratioh))
        label12 = self.myfont.render("Save & quit", 1, (255, 255, 255))
        screen.blit(label12, (int(66*self.ratiow), int(902*self.ratioh)))

        pygame.draw.rect(screen, [255, 255, 255, 255], (int(1490*self.ratiow),
                                      int(10*self.ratioh), int(150*self.ratiow), int(50*self.ratioh)), 3)
        self.button3 = pygame.Rect(int(1490*self.ratiow), int(10*self.ratioh),
                                                       int(150*self.ratiow), int(50*self.ratioh))
        screen.fill([50, 50, 50], (int(1490*self.ratiow), int(10*self.ratioh),
                                                 int(150*self.ratiow), int(50*self.ratioh)))

        if pause: label13 = self.myfont.render("Play", 1, (255, 255, 255))
        if not pause: label13 = self.myfont.render("Pause", 1, (255, 255, 255))
        screen.blit(label13, (int(1529*self.ratiow), int(17*self.ratioh)))
