""" Contains the AreaScene class """

import sys
import os
import random
import datetime
import math
import gc
import ctypes

import pygame
from pygame import font

import GUI
import MAIN1 as MAIN
import GENERAL as GEN

gc.enable()

class AreaScene():
    """ This class is responsible for the scene that corresponds to a
          particular area's menu. It also contains the necessary
          functions for buildings. """
    def __init__(self, screen, arealist, clock, numplayers, year, currentplayer, player):
        """ Initializes the variables of the AreaScene class, creates
              necessary Label, Bar objects and the pygame Rects
              corresponding to buttons. """
        # Reads from the Info.txt file the current state of the game
        # and creates the self.AreaList, the self.TroopList and the
        # self.PlayerList lists.
        self.ReadInfo(screen)

        self.time = pygame.time.Clock()
        
        self.screen = screen
        self.area = arealist
        self.Clock = clock
        self.NumPlayers = numplayers
        self.year = year
        self.currentplayer = currentplayer
        self.player = player
        
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.pause = False

        # Gets the size metrics of the current display
        metrics = GEN.screen_metrics()
        self.w = metrics[0]
        self.h = metrics[1]
        self.ratiow = metrics[2]
        self.ratioh = metrics[3]

        #Creates the necessary font objects
        self.hugefont = pygame.font.SysFont("Times", int(80*self.ratiow))
        self.verylargefont = pygame.font.SysFont("Times", int(50*self.ratiow))
        self.largefont = pygame.font.SysFont("Times", int(40*self.ratiow))
        self.medfont = pygame.font.SysFont("Times", int(25*self.ratiow))
        self.smallfont = pygame.font.SysFont("Times", int(20*self.ratiow))

        # Creation of pygame Rect objects associated with buttons
        self.ButtonDict = {}
        buttonw = int(180*self.ratiow)
        buttonh = int(50*self.ratioh)
        marg = int(1660*self.ratiow)
        self.BackToMain = pygame.Rect((int(1600*self.ratiow), int(20*self.ratioh),
                                                                 buttonw, buttonh))
        self.BuildCapital = pygame.Rect((marg, int(170*self.ratioh), buttonw, buttonh))
        self.BuildFactory = pygame.Rect((marg, int(255*self.ratioh), buttonw, buttonh))
        self.BuildPort = pygame.Rect((marg, int(315*self.ratioh), buttonw, buttonh))
        self.BuildAirPort = pygame.Rect((marg, int(375*self.ratioh), buttonw, buttonh))
        self.BuildFort = pygame.Rect((marg, int(455*self.ratioh), buttonw, buttonh))
        self.BuildHospital = pygame.Rect((marg, int(515*self.ratioh), buttonw, buttonh))
        self.BuildUni = pygame.Rect((marg, int(575*self.ratioh), buttonw, buttonh))
        self.BuildBank = pygame.Rect((marg, int(655*self.ratioh), buttonw, buttonh))
        
        # Creation of Bar objects (sliding bars)
        self.bar = pygame.image.load("bar.png")
        self.bar = pygame.transform.scale(self.bar, (int(400*self.ratiow), int(10*self.ratioh)))
        self.point = pygame.image.load("point.png")
        self.point = pygame.transform.scale(self.point, (int(40*self.ratiow), int(40*self.ratioh)))
        self.playerdot = pygame.image.load(self.area[5]+".png")
        self.playerdot = pygame.transform.scale(self.playerdot, (buttonh, buttonh))
        self.barlist = []
        marg = int(60*self.ratiow)
        marg2 = marg//10
        self.taxesbar = GUI.Bar(self.screen, [marg - marg2, int(200*self.ratioh)], "Taxes",
                                                [marg, int(220*self.ratioh)], [0, 100], self.area[10])
        self.barlist.append(self.taxesbar)
        self.foodbar = GUI.Bar(self.screen, [marg - marg2, int(280*self.ratioh)], "Food",
                                               [marg, int(300*self.ratioh)], [0, 200], self.area[4][5][2])
        self.barlist.append(self.foodbar)
        self.metalbar = GUI.Bar(self.screen, [marg - marg2, int(360*self.ratioh)], "Metal",
                                                 [marg, int(380*self.ratioh)], [0, 100], self.area[4][0][2])
        self.barlist.append(self.metalbar)
        self.timberbar = GUI.Bar(self.screen, [marg - marg2, int(440*self.ratioh)], "Timber",
                                                  [marg, int(460*self.ratioh)], [0, 100], self.area[4][1][2])
        self.barlist.append(self.timberbar)
        self.fossilbar = GUI.Bar(self.screen, [marg - marg2, int(520*self.ratioh)], "Fossils",
                                                [marg, int(540*self.ratioh)], [0, 100], self.area[4][2][2])
        self.barlist.append(self.fossilbar)
        self.uraniumbar = GUI.Bar(self.screen, [marg - marg2, int(600*self.ratioh)], "Uranium",
                                                     [marg, int(620*self.ratioh)], [0, 100], self.area[4][3][2])
        self.barlist.append(self.uraniumbar)
        self.renewbar = GUI.Bar(self.screen, [marg - marg2, int(680*self.ratioh)], "Renewables",
                                                 [marg, int(700*self.ratioh)], [0, 100], self.area[4][4][1])
        self.barlist.append(self.renewbar)

        # Creation of Label objects
        if self.area[11][0] == 0: capital = "- Not Capital"
        else: capital = "- Capital"
        if self.area[11][7] == 0: bank = "- No bank"
        else: bank = "- Bank"
        marg = int(660*self.ratiow)
        marg2 = int(1360*self.ratiow) ###############################################################################
        self.labellist = [GUI.Label(self.area[1], self.hugefont, [int(self.w/2 - len(self.area[1])
                                                    *19), int(20*self.ratioh)]),
                                GUI.Label("- Moral: "+str(round(self.area[6]))+"%", self.largefont,
                                                  [marg, int(175*self.ratioh)]),
                                GUI.Label("- Population: "+str(round(self.area[3], 3))
                                                  +" million people",
                                                  self.largefont, [marg, int(225*self.ratioh)]),
                                GUI.Label("- Per Capita Income: "+str(int(self.area[9]))
                                                  +" coins", self.largefont, [marg, int(275
                                                                                            *self.ratioh)]),
                                GUI.Label("- Resources", self.verylargefont,
                                                   [marg, int(340*self.ratioh)]),
                                GUI.Label("- Food: "+str(int(self.area[4][5][0]))+"/"
                                                   +str(self.area[4][5][1]), self.largefont,
                                                   [marg, int(400*self.ratioh)]),
                                GUI.Label("- Metal: "+str(self.area[4][0][0])+"/"
                                                  +str(self.area[4][0][1]), self.largefont,
                                                  [marg, int(450*self.ratioh)]),
                                GUI.Label("- Timber: "+str(int(self.area[4][1][0]))+"/"
                                                  +str(self.area[4][1][1]), self.largefont,
                                                  [marg, int(500*self.ratioh)]),
                                GUI.Label("- Fossil Fuels: "+str(self.area[4][2][0])+"/"
                                                  +str(self.area[4][2][1]), self.largefont,
                                                  [marg, int(550*self.ratioh)]),
                                GUI.Label("- Uranium: "+str(self.area[4][3][0])+"/"
                                                   +str(self.area[4][3][1]), self.largefont,
                                                   [marg, int(600*self.ratioh)]),
                                GUI.Label("- Renewables: "+"| "+(self.area[4][4][0] + 1)*"+"
                                                   +(6 - self.area[4][4][0])*" "+"|", self.largefont,
                                                   [marg, int(650*self.ratioh)]),
                                GUI.Label(capital, self.largefont, [marg2, int(175*self.ratioh)]),
                                GUI.Label("- Factory: lvl. "+str(self.area[11][1]), self.largefont,
                                                   (marg2, int(260*self.ratioh))),
                                GUI.Label("- Port: lvl. "+str(self.area[11][2]), self.largefont,
                                                  (marg2, int(320*self.ratioh))),
                                GUI.Label("- Airport: lvl. "+str(self.area[11][3]), self.largefont,
                                                  (marg2, int(380*self.ratioh))),
                                GUI.Label("- Fort: lvl. "+str(self.area[11][4]), self.largefont,
                                                  (marg2, int(460*self.ratioh))),
                                GUI.Label("- Hospital: lvl. "+str(self.area[11][5]), self.largefont,
                                                  (marg2, int(520*self.ratioh))),
                                GUI.Label("- University: lvl. "+str(self.area[11][6]), self.largefont,
                                                  (marg2, int(580*self.ratioh))),
                                GUI.Label(bank, self.largefont, (marg2, int(660*self.ratioh)))]

        # Calling the self.Draw method 
        self.Draw()
        
  
    def DrawButton(self, rect, text, textloc):
        """ (rect, text, textlocation)
              Draws a button in the position of rect with the label
              written in text in the position of textlocation. """
        self.ButtonDict.update({str(pygame.Rect(rect)):pygame.Rect(rect)})
        label = self.medfont.render(text, 1, self.white)
        self.screen.fill(self.black, rect)
        self.screen.blit(label, textloc)
        

    def Draw(self):
        """ Draws on the screen all the components of the
              display, handles events. """
        while 1:
            self.screen.fill((50, 50, 50))
            self.screen.blit(self.playerdot, (int(self.w/2 + 19*self.ratiow
                                     *len(self.area[1])) + 20, int(50*self.ratioh)))

            # Updating the clock, updating its display on the screen,
            # checking whether the time is up for the player.
            dt = self.time.tick()
            self.Clock -= dt/1000
            if self.Clock < 0:
                active_scene = MAIN.MainScene(self.screen, self.NumPlayers, "AreaScene",
                                                                        self.Clock, self.year)
            clock_ = str(int(self.Clock/60))+":"+str(int(self.Clock%60))
            if self.Clock%60 < 10: clock_ = str(int(self.Clock/60))+":0"+str(int(self.Clock%60))            
            clock_label = self.largefont.render(clock_, 1, (255, 255, 255))
            self.screen.blit(clock_label, (int(1820*self.ratiow), int(20*self.ratioh)))

            # Drawing the buttons.
            marg1 = int(1660*self.ratiow)
            marg2 = int(1708*self.ratioh)
            buttonw = int(180*self.ratiow)
            buttonh = int(50*self.ratioh)
            self.DrawButton((int(1600*self.ratiow), int(20*self.ratioh), buttonw, buttonh),
                                          "Back to Map >>", [int(1610*self.ratiow), int(30*self.ratioh)])
            self.DrawButton((marg1, int(170*self.ratioh), buttonw, buttonh), "Upgrade",
                                          [marg2, int(179*self.ratioh)])
            self.DrawButton((marg1, int(255*self.ratioh), buttonw, buttonh), "Upgrade",
                                          [marg2, int(264*self.ratioh)])
            self.DrawButton((marg1, int(375*self.ratioh), buttonw, buttonh), "Upgrade",
                                          [marg2, int(384*self.ratioh)])
            self.DrawButton((marg1, int(455*self.ratioh), buttonw, buttonh), "Upgrade",
                                          [marg2, int(464*self.ratioh)])
            self.DrawButton((marg1, int(515*self.ratioh), buttonw, buttonh), "Upgrade",
                                          [marg2, int(524*self.ratioh)])
            self.DrawButton((marg1, int(575*self.ratioh), buttonw, buttonh), "Upgrade",
                                          [marg2, int(584*self.ratioh)])
            self.DrawButton((marg1, int(655*self.ratioh), buttonw, buttonh), "Upgrade",
                                          [marg2, int(664*self.ratioh)])
            self.DrawButton((marg1, int(315*self.ratioh), buttonw, buttonh), "Upgrade",
                                          [marg2, int(324*self.ratioh)])

            # Drawing the sliding bars.
            self.foodbar.Draw_Bar(self.area[4][5][2], self.bar, self.point)
            self.taxesbar.Draw_Bar(self.area[10], self.bar, self.point)
            self.metalbar.Draw_Bar(self.area[4][0][2], self.bar, self.point)
            self.timberbar.Draw_Bar(self.area[4][1][2], self.bar, self.point)
            self.fossilbar.Draw_Bar(self.area[4][2][2], self.bar, self.point)
            self.uraniumbar.Draw_Bar(self.area[4][3][2], self.bar, self.point)
            self.renewbar.Draw_Bar(self.area[4][4][1], self.bar, self.point)

            #Drawing the labels.
            for label in self.labellist:
                label.DrawLabel(self.screen)
            
            mouse_pos = pygame.mouse.get_pos()

            # i is the index of the area in question.
            i = self.area[8]
            # Calling the Drag method of the Bar class when
            # the user drags the sliding point.
            if self.taxesbar.drag == True:
                self.area[10] = self.taxesbar.Drag(mouse_pos)
                self.AreaList[i][10] = self.area[10]
            if self.foodbar.drag == True:
                self.area[4][5][2] = self.foodbar.Drag(mouse_pos)
                self.AreaList[i][4][5][2] = self.area[4][5][2]
            if self.metalbar.drag == True:
                self.area[4][0][2] = self.metalbar.Drag(mouse_pos)
                self.AreaList[i][4][0][2] = self.area[4][0][2]
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

            # Draws a white rect around the button when the
            # mouse cursor is above it.
            for button in self.ButtonDict.keys():
                if self.ButtonDict[button].collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, self.white, self.ButtonDict[button], 1)

            # Calls the Hover functions when the mouse cursor 
            # is over one of the buttons for upgrading buildings.
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

            # Event handling.
            for event in pygame.event.get():
                # Events for quiting the game.
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()

                # Events in which the user clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BackToMain.collidepoint(mouse_pos):
                        # Writes state of the game in Info.txt.
                        self.WriteInfo()
                        # Creates an object of MainScene
                        active_scene = MAIN.MainScene(self.screen, self.NumPlayers, "AreaScene",
                                                                                 self.Clock, self.year)
                    # Calling the right Upgrade method when the corresponding
                    # button is pushed.
                    if self.currentplayer:
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

                    # Controls the drag parameter of each Bar object.
                    for bar in self.barlist:
                        if bar.pointrect.collidepoint(mouse_pos) and self.currentplayer:
                            temp = bar.drag
                            if temp == True: bar.drag = False
                            if temp == False: bar.drag = True
                            
            pygame.display.flip()


    def CapitalHover(self):
        """ This method is called when the cursor hovers over the
              self.BuildCapital rect, to create a display of
              requirements for upgrading the capital. """
        # Defining the dimensions of the display
        extraw = int(self.ratiow*20)
        extrah = int(self.ratioh*20)
        rect = [self.BuildCapital[0], self.BuildCapital[1] + self.BuildCapital[3]
                    + extrah, self.BuildCapital[2] + int(60*self.ratiow), int(200*self.ratioh)]

        # Drawing the display
        self.screen.fill([50, 50, 50, 50], tuple(rect))
        pygame.draw.rect(self.screen, [0, 0, 0, 0], tuple(rect), 3)

        # Handling what's written in the display
        #  self.area[11][0] is the capital, 0 for none, 1 for existing
        if self.area[11][0] == 1:
            caplabel = GUI.Label("Cannot upgrade", self.medfont, [rect[0] + extraw,
                                                 rect[1] + extrah])
            costlabel = [GUI.Label("", self.smallfont, [rect[0] + extraw, rect[1]
                                                   + int(50*self.ratioh)])]
            self.capital_check = -1
        else:
            self.capital_check = 0
            # Checks every area that belongs to current player
            # to examine if there is a capital built already in some other
            # area.
            for everyarea in self.AreaList:
                if self.area[5] == everyarea[5]:
                    if everyarea[11][0] == 1:
                        self.capital_check = 1
                        break

            # If there is a capital elsewhere: 
            if self.capital_check == 1:
                caplabel = GUI.Label("Build new capital", self.medfont, [rect[0] + extraw,
                                                     rect[1] + extrah])
                costlabel = []
                # Checking all cost requirements for building a new capital.
                # Metal
                if self.PlayerList[self.player][4][0] < 1000:
                    costlabel.append(GUI.Label("- Metal: "+str(self.PlayerList[self.player][4][0])
                                                                   +"/1000", self.smallfont, [rect[0] + extraw, rect[1]
                                                                    + int(60*self.ratioh)], color = (255, 0, 0)))
                else:
                    costlabel.append(GUI.Label("- Metal: "+str(self.PlayerList[self.player][4][0])
                                                                    +"/1000", self.smallfont, [rect[0] + extraw, rect[1]
                                                                    + int(60*self.ratioh)], color = (255, 255, 255)))
                # Timber
                if self.PlayerList[self.player][4][1] < 3000:
                    costlabel.append(GUI.Label("- Timber: "+str(self.PlayerList[self.player][4][1])
                                                                   +"/3000", self.smallfont, [rect[0] + extraw, rect[1]
                                                                   + int(90*self.ratioh)], color = (255, 0, 0)))
                else:
                    costlabel.append(GUI.Label("- Timber: "+str(self.PlayerList[self.player][4][1])
                                                                   +"/3000", self.smallfont, [rect[0] + extraw, rect[1]
                                                                   + int(90*self.ratioh)], color = (255, 255, 255)))
                # Energy
                if (self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20
                     + self.PlayerList[self.player][4][4]*3 < 1000):
                    costlabel.append(GUI.Label("- Energy: "+str(self.PlayerList[self.player][4][2]
                                                                   + self.PlayerList[self.player][4][3]*20
                                                                   + self.PlayerList[self.player][4][4]*3 )+"/1000",
                                                                   self.smallfont, [rect[0] + extraw, rect[1]
                                                                   + int(120*self.ratioh)], color = (255, 0, 0)))
                else:
                    costlabel.append(GUI.Label("- Energy: "+str(self.PlayerList[self.player][4][2]
                                                                   + self.PlayerList[self.player][4][3]*20
                                                                   + self.PlayerList[self.player][4][4]*3 )+"/1000",
                                                                   self.smallfont, [rect[0] + extraw, rect[1]
                                                                   + int(120*self.ratioh)], color = (255, 255, 255)))
                # Coins
                if self.PlayerList[self.player][5] < 10**11:
                    costlabel.append(GUI.Label("- Coins: "+str(self.PlayerList[self.player][5]//10**9)
                                                                   +"/100 billion", self.smallfont, [rect[0] + extraw,
                                                                   rect[1] + int(150*self.ratioh)], color = (255, 0, 0)))
                else:
                    costlabel.append(GUI.Label("- Coins: "+str(self.PlayerList[self.player][5]//10**9)
                                                                    +"/100 billion", self.smallfont, [rect[0] + extraw,
                                                                    rect[1] + int(150*self.ratioh)]))
            # Checking where there is no capital
            else:
                caplabel = GUI.Label("Found your capital", self.medfont, [rect[0] + extraw,
                                                     rect[1] + extrah])
                costlabel = [GUI.Label("Free", self.smallfont, [rect[0] + extraw, rect[1]
                                                        + int(90*self.ratioh)])]

        caplabel.DrawLabel(self.screen)
        for label in costlabel:
            label.DrawLabel(self.screen)

    def CapitalUpgrade(self):
        """ This function is called whenever the self.BuildCapital rect is
              clicked on. It manages the upgrading of the capital building"""
        # capital_check = -1: already a capital in the area
        # capital_check = 0: no capital in any of the player's areas
        # capital_check = 1: there's a capital elsewhere in the player's areas

        # If there is already a capital, it returns.
        if self.capital_check == -1:
            return

        # If there is no capital, it builds one for free.
        elif self.capital_check == 0:
            self.area[11][0] = 1
            self.AreaList[self.area[8]][11][0] = 1
            self.labellist[11] = GUI.Label("- Capital", self.largefont, [int(1360*self.ratiow),
                                                                int(175*self.ratioh)])
            self.capital_check = -1
            return

        # If there is already a capital elsewhere, it examines
        # whether the player has the essential resources to
        # build a new capital, demolishes the old one,
        # and builds a new one, subtracting the cost off
        # the player's resources.
        else:
            # Checks resources' availability.
            if (self.PlayerList[self.player][4][0] >= 2000
                    and self.PlayerList[self.player][4][1] >= 3000
                    and (self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20
                       + self.PlayerList[self.player][4][4]*3 >= 1000)
                    and self.PlayerList[self.player][5] >= 10**11):
                # Subtracting the costs.
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
                self.PlayerList[self.player][5] -= 100*(10**9)
                
                # Demolishes old capital
                for area in self.PlayerList[self.player][3]:
                    if self.AreaList[area][11][0] == 1:
                        self.AreaList[area][11][0] = 0
                        break
                # Builds new capital
                self.area[11][0] = 1
                self.AreaList[self.area[8]][11][0] = 1
                self.capital_check = -1
            else: return
            

    def BuildingHover(self, building):
        """ (building)
              This method is called when the cursor hovers over
              any of the self.Build______ rects, to create a display of
              requirements for upgrading the corresponding building. """

        extraw = int(60*self.ratiow)
        extrah = int(20*self.ratioh)
        vert = int(200*self.ratioh)

        # Determing which building the function was called for.
        # Adjusting variables.
        if building == "factory":
            # Display position and size.
            rect = [self.BuildFactory[0], self.BuildFactory[1] + self.BuildFactory[3] + extrah,
                       self.BuildFactory[2] + extraw, vert]
            # Highest level the building can reach.
            highestlevel = 4
            # Cost of upgrading.
            metal = 300
            timber = 700
            energy = 500
            coins = 80
            # Index in self.area[11]
            index = 1
            
        elif building == "port":
            rect = [self.BuildPort[0], self.BuildPort[1] + self.BuildPort[3] + extrah,
                       self.BuildPort[2] + extraw, vert]
            if type(self.area[7][-1]) != list:
                caplabel = GUI.Label("Cannot build port", self.medfont, [rect[0] + extraw//3,
                                                     rect[1] + extrah])
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
            rect = [self.BuildAirPort[0], self.BuildAirPort[1] + self.BuildAirPort[3] + extrah,
                        self.BuildAirPort[2] + extraw, vert]
            highestlevel = 2
            metal = 400
            timber = 1500
            energy = 750
            coins = 200
            index = 3

        elif building == "fort":
            rect = [self.BuildFort[0], self.BuildFort[1] + self.BuildFort[3] + extrah,
                       self.BuildFort[2] + extraw, vert]
            highestlevel = 5
            metal = 200
            timber = 600
            energy = 300
            coins = 100
            index = 4

        elif building == "hospital":
            rect = [self.BuildHospital[0], self.BuildHospital[1] + self.BuildHospital[3] + extrah,
                       self.BuildHospital[2] + extraw, vert]
            highestlevel = 3
            metal = 200
            timber = 700
            energy = 300
            coins = 200
            index = 5

        elif building == "university":
            rect = [self.BuildUni[0], self.BuildUni[1] + self.BuildUni[3] + extrah,
                       self.BuildUni[2] + extraw, vert]
            highestlevel = 4
            metal = 200
            timber = 700
            energy = 300
            coins = 200
            index = 6

        elif building == "bank":
            rect = [self.BuildBank[0], self.BuildBank[1] + self.BuildBank[3] + extrah,
                       self.BuildBank[2] + extraw, vert]
            highestlevel = 1
            metal = 100
            timber = 500
            energy = 500
            coins = 500
            index = 7

        # Drawing the display.
        extraw = int(self.ratiow*20)
        self.screen.fill([50, 50, 50, 50], tuple(rect))
        pygame.draw.rect(self.screen, [0, 0, 0, 0], tuple(rect), 3)

        # Configuring the labels, red when there
        # are not enough resources, white when there
        # are.
        if self.area[11][index] == highestlevel:
            caplabel = GUI.Label("Cannot upgrade", self.medfont, [rect[0] + extraw, rect[1]
                                                + extrah])
            costlabel = [GUI.Label("", self.smallfont, [rect[0] + extraw, rect[1]
                                                  + int(50*self.ratioh)])]
        else:
            caplabel = GUI.Label("Upgrade "+building, self.medfont, [rect[0] + extraw,
                                                rect[1] + extrah])
            
            costlabel = []
            if self.PlayerList[self.player][4][0] < metal:
                costlabel.append(GUI.Label("- Metal: "+str(self.PlayerList[self.player][4][0])
                                                               +"/"+str(metal), self.smallfont, [rect[0] + extraw,
                                                                rect[1] + int(60*self.ratioh)], color = (255, 0, 0)))
            else:
                costlabel.append(GUI.Label("- Metal: "+str(self.PlayerList[self.player][4][0])
                                                              +"/"+str(metal), self.smallfont, [rect[0] + extraw,
                                                              rect[1] + int(60*self.ratioh)], color = (255, 255, 255)))
                
            if self.PlayerList[self.player][4][1] < timber:
                costlabel.append(GUI.Label("- Timber: "+str(self.PlayerList[self.player][4][1])
                                                               +"/"+str(timber), self.smallfont, [rect[0] + extraw,
                                                               rect[1] + int(90*self.ratioh)], color = (255, 0, 0)))
            else:
                costlabel.append(GUI.Label("- Timber: "+str(self.PlayerList[self.player][4][1])
                                                               +"/"+str(timber), self.smallfont, [rect[0] + extraw,
                                                                rect[1] + int(90*self.ratioh)], color = (255, 255, 255)))
                
            if (self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20
                    + self.PlayerList[self.player][4][4]*3 < energy):
                costlabel.append(GUI.Label("- Energy: "+str(self.PlayerList[self.player][4][2]
                                                               + self.PlayerList[self.player][4][3]*20
                                                               + self.PlayerList[self.player][4][4]*3 )+"/"+str(energy),
                                                                self.smallfont, [rect[0] + extraw,
                                                                rect[1] + int(120*self.ratioh)], color = (255, 0, 0)))
            else:
                costlabel.append(GUI.Label("- Energy: "+str(self.PlayerList[self.player][4][2]
                                                                + self.PlayerList[self.player][4][3]*20
                                                                + self.PlayerList[self.player][4][4]*3 )+"/"+str(energy),
                                                                self.smallfont, [rect[0] + extraw,
                                                                rect[1] + int(120*self.ratioh)], color = (255, 255, 255)))
                
            if self.PlayerList[self.player][5] < coins*10**9:
                costlabel.append(GUI.Label("- Coins: "+str(self.PlayerList[self.player][5]//10**9)
                                                              +"/"+str(coins)+" billion", self.smallfont,
                                                              [rect[0] + extraw, rect[1] + int(150*self.ratioh)],
                                                              color = (255, 0, 0)))
            else:
                costlabel.append(GUI.Label("- Coins: "+str(self.PlayerList[self.player][5]//10**9)
                                                               +"/"+str(coins)+" billion", self.smallfont,
                                                               [rect[0] + extraw, rect[1] + int(150*self.ratioh)]))

        caplabel.DrawLabel(self.screen)
        for label in costlabel:
            label.DrawLabel(self.screen)
            

    def BuildingUpgrade(self, building):
        """ (building)
              This method is called when a
              self.Build_____ rect is clicked on.
              It manages the upgrading of buildings. """

        #  Configuring variables according to building.
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

        # Checking resources availability
        if (self.PlayerList[self.player][4][0] >= metal
                and self.PlayerList[self.player][4][1] >= timber
                and (self.PlayerList[self.player][4][2] + self.PlayerList[self.player][4][3]*20
                   + self.PlayerList[self.player][4][4]*3 >= energy)
                and self.PlayerList[self.player][5] >= coins*10**9):
            #  Subtracting cost.
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
            self.PlayerList[self.player][5] -= coins*(10**9)

            # Upgrading.
            self.area[11][index] += 1
            self.AreaList[self.area[8]][11][index] += 1
            if self.area[11][0] == 0: capital = "- Not Capital"
            else: capital = "- Capital"
            if self.area[11][7] == 0: bank = "- No bank"
            else: bank = "- Bank"
            marg1 = int(660*self.ratiow)
            marg2 = int(1360*self.ratiow)
            # Configuring lables (could be independent function) ######################################################
            self.labellist = [GUI.Label(self.area[1], self.hugefont, [int(self.w/2
                                                        - len(self.area[1])*19), int(20*self.ratioh)]),
                          GUI.Label("- Moral: "+str(round(self.area[6]))+"%", self.largefont,
                                            [marg1, int(175*self.ratioh)]),
                          GUI.Label("- Population: "+str(round(self.area[3], 3))+" million people",
                                             self.largefont, [marg1, int(225*self.ratioh)]),
                          GUI.Label("- Per Capita Income: "+str(int(self.area[9]))+" coins",
                                             self.largefont, [marg1, int(275*self.ratioh)]),
                          GUI.Label("- Resources", self.verylargefont, [marg1, int(340*self.ratioh)]),
                          GUI.Label("- Food: "+str(int(self.area[4][5][0]))+"/"+str(self.area[4][5][1]),
                                             self.largefont, [marg1, int(400*self.ratioh)]),
                          GUI.Label("- Metal: "+str(self.area[4][0][0])+"/"+str(self.area[4][0][1]),
                                            self.largefont, [marg1, int(450*self.ratioh)]),
                          GUI.Label("- Timber: "+str(int(self.area[4][1][0]))+"/"+str(self.area[4][1][1]),
                                            self.largefont, [marg1, int(500*self.ratioh)]),
                          GUI.Label("- Fossil Fuels: "+str(self.area[4][2][0])+"/"+str(self.area[4][2][1]),
                                            self.largefont, [marg1, int(550*self.ratioh)]),
                          GUI.Label("- Uranium: "+str(self.area[4][3][0])+"/"+str(self.area[4][3][1]),
                                            self.largefont, [marg1, int(600*self.ratioh)]),
                          GUI.Label("- Renewables: "+"| "+(self.area[4][4][0] + 1)*"+"
                                             +(6 - self.area[4][4][0])*" "+"|", self.largefont,
                                             [marg1, int(650*self.ratioh)]),
                          GUI.Label(capital, self.largefont, [marg2, int(175*self.ratioh)]),
                          GUI.Label("- Factory: lvl. "+str(self.area[11][1]), self.largefont,
                                            (marg2, int(260*self.ratioh))),
                          GUI.Label("- Port: lvl. "+str(self.area[11][2]), self.largefont,
                                            (marg2, int(320*self.ratioh))),
                          GUI.Label("- Airport: lvl. "+str(self.area[11][3]), self.largefont,
                                            (marg2, int(380*self.ratioh))),
                          GUI.Label("- Fort: lvl. "+str(self.area[11][4]), self.largefont,
                                            (marg2, int(460*self.ratioh))),
                          GUI.Label("- Hospital: lvl. "+str(self.area[11][5]), self.largefont,
                                            (marg2, int(520*self.ratioh))),
                          GUI.Label("- University: lvl. "+str(self.area[11][6]), self.largefont,
                                             (marg2, int(580*self.ratioh))),
                          GUI.Label(bank, self.largefont, (marg2, int(660*self.ratioh)))]


    def WriteInfo(self):
        """ This method writes the game info in the
              Info.txt file. """
        f = open("Info.txt", "w")

        # Writing the information in self.AreaList.
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

        # Writing info in self.TroopList
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

        # Writing info in self.PlayerList.
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
        """ Reads the info in the Info.txt file
              and creates the Area, Troop and
              Player lists. """
        
        f = open("Info.txt", "r")
        
        self.AreaList = []
        self.TroopList = []
        self.PlayerList = []
        
        for line in f:
            lista = []

            # Lines for self.AreaList
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

            # Lines for self.TroopList.
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

            # Lines for self.PlayerList.
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
