import pygame, sys, os, random, datetime, math, gc
from pygame import font
import ctypes
import GUI
import MAIN1 as MAIN

gc.enable()

class AreaScene():
    def __init__(self, screen, arealist, clock, numplayers, year, currentplayer, player):
        self.ReadInfo(screen)
        self.area = arealist
        self.time = pygame.time.Clock()
        self.Clock = clock
        self.NumPlayers = numplayers
        self.year = year
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.pause = False
        self.currentplayer = currentplayer
        self.player = player
        infoObject = pygame.display.Info()
        self.w = int(infoObject.current_w)
        self.h = int(infoObject.current_h)
        self.screen = screen
        self.hugefont = pygame.font.SysFont("Times", 80)
        self.verylargefont = pygame.font.SysFont("Times", 50)
        self.largefont = pygame.font.SysFont("Times", 40)
        self.medfont = pygame.font.SysFont("Times", 25)
        self.smallfont = pygame.font.SysFont("Times", 20)
        self.ButtonDict = {}
        self.BackToMain = pygame.Rect((1600, 20, 180, 50))
        self.BuildCapital = pygame.Rect((1660, 170, 180, 50))
        self.BuildFactory = pygame.Rect((1660, 255, 180, 50))
        self.BuildPort = pygame.Rect((1660, 315, 180, 50))
        self.BuildAirPort = pygame.Rect((1660, 375, 180, 50))
        self.BuildFort = pygame.Rect((1660, 455, 180, 50))
        self.BuildHospital = pygame.Rect((1660, 515, 180, 50))
        self.BuildUni = pygame.Rect((1660, 575, 180, 50))
        self.BuildBank = pygame.Rect((1660, 655, 180, 50))
        
        self.bar = pygame.image.load("bar.png")
        self.bar = pygame.transform.scale(self.bar, (400, 10))
        self.point = pygame.image.load("point.png")
        self.point = pygame.transform.scale(self.point, (40, 40))
        self.playerdot = pygame.image.load(self.area[5]+".png")
        self.playerdot = pygame.transform.scale(self.playerdot, (50, 50))
        self.barlist = []
        
        self.taxesbar = GUI.Bar(self.screen, [50, 200], "Taxes", [60, 220], [0, 100], self.area[10])
        self.barlist.append(self.taxesbar)
        self.foodbar = GUI.Bar(self.screen, [50, 280], "Food", [60, 300], [0, 200], self.area[4][5][2])
        self.barlist.append(self.foodbar)
        self.metalbar = GUI.Bar(self.screen, [50, 360], "Metal", [60, 380], [0, 100], self.area[4][0][2])
        self.barlist.append(self.metalbar)
        self.timberbar = GUI.Bar(self.screen, [50, 440], "Timber", [60, 460], [0, 100], self.area[4][1][2])
        self.barlist.append(self.timberbar)
        self.fossilbar = GUI.Bar(self.screen, [50, 520], "Fossils", [60, 540], [0, 100], self.area[4][2][2])
        self.barlist.append(self.fossilbar)
        self.uraniumbar = GUI.Bar(self.screen, [50, 600], "Uranium", [60, 620], [0, 100], self.area[4][3][2])
        self.barlist.append(self.uraniumbar)
        self.renewbar = GUI.Bar(self.screen, [50, 680], "Renewables", [60, 700], [0, 100], self.area[4][4][1])
        self.barlist.append(self.renewbar)

        if self.area[11][0] == 0: capital = "- Not Capital"
        else: capital = "- Capital"
        if self.area[11][7] == 0: bank = "- No bank"
        else: bank = "- Bank"

        self.labellist = [GUI.Label(self.area[1], self.hugefont, [int(self.w/2 - len(self.area[1])*19), 20]),
                          GUI.Label("- Moral: "+str(round(self.area[6]))+"%", self.largefont, [660, 175]),
                          GUI.Label("- Population: "+str(round(self.area[3], 3))+" million people", self.largefont, [660, 225]),
                          GUI.Label("- Per Capita Income: "+str(int(self.area[9]))+" coins", self.largefont, [660, 275]),
                          GUI.Label("- Resources", self.verylargefont, [660, 340]),
                          GUI.Label("- Food: "+str(int(self.area[4][5][0]))+"/"+str(self.area[4][5][1]), self.largefont, [660, 400]),
                          GUI.Label("- Metal: "+str(self.area[4][0][0])+"/"+str(self.area[4][0][1]), self.largefont, [660, 450]),
                          GUI.Label("- Timber: "+str(int(self.area[4][1][0]))+"/"+str(self.area[4][1][1]), self.largefont, [660, 500]),
                          GUI.Label("- Fossil Fuels: "+str(self.area[4][2][0])+"/"+str(self.area[4][2][1]), self.largefont, [660, 550]),
                          GUI.Label("- Uranium: "+str(self.area[4][3][0])+"/"+str(self.area[4][3][1]), self.largefont, [660, 600]),
                          GUI.Label("- Renewables: "+"| "+(self.area[4][4][0] + 1)*"+"+(6 - self.area[4][4][0])*" "+"|", self.largefont, [660, 650]),
                          GUI.Label(capital, self.largefont, [1360, 175]),
                          GUI.Label("- Factory: lvl. "+str(self.area[11][1]), self.largefont, (1360, 260)),
                          GUI.Label("- Port: lvl. "+str(self.area[11][2]), self.largefont, (1360, 320)),
                          GUI.Label("- Airport: lvl. "+str(self.area[11][3]), self.largefont, (1360, 380)),
                          GUI.Label("- Fort: lvl. "+str(self.area[11][4]), self.largefont, (1360, 460)),
                          GUI.Label("- Hospital: lvl. "+str(self.area[11][5]), self.largefont, (1360, 520)),
                          GUI.Label("- University: lvl. "+str(self.area[11][6]), self.largefont, (1360, 580)),
                          GUI.Label(bank, self.largefont, (1360, 660)),]
        
        self.Draw()
        
    def SwitchToScene(self, scene):
        active_scene = scenes[scene]

    def DrawButton(self, rect, text, textloc):
        self.ButtonDict.update({str(pygame.Rect(rect)):pygame.Rect(rect)})
        label = self.medfont.render(text, 1, self.white)
        self.screen.fill(self.black, rect)
        self.screen.blit(label, textloc)

    def Draw(self):
        while 1:
            self.screen.fill((50, 50, 50))
            self.screen.blit(self.playerdot, (int(self.w/2) + 19*len(self.area[1]) + 20, 50))
            dt = self.time.tick()
            self.Clock -= dt/1000
            if self.Clock < 0:
                active_scene = MAIN.MainScene(self.screen, self.NumPlayers, "AreaScene", self.Clock, self.year)
            clock_ = str(int(self.Clock/60))+":"+str(int(self.Clock%60))
            if self.Clock%60 < 10: clock_ = str(int(self.Clock/60))+":0"+str(int(self.Clock%60))            
            clock_label = self.largefont.render(clock_, 1, (255, 255, 255))
            self.screen.blit(clock_label, (1820, 20))
            
            self.DrawButton((1600, 20, 180, 50), "Back to Map >>", [1610, 30])
            self.DrawButton((1660, 170, 180, 50), "Upgrade", [1708, 179])
            self.DrawButton((1660, 255, 180, 50), "Upgrade", [1708, 264])
            self.DrawButton((1660, 375, 180, 50), "Upgrade", [1708, 384])
            self.DrawButton((1660, 455, 180, 50), "Upgrade", [1708, 464])
            self.DrawButton((1660, 515, 180, 50), "Upgrade", [1708, 524])
            self.DrawButton((1660, 575, 180, 50), "Upgrade", [1708, 584])
            self.DrawButton((1660, 655, 180, 50), "Upgrade", [1708, 664])
            self.DrawButton((1660, 315, 180, 50), "Upgrade", [1708, 324])
            
            self.foodbar.Draw_Bar(self.area[4][5][2], self.bar, self.point)
            self.taxesbar.Draw_Bar(self.area[10], self.bar, self.point)
            self.metalbar.Draw_Bar(self.area[4][0][2], self.bar, self.point)
            self.timberbar.Draw_Bar(self.area[4][1][2], self.bar, self.point)
            self.fossilbar.Draw_Bar(self.area[4][2][2], self.bar, self.point)
            self.uraniumbar.Draw_Bar(self.area[4][3][2], self.bar, self.point)
            self.renewbar.Draw_Bar(self.area[4][4][1], self.bar, self.point)
            
            for label in self.labellist:
                label.DrawLabel(self.screen)
            
            mouse_pos = pygame.mouse.get_pos()

            i = self.area[8]
            if self.taxesbar.drag == True:
                self.area[10] = self.taxesbar.Drag(mouse_pos)
                self.AreaList[self.area[8]][10] = self.area[10]
            if self.foodbar.drag == True:
                self.area[4][5][2] = self.foodbar.Drag(mouse_pos)
                self.AreaList[self.area[8]][4][5][2] = self.area[4][5][2]
            if self.metalbar.drag == True:
                self.area[4][0][2] = self.metalbar.Drag(mouse_pos)
                self.AreaList[self.area[8]][4][0][2] = self.area[4][0][2]
            if self.timberbar.drag == True:
                self.area[4][1][2] = self.timberbar.Drag(mouse_pos)
                self.AreaList[i][4][1][2] = self.area[4][1][2]
            if self.fossilbar.drag == True:
                self.area[4][2][2] = self.fossilbar.Drag(mouse_pos)
                self.AreaList[i][4][2][2] = self.area[4][2][2]
            if self.uraniumbar.drag == True:
                self.area[4][3][2] = self.uraniumbar.Drag(mouse_pos)
                self.AreaList[i][4][3][2] = self.area[4][3][2]
            if self.renewbar.drag == True:
                self.area[4][4][1] = self.renewbar.Drag(mouse_pos)
                self.AreaList[i][4][4][1] = self.area[4][4][1]
            for button in self.ButtonDict.keys():
                if self.ButtonDict[button].collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, self.white, self.ButtonDict[button], 1)

            if self.BuildCapital.collidepoint(mouse_pos) and self.currentplayer:
                self.CapitalHover()
            elif self.BuildFactory.collidepoint(mouse_pos) and self.currentplayer:
                self.BuildingHover("factory")
            elif self.BuildPort.collidepoint(mouse_pos) and self.currentplayer:
                self.BuildingHover("port")
            elif self.BuildAirPort.collidepoint(mouse_pos) and self.currentplayer:
                self.BuildingHover("airport")
            elif self.BuildFort.collidepoint(mouse_pos) and self.currentplayer:
                self.BuildingHover("fort")
            elif self.BuildHospital.collidepoint(mouse_pos) and self.currentplayer:
                self.BuildingHover("hospital")
            elif self.BuildUni.collidepoint(mouse_pos) and self.currentplayer:
                self.BuildingHover("university")
            elif self.BuildBank.collidepoint(mouse_pos) and self.currentplayer:
                self.BuildingHover("bank")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BackToMain.collidepoint(mouse_pos):
                        self.WriteInfo()
                        active_scene = MAIN.MainScene(self.screen, self.NumPlayers, "AreaScene", self.Clock, self.year)
                    if self.BuildCapital.collidepoint(mouse_pos):
                        self.CapitalUpgrade()
                    if self.BuildFactory.collidepoint(mouse_pos):
                        self.BuildingUpgrade("factory")
                    if self.BuildPort.collidepoint(mouse_pos):
                        self.BuildingUpgrade("port")
                    if self.BuildAirPort.collidepoint(mouse_pos):
                        self.BuildingUpgrade("airport")
                    if self.BuildFort.collidepoint(mouse_pos):
                        self.BuildingUpgrade("fort")
                    if self.BuildHospital.collidepoint(mouse_pos):
                        self.BuildingUpgrade("hospital")
                    if self.BuildUni.collidepoint(mouse_pos):
                        self.BuildingUpgrade("university")
                    if self.BuildBank.collidepoint(mouse_pos):
                        self.BuildingUpgrade("bank")
                    
                    for bar in self.barlist:
                        if bar.pointrect.collidepoint(mouse_pos) and self.currentplayer:
                            temp = bar.drag
                            if temp == True: bar.drag = False
                            if temp == False: bar.drag = True
            pygame.display.flip()

    def CapitalHover(self):
        rect = [self.BuildCapital[0], self.BuildCapital[1] + self.BuildCapital[3] + 20, self.BuildCapital[2] + 60, 200]
        self.screen.fill([50, 50, 50, 50], tuple(rect))
        pygame.draw.rect(self.screen, [0, 0, 0, 0], tuple(rect), 3)
        if self.area[11][0] == 1:
            caplabel = GUI.Label("Cannot upgrade", self.medfont, [rect[0] + 20, rect[1] + 20])
            costlabel = [GUI.Label("", self.smallfont, [rect[0] + 20, rect[1] + 50])]
            self.capital_check = -1
        else:
            self.capital_check = 0
            for everyarea in self.AreaList:
                if self.area[5] == everyarea[5]:
                    if everyarea[11][0] == 1: self.capital_check = 1
            if self.capital_check == 1:
                caplabel = GUI.Label("Build new capital", self.medfont, [rect[0] + 20, rect[1] + 20])
                costlabel = []
                if self.PlayerList[self.player][4][0] < 1000:
                    costlabel.append(GUI.Label("- Metal: "+str(self.PlayerList[self.player][4][0])+"/1000", self.smallfont, [rect[0] + 20, rect[1] + 60], color = (255, 0, 0)))
                else:
                    costlabel.append(GUI.Label("- Metal: "+str(self.PlayerList[self.player][4][0])+"/1000", self.smallfont, [rect[0] + 20, rect[1] + 60], color = (255, 255, 255)))
                if self.PlayerList[self.player][4][1] < 3000:
                    costlabel.append(GUI.Label("- Timber: "+str(self.PlayerList[self.player][4][1])+"/3000", self.smallfont, [rect[0] + 20, rect[1] + 90], color = (255, 0, 0)))
                else:
                    costlabel.append(GUI.Label("- Timber: "+str(self.PlayerList[self.player][4][1])+"/3000", self.smallfont, [rect[0] + 20, rect[1] + 90], color = (255, 255, 255)))
                    
                if self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20 + self.PlayerList[self.player][4][4]*3 < 1000:
                    costlabel.append(GUI.Label("- Energy: "+str(self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20 + self.PlayerList[self.player][4][4]*3 )+"/1000",
                                           self.smallfont, [rect[0] + 20, rect[1] + 120], color = (255, 0, 0)))
                else:
                    costlabel.append(GUI.Label("- Energy: "+str(self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20 + self.PlayerList[self.player][4][4]*3 )+"/1000",
                                           self.smallfont, [rect[0] + 20, rect[1] + 120], color = (255, 255, 255)))
                if self.PlayerList[self.player][5] < 10**11:
                    costlabel.append(GUI.Label("- Coins: "+str(self.PlayerList[self.player][5]//10**9)+"/100 billion", self.smallfont, [rect[0] + 20, rect[1] + 150], color = (255, 0, 0)))
                else:
                    costlabel.append(GUI.Label("- Coins: "+str(self.PlayerList[self.player][5]//10**9)+"/100 billion", self.smallfont, [rect[0] + 20, rect[1] + 150]))
            else:
                caplabel = GUI.Label("Found your capital", self.medfont, [rect[0] + 20, rect[1] + 20])
                costlabel = [GUI.Label("Free", self.smallfont, [rect[0] + 20, rect[1] + 90])]

        caplabel.DrawLabel(self.screen)
        for label in costlabel:
            label.DrawLabel(self.screen)

    def CapitalUpgrade(self):
        if self.capital_check == -1:
            return
        elif self.capital_check == 0:
            self.area[11][0] = 1
            self.AreaList[self.area[8]][11][0] = 1
            self.labellist[11] = GUI.Label("- Capital", self.largefont, [1360, 175])
            self.capital_check = -1
            return
        else:
            if self.PlayerList[self.player][4][0] >= 2000 and self.PlayerList[self.player][4][1] >= 3000 and self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20 + self.PlayerList[self.player][4][4]*3 >= 1000 and self.PlayerList[self.player][5] >= 10**11:
                self.PlayerList[self.player][4][0] -= 2000
                self.PlayerList[self.player][4][1] -= 3000
                energy = 0
                while energy < 1000:
                    if self.PlayerList[self.player][4][2] > 0:
                        self.PlayerList[self.player][4][2] -= 1
                        energy += 1
                    if self.PlayerList[self.player][4][3] > 0:
                        self.PlayerList[self.player][4][3] -= 1
                        energy += 20
                    if self.PlayerList[self.player][4][4] > 0:
                        self.PlayerList[self.player][4][4] -= 1
                        energy += 3
                for area in self.PlayerList[self.player][3]:
                    if self.AreaList[area][11][0] == 1: self.AreaList[area][11][0] = 0
                self.area[11][0] = 1
                self.AreaList[self.area[8]][11][0] = 1
                self.capital_check = -1
                

    def BuildingHover(self, building):
        if building == "factory":
            rect = [self.BuildFactory[0], self.BuildFactory[1] + self.BuildFactory[3] + 20, self.BuildFactory[2] + 60, 200]
            highestlevel = 4
            metal = 300
            timber = 700
            energy = 500
            coins = 80
            index = 1
            
        elif building == "port":
            rect = [self.BuildPort[0], self.BuildPort[1] + self.BuildPort[3] + 20, self.BuildPort[2] + 60, 200]
            if type(self.area[7][-1]) != list:
                caplabel = GUI.Label("Cannot build port", self.medfont, [rect[0] + 20, rect[1] + 20])
                self.screen.fill([50, 50, 50, 50], tuple(rect))
                pygame.draw.rect(self.screen, [0, 0, 0, 0], tuple(rect), 3)
                caplabel.DrawLabel(self.screen)
                return
            highestlevel = 3
            metal = 400
            timber = 1200
            energy = 600
            coins = 140
            index = 2

        elif building == "airport":
            rect = [self.BuildAirPort[0], self.BuildAirPort[1] + self.BuildAirPort[3] + 20, self.BuildAirPort[2] + 60, 200]
            highestlevel = 2
            metal = 400
            timber = 1500
            energy = 750
            coins = 200
            index = 3

        elif building == "fort":
            rect = [self.BuildFort[0], self.BuildFort[1] + self.BuildFort[3] + 20, self.BuildFort[2] + 60, 200]
            highestlevel = 5
            metal = 200
            timber = 600
            energy = 300
            coins = 100
            index = 4

        elif building == "hospital":
            rect = [self.BuildHospital[0], self.BuildHospital[1] + self.BuildHospital[3] + 20, self.BuildHospital[2] + 60, 200]
            highestlevel = 3
            metal = 200
            timber = 700
            energy = 300
            coins = 200
            index = 5

        elif building == "university":
            rect = [self.BuildUni[0], self.BuildUni[1] + self.BuildUni[3] + 20, self.BuildUni[2] + 60, 200]
            highestlevel = 4
            metal = 200
            timber = 700
            energy = 300
            coins = 200
            index = 6

        elif building == "bank":
            rect = [self.BuildBank[0], self.BuildBank[1] + self.BuildBank[3] + 20, self.BuildBank[2] + 60, 200]
            highestlevel = 1
            metal = 100
            timber = 500
            energy = 500
            coins = 500
            index = 7
            
        self.screen.fill([50, 50, 50, 50], tuple(rect))
        pygame.draw.rect(self.screen, [0, 0, 0, 0], tuple(rect), 3)
        if self.area[11][index] == highestlevel:
            caplabel = GUI.Label("Cannot upgrade", self.medfont, [rect[0] + 20, rect[1] + 20])
            costlabel = [GUI.Label("", self.smallfont, [rect[0] + 20, rect[1] + 50])]
        else:
            caplabel = GUI.Label("Upgrade "+building, self.medfont, [rect[0] + 20, rect[1] + 20])
            costlabel = []
            if self.PlayerList[self.player][4][0] < metal:
                costlabel.append(GUI.Label("- Metal: "+str(self.PlayerList[self.player][4][0])+"/"+str(metal), self.smallfont, [rect[0] + 20, rect[1] + 60], color = (255, 0, 0)))
            else:
                costlabel.append(GUI.Label("- Metal: "+str(self.PlayerList[self.player][4][0])+"/"+str(metal), self.smallfont, [rect[0] + 20, rect[1] + 60], color = (255, 255, 255)))
            if self.PlayerList[self.player][4][1] < timber:
                costlabel.append(GUI.Label("- Timber: "+str(self.PlayerList[self.player][4][1])+"/"+str(timber), self.smallfont, [rect[0] + 20, rect[1] + 90], color = (255, 0, 0)))
            else:
                costlabel.append(GUI.Label("- Timber: "+str(self.PlayerList[self.player][4][1])+"/"+str(timber), self.smallfont, [rect[0] + 20, rect[1] + 90], color = (255, 255, 255)))
                
            if self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20 + self.PlayerList[self.player][4][4]*3 < energy:
                costlabel.append(GUI.Label("- Energy: "+str(self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20 + self.PlayerList[self.player][4][4]*3 )+"/"+str(energy),
                                       self.smallfont, [rect[0] + 20, rect[1] + 120], color = (255, 0, 0)))
            else:
                costlabel.append(GUI.Label("- Energy: "+str(self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20 + self.PlayerList[self.player][4][4]*3 )+"/"+str(energy),
                                       self.smallfont, [rect[0] + 20, rect[1] + 120], color = (255, 255, 255)))
            if self.PlayerList[self.player][5] < coins*10**9:
                costlabel.append(GUI.Label("- Coins: "+str(self.PlayerList[self.player][5]//10**9)+"/"+str(coins)+" billion", self.smallfont, [rect[0] + 20, rect[1] + 150], color = (255, 0, 0)))
            else:
                costlabel.append(GUI.Label("- Coins: "+str(self.PlayerList[self.player][5]//10**9)+"/"+str(coins)+" billion", self.smallfont, [rect[0] + 20, rect[1] + 150]))

        caplabel.DrawLabel(self.screen)
        for label in costlabel:
            label.DrawLabel(self.screen)
            

    def BuildingUpgrade(self, building):
        if building == "factory":
            highestlevel = 4
            metal = 300
            timber = 700
            energy = 500
            coins = 80
            index = 1
            
        elif building == "port":
            if type(self.area[7][-1]) != list:
                return
            highestlevel = 3
            metal = 400
            timber = 1200
            energy = 600
            coins = 140
            index = 2

        elif building == "airport":
            highestlevel = 2
            metal = 400
            timber = 1500
            energy = 750
            coins = 200
            index = 3

        elif building == "fort":
            highestlevel = 5
            metal = 200
            timber = 600
            energy = 300
            coins = 100
            index = 4

        elif building == "hospital":
            highestlevel = 3
            metal = 200
            timber = 700
            energy = 300
            coins = 200
            index = 5

        elif building == "university":
            highestlevel = 4
            metal = 200
            timber = 700
            energy = 300
            coins = 200
            index = 6

        elif building == "bank":
            highestlevel = 1
            metal = 100
            timber = 500
            energy = 500
            coins = 500
            index = 7

        if self.area[11][index] == highestlevel: return
        if self.PlayerList[self.player][4][0] >= metal and self.PlayerList[self.player][4][1] >= timber and self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20 + self.PlayerList[self.player][4][4]*3 >= energy and self.PlayerList[self.player][5] >= coins*10**9:
            self.PlayerList[self.player][4][0] -= metal
            self.PlayerList[self.player][4][1] -= timber
            energydem = 0
            while energydem < energy:
                if self.PlayerList[self.player][4][2] > 0:
                    self.PlayerList[self.player][4][2] -= 1
                    energydem += 1
                if self.PlayerList[self.player][4][3] > 0:
                    self.PlayerList[self.player][4][3] -= 1
                    energydem += 20
                if self.PlayerList[self.player][4][4] > 0:
                    self.PlayerList[self.player][4][4] -= 1
                    energydem += 3
            self.area[11][index] += 1
            self.AreaList[self.area[8]][11][index] += 1
            if self.area[11][0] == 0: capital = "- Not Capital"
            else: capital = "- Capital"
            if self.area[11][7] == 0: bank = "- No bank"
            else: bank = "- Bank"
            self.labellist = [GUI.Label(self.area[1], self.hugefont, [int(self.w/2 - len(self.area[1])*19), 20]),
                          GUI.Label("- Moral: "+str(round(self.area[6]))+"%", self.largefont, [660, 175]),
                          GUI.Label("- Population: "+str(round(self.area[3], 3))+" million people", self.largefont, [660, 225]),
                          GUI.Label("- Per Capita Income: "+str(int(self.area[9]))+" coins", self.largefont, [660, 275]),
                          GUI.Label("- Resources", self.verylargefont, [660, 340]),
                          GUI.Label("- Food: "+str(int(self.area[4][5][0]))+"/"+str(self.area[4][5][1]), self.largefont, [660, 400]),
                          GUI.Label("- Metal: "+str(self.area[4][0][0])+"/"+str(self.area[4][0][1]), self.largefont, [660, 450]),
                          GUI.Label("- Timber: "+str(int(self.area[4][1][0]))+"/"+str(self.area[4][1][1]), self.largefont, [660, 500]),
                          GUI.Label("- Fossil Fuels: "+str(self.area[4][2][0])+"/"+str(self.area[4][2][1]), self.largefont, [660, 550]),
                          GUI.Label("- Uranium: "+str(self.area[4][3][0])+"/"+str(self.area[4][3][1]), self.largefont, [660, 600]),
                          GUI.Label("- Renewables: "+"| "+(self.area[4][4][0] + 1)*"+"+(6 - self.area[4][4][0])*" "+"|", self.largefont, [660, 650]),
                          GUI.Label(capital, self.largefont, [1360, 175]), Label("- Factory: lvl. "+str(self.area[11][1]), self.largefont, (1360, 260)),
                          GUI.Label("- Port: lvl. "+str(self.area[11][2]), self.largefont, (1360, 320)),
                          GUI.Label("- Airport: lvl. "+str(self.area[11][3]), self.largefont, (1360, 380)),
                          GUI.Label("- Fort: lvl. "+str(self.area[11][4]), self.largefont, (1360, 460)),
                          GUI.Label("- Hospital: lvl. "+str(self.area[11][5]), self.largefont, (1360, 520)),
                          GUI.Label("- University: lvl. "+str(self.area[11][6]), self.largefont, (1360, 580)),
                          GUI.Label(bank, self.largefont, (1360, 660)),]

    def WriteInfo(self):
        f = open("Info.txt", "w")
        for area in self.AreaList:
            f.write("a,")
            f.write(area[1]+",")
            f.write(str(area[2][0])+"."+str(area[2][1])+",")
            f.write(str(area[3])+",")
            i = -1
            for resource in area[4]:
                i += 1
                j = -1
                for element in resource:
                    j += 1
                    f.write(str(element))
                    if j == len(resource) -1 and i == 5:
                        f.write(",")
                    elif j == len(resource) -1:
                        f.write(":")
                    else:
                        f.write("/")
            f.write(area[5]+",")
            f.write(str(area[6])+",")
            for neighbor in area[7]:
                if type(neighbor) == list:
                    f.write("S/")
                    for sea in neighbor:
                        f.write(str(sea))
                        if neighbor.index(sea) == len(neighbor) - 1:
                            f.write(",")
                        else:
                            f.write("/")
                else:
                    f.write(str(neighbor))
                    if area[7].index(neighbor) == len(area[7]) - 1:
                        f.write(",")
                    else:
                        f.write(".")
            f.write(str(area[8])+",")
            f.write(str(area[9])+",")
            f.write(str(area[10])+",")
            i = 0
            for building in area[11]:
                f.write(str(building))
                if i == 7:
                    f.write("\n")
                else:
                    f.write(".")
                i += 1

        for troop in self.TroopList:
            f.write("t,")
            f.write(str(troop[1])+",")
            f.write(troop[2]+",")
            f.write(troop[3]+",")
            f.write(str(troop[4])+",")
            i = -1
            for units in troop[5]:
                i += 1
                if i == 7:
                    f.write(str(units)+",")
                else:
                    f.write(str(units)+".")
            f.write(str(troop[6])+"\n")

        for player in self.PlayerList:
            f.write("p,")
            f.write(str(player[1])+",")
            f.write(player[2]+",")
            
            for area in player[3]:
                if player[3].index(area) == len(player[3]) - 1:
                    f.write(str(area)+",")
                else:
                    f.write(str(area)+".")
            i = -1 
            for resource in player[4]:
                i+=1
                if i == 5:
                    f.write(str(resource)+",")
                else:
                    f.write(str(resource)+"/")
            f.write(str(player[5])+",")
            f.write(str(player[6])+",")
            for troop in player[7]:
                if player[7].index(troop) == len(player[7]) - 1:
                    f.write(str(troop)+"\n")
                else:
                    f.write(str(troop)+".")
        f.close()

    def ReadInfo(self, screen):
        f = open("Info.txt", "r")
        self.AreaList = []
        self.TroopList = []
        self.PlayerList = []
        for line in f:
            lista = []
        
            if line[0] == "a":
                lista = line.split(",")
                lista[0] = screen
                lista[2] = lista[2].split(".")
                for i in range(2):
                    lista[2][i] = int(lista[2][i])
                lista[3] = float(lista[3])
                lista[4] = lista[4].split(":")
            
                for i in range(6):
                    lista[4][i] = lista[4][i].split("/")
                    for j in range(len(lista[4][i])):
                        lista[4][i][j] = int(float(lista[4][i][j]))
                lista[6] = float(lista[6])
                lista[7] = lista[7].split(".")
                if "S" in lista[7][-1]:
                    lista[7][len(lista[7])-1] = lista[7][-1].split("/")
                    lista[7][-1].pop(0)
                    for sea in lista[7][-1]:
                        lista[7][-1][lista[7][-1].index(sea)] = int(sea)
                for i in range(len(lista[7]) - 1):
                    lista[7][i] = int(lista[7][i])
                lista[8] = int(lista[8])
                lista[9] = float(lista[9])
                lista[10] = int(lista[10])
                lista[11] = lista[11].split(".")
                for i in range(len(lista[11])):
                    lista[11][i] = int(lista[11][i])
                self.AreaList.append(lista)
            
            if line[0] == "t":
                lista = line.split(",")
                lista[0] = screen
                lista[1] = int(lista[1])
                lista[4] = int(lista[4])
                lista[5] = lista[5].split(".")
                for i in range(8):
                    lista[5][i] = int(lista[5][i])
                lista[6] = float(lista[6])                
                self.TroopList.append(lista)
                
            if line[0] == "p":
                lista = line.split(",")
                lista[0] = screen
                lista[1] = int(lista[1])
                lista[3] = lista[3].split(".")
                for area in lista[3]:
                    lista[3][lista[3].index(area)] = int(area)
                lista[4] = lista[4].split("/")
                for i in range(6):
                    lista[4][i] = int(float(lista[4][i]))
                lista[5] = int(float(lista[5]))
                lista[6] = float(lista[6])
                lista[7] = lista[7].split(".")
                for troop in lista[7]:
                    lista[7][lista[7].index(troop)] = int(troop)
                self.PlayerList.append(lista)
        
        f.close()
        return  
