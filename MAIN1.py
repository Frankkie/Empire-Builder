import pygame, sys, os, random, datetime, math, ctypes
from pygame import font

import OBJECTS as OBJ
import GENERAL as GEN
import AREA


class MainScene():
    def __init__(self, screen, NumPlayers, previous, clock, year):
        self.NumPlayers = NumPlayers
        self.screen = screen
        metrics = GEN.screen_metrics()
        self.w = metrics[0]
        self.h = metrics[1]
        self.ratiow = metrics[2]
        self.ratioh = metrics[3]
        screen.fill((0, 0, 0))
        if previous == "MenuScene":
            self.InitializeGame()
            check = 1
        else:
            self.ReadInfo(screen)
            self.listofplayers = []
            for i in range(self.NumPlayers + 1):
                self.listofplayers = self.listofplayers + [i]
            year -= 1
            check = 0
        while True:
            year += 1
            for player in self.listofplayers:
                if check:
                    self.Clock = 180.9
                    self.UpdateStatistics(player)
                else:
                    self.Clock = clock
                if self.listofplayers.index(player) != len(self.listofplayers) - 1:
                    self.DrawMap(screen, player, year, self.Clock)
                check = 1
        
            

    def SwitchToScene(self, scene):
        active_scene = scenes[scene]

    def InitializeGame(self):
        self.AreaList = self.InitializeAreaList(self.screen, self.NumPlayers)
        num = int(self.NumPlayers)
        if num == 1: cap = 60
        if num == 2: cap = 40
        if num == 3: cap = 30
        if num > 3: cap = 25
        for i in range (num):
            result = 0
            while not result:
                result = self.DistributeAreas(num, i+1, cap)
        self.TroopList = self.InitializeTroopList(self.screen)
        self.PlayerList = self.InitializePlayerList(self.screen, num)
        self.listofplayers = []
        for i in range(num + 1):
            self.listofplayers = self.listofplayers + [i]

    def InitializeAreaList(self, screen, players):
        f = open("InitAreas.txt", "r")
        self.AreaList = []

        for line in f:
            lista = [screen]
            temp = []
            temp2 = []
            line = line.split(",")
            temp.append(int(int(line[1])*self.ratiow))
            temp.append(int(int(line[2])*self.ratioh))
            line[3] = int(line[3])
            line[6] = int(line[6])
            temp2 = line[7].split(".")
            if "S" in temp2[-1]:
                temp2[-1] = temp2[-1].split("/")
                temp2[-1].pop(0)
            for i in range(len(temp2) - 1):
                temp2[i] = int(temp2[i])
            if type(temp2[-1]) == list:
                for i in range(len(temp2[-1])):
                    temp2[-1][i] = int(temp2[-1][i])
            else:
                temp2[-1] = int(temp2[-1])
            line[8].rstrip()
            line[8] = int(line[8])
            lista.append(line[0])
            lista.append(temp)
            lista.append(line[3])
            lista.append(line[4])
            lista.append(line[5])
            lista.append(line[6])
            lista.append(temp2)
            lista.append(line[8])
            lista.append(1000)
            lista.append(30)
            
            lista.append([0, 0, 0, 0, 0, 0, 0, 0])

            resources = list(lista[4])
            
            for i in range(6):
                resources[i] = int(resources[i])
            
            if resources[0] == 0: resources[0] = [1000, 1000, 10]
            else: resources[0] = [5000*resources[0], 5000*resources[0], 10]

            if resources[1] == 0: resources[1] = [200, 200, 30]
            else: resources[1] = [200 + resources[1]*600, 200 + resources[1]*600, 30]

            resources[2] = [1000 + resources[2]*1000, 1000 + resources[2]*1000, 5]

            if resources[3] == 0: resources[3] = [50, 50, 0]
            else: resources[3] = [250*resources[3], 250*resources[3], 0]

            resources[4] = [resources[4], 0]

            if resources[5] < 7: resources[5] = [200 + 200*resources[5], 200 + 200*resources[5], 100]
            else: resources[5] = [1700 + 300*(resources[5] - 7), 1700 + 300*(resources[5] - 7), 100]

            lista[4] = resources
            
            self.AreaList.append(lista)

        f.close()
        return self.AreaList
        
    def InitializeTroopList(self, screen):
        self.TroopList = []
        
        index = 0
        for area in self.AreaList:
            temp = [screen]
            if area[5] != "o":
                temp.append(index)
                index += 1
                temp.append(area[5]+"_"+str(index))
                temp.append(area[5])
                temp.append(area[8])
                temp.append([10, 0, 0, 0, 0, 0, 0, 0])
                temp.append(70)
                self.TroopList.append(temp)
                
        return self.TroopList

    def InitializePlayerList(self, screen, NumPlayers):
        self.PlayerList = []
        for index in range(int(NumPlayers)):
            temp = [screen]
            temp2 = []
            temp.append(index)
            temp.append("p"+str(index+1))
            for area in self.AreaList:
                if area[5] == temp[2]:
                    temp2.append(area[8])
            temp.append(temp2)
            temp.append([0, 0, 0, 0, 0, 0])
            temp.append(0)
            total_pop = 0
            for area in temp2:
                total_pop += self.AreaList[area][3]
            
            temp.append(total_pop)
            temp2 = []
            for troop in self.TroopList:
                if troop[3] == temp[2]:
                    temp2.append(troop[1])
            temp.append(temp2)
            self.PlayerList.append(temp)

        temp = []
        summ = 0
        temp2 = []
        for area in self.AreaList:
            if area[5] == "c":
                temp.append(area[8])
                summ += area[3]
        for troop in self.TroopList:
                if troop[3] == "c":
                    temp2.append(troop[1])
        computer = [screen, NumPlayers, "c", temp, [0, 0, 0, 0, 0, 0], 0, summ, temp2]
        self.PlayerList.append(computer)

        return self.PlayerList

    def DistributeAreas(self, players, player, cap):
        if players <= 3:
            total = 0
            index_dict = {}
            while 1:
                random.seed(datetime.datetime.now())
                index =  random.randint(0,70)
                area = self.AreaList[index]
                pop = area[3]
                p = area[5]
                if pop < cap and p == "c": break
                
            self.AreaList[index][5] = "p"+str(player)
            total += self.AreaList[index][3]
            
            if total >= cap*(0.8): return 1
            else:
                if type(area[7][-1]) == list: neighbors = area[7][:-1]
                if type(area[7][-1]) == int: neighbors = area[7]
                for index in neighbors:
                    index_dict.update({str(index):index})
                    
                    if self.AreaList[index][3] + total <= cap and self.AreaList[index][5] == "c":
                        self.AreaList[index][5] = "p"+str(player)
                        total += self.AreaList[index][3]
                        
                        if type(self.AreaList[index][7][-1]) == list: neighbors1 = self.AreaList[index][7][:-1]
                        if type(self.AreaList[index][7][-1]) == int: neighbors1 = self.AreaList[index][7]
                        for index1 in neighbors1:
                            index_dict.update({str(index1):index1})
                        if total >= cap*0.8: return  1
                    else: pass
        
            if total < cap*0.8:
                for index in index_dict.keys():
                    index = int(index)
                    if self.AreaList[index][3] + total <= cap and self.AreaList[index][5] == "c":
                        self.AreaList[index][5] = "p"+str(player)
                        total += self.AreaList[index][3]
                        if total >= cap*0.8: return 1
                    else: pass


            for area in self.AreaList:
                if area[5] == "p"+str(player):
                    self.AreaList[self.AreaList.index(area)][5] = "c"
            return 0

        if players > 3:
            total = 0
            index_dict = {}
            while 1:
                random.seed(datetime.datetime.now())
                index =  random.randint(0,70)
                area = self.AreaList[index]
                pop = area[3]
                p = area[5]
                if pop < cap and pop >= cap*(2/3) and p == "c":
                    self.AreaList[index][5] = "p"+str(player)
                    return 1

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
        
    def DrawMap(self, screen, player, year, clock):
        
        self.Clock = clock
        time = pygame.time.Clock()
        self.player = player
        if player == self.NumPlayers: playername = "c"
        else:
            playername = "p"+str(player + 1)
        
        self.pause = False
        self.background = pygame.image.load("Colored Map, black sea.bmp")
        self.background = pygame.transform.scale(self.background, (int(self.w/1.05), int(self.h/1.05)))

        self.verylargefont = pygame.font.SysFont("Times", int(50*self.ratiow))
        self.largefont = pygame.font.SysFont("Times", int(40*self.ratiow))
        self.mediumfont = pygame.font.SysFont("Times", int(25*self.ratiow))
        
        self.areadotlist = []
        self.troopdotlist = []
        
        x = 0
        for i in range(len(self.AreaList)):
            self.areadotlist.append(OBJ.Area(self.AreaList[x]))
            x += 1

        x = 0
        for i in range(len(self.TroopList)):
            self.troopdotlist.append(OBJ.Troop(self.TroopList[x], self.AreaList[self.TroopList[x][4]][2]))
            x += 1

        while 1:
            dt = time.tick()
            if not self.pause:
                self.Clock -= dt/1000
                if self.Clock < 0:
                    return
            
            screen.blit(self.background, [0,0])
            for area in self.areadotlist:
                area.draw_area(screen)

            for troop in self.troopdotlist:
                troop.draw_troop(screen)

            self.current_player = OBJ.Player(self.PlayerList[player], self.pause)
            yearlabel = self.mediumfont.render("Year: "+str(year), 1, (255, 255, 255))
            screen.blit(yearlabel, [int(10*self.ratiow), int(10*self.ratioh)])

            mouse_pos = pygame.mouse.get_pos()
            
            for i in range(len(self.AreaList)):
                if self.areadotlist[i].button.collidepoint(mouse_pos):
                    self.areadotlist[i].hover_display(screen, self.areadotlist[i].rect)

            for i in range(len(self.TroopList)):
                if self.troopdotlist[i].button.collidepoint(mouse_pos):
                    self.troopdotlist[i].hover_display(screen)

            clock_ = str(int(self.Clock/60))+":"+str(int(self.Clock%60))
            if self.Clock%60 < 10: clock_ = str(int(self.Clock/60))+":0"+str(int(self.Clock%60))
            
            clock_label = self.largefont.render(clock_, 1, (255, 255, 255))
            screen.blit(clock_label, (int(1680*self.ratiow), int(10*self.ratioh)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause == False:
                        for i in range(len(self.AreaList)):
                            if self.areadotlist[i].button.collidepoint(mouse_pos):
                                self.WriteInfo()
                                if self.AreaList[i][5] == playername: currentplayer = True
                                else: currentplayer = False
                                self.activescene = AREA.AreaScene(self.screen, self.AreaList[i], self.Clock, self.NumPlayers, year, currentplayer, self.player)
                        for i in range(len(self.TroopList)):
                            if self.troopdotlist[i].button.collidepoint(mouse_pos):
                                    #Create Troop_display class
                                pass

                    if self.current_player.button1.collidepoint(mouse_pos):
                        return
                        
                    if self.current_player.button2.collidepoint(mouse_pos):
                        pass
                        #Make Save_game function
                    
                    if self.current_player.button3.collidepoint(mouse_pos):
                        temp = self.pause
                        if temp == False: self.pause = True
                        if temp == True: self.pause = False
                        
            pygame.display.flip()
        return

    def UpdateStatistics(self, player):
        total = 0
        old_food = self.PlayerList[player][4][5]
        food = self.UpdateFood(player)
        food_production = food - old_food
        for index in range(len(self.AreaList)):
            if self.AreaList[index][5] == self.PlayerList[player][2]:
                self.AreaList[index][3] = self.UpdatePopulation(self.AreaList[index][3], self.AreaList[index][6], self.AreaList[index][8], self.AreaList[index][11])
                total += self.AreaList[index][3]
        self.PlayerList[player][6] = total
        food_needs = int(total*10)
        if food_production != 0:
            food_remains = (food_production - food_needs)/food_production
        else: food_remains = -100
        if food >= food_needs:
            food = food - food_needs
            portion = 0
        else:
            dead = (food_needs - food)/17
            food = 0
            portion = dead/total
        self.PlayerList[player][4][5] = food
        self.UpdateMoral(player, portion)
        newtotal = 0
        #Make function CalculateDeaths(self)
        for index in self.PlayerList[player][3]:
            self.AreaList[index][3] = round(self.AreaList[index][3] - portion*self.AreaList[index][3], 2)
            newtotal += self.AreaList[index][3]
        self.PlayerList[player][6] = round(newtotal, 2)
        self.UpdateMetal(player)
        self.UpdateTimber(player)
        self.UpdateFossilFuels(player, 2)
        self.UpdateUranium(player, 3)
        self.UpdateIncome(player, food_remains)
        self.UpdateCoins(player)
        self.UpdateInfantry(player)
        
    def UpdatePopulation(self, old_pop, moral, basic_gdp, buildings):
        growth = old_pop*(moral - 50)/100*(1/16)
        if growth > 0 and buildings[0] == 1: growth = 1.5*growth
        new_pop = old_pop + growth
        return round(new_pop, 2)

    def UpdateFood(self, player):
        food =  self.PlayerList[player][4][5]
        for index in (self.PlayerList[player][3]):
            buildings = self.AreaList[index][11]
            temp = self.AreaList[index][4][5][0]*self.AreaList[index][4][5][2]*(1/500)*(math.sin(3.14/200*self.AreaList[index][6]) + 0.24)
            bonus = temp*0.02*buildings[1] + temp*0.02*buildings[2] + temp*0.02*buildings[3]
            food += int(temp + bonus)
            self.AreaList[index][4][5][0] = self.AreaList[index][4][5][0] - int(temp) + self.AreaList[index][4][5][1]/5
        self.PlayerList[player][4][5] = food
        return food

    def UpdateMetal(self, player):
        metal = self.PlayerList[player][4][0]
        for index in (self.PlayerList[player][3]):
            buildings = self.AreaList[index][11]
            if self.AreaList[index][4][0][0]*2 >= self.AreaList[index][4][0][1]: temp = (self.AreaList[index][6]/100)*self.AreaList[index][4][0][1]*self.AreaList[index][4][0][2]/1000
            else: temp = (2/5)*((self.AreaList[index][4][0][0]**2)/self.AreaList[index][4][0][1])*(self.AreaList[index][6]/100)*(self.AreaList[index][4][0][2]/100)
            self.AreaList[index][4][0][0] = self.AreaList[index][4][0][0] - int(temp)
            bonus = temp*0.02*buildings[1] + temp*0.02*buildings[2] + temp*0.02*buildings[3]
            if temp < 1:
                pass
            else:
                metal += int(temp + bonus)   
        self.PlayerList[player][4][0] = metal

    def UpdateTimber(self, player):
        timber = self.PlayerList[player][4][1]
        for index in (self.PlayerList[player][3]):
            buildings = self.AreaList[index][11]
            temp = self.AreaList[index][4][1][0]*self.AreaList[index][4][1][2]*(1/500)*(math.sin(3.14/200*self.AreaList[index][6]) + 0.24)
            bonus = temp*0.02*buildings[1] + temp*0.02*buildings[2] + temp*0.02*buildings[3]
            timber += int(temp + bonus)
            self.AreaList[index][4][1][0] = self.AreaList[index][4][1][0] - int(temp) + self.AreaList[index][4][1][1]/5
        self.PlayerList[player][4][1] = timber

    def UpdateFossilFuels(self, player, mine = 2):
        mined = self.PlayerList[player][4][mine]
        for index in (self.PlayerList[player][3]):
            buildings = self.AreaList[index][11]
            if self.AreaList[index][4][mine][0]*2 >= self.AreaList[index][4][mine][1]: temp = (self.AreaList[index][6]/100)*self.AreaList[index][4][mine][1]*self.AreaList[index][4][mine][2]/1000
            else: temp = (2/5)*((self.AreaList[index][4][mine][0]**2)/self.AreaList[index][4][mine][1])*(self.AreaList[index][6]/100)*(self.AreaList[index][4][mine][2]/100)
            bonus = temp*0.02*buildings[1] + temp*0.02*buildings[2] + temp*0.02*buildings[3]
            if temp + bonus < 1:
                pass
            else:
                mined += int(temp + bonus)
                self.AreaList[index][4][mine][0] = self.AreaList[index][4][mine][0] - int(temp)
        self.PlayerList[player][4][mine] = mined

    def UpdateUranium(self, player, mine = 3):
        mined = self.PlayerList[player][4][mine]
        for index in (self.PlayerList[player][3]):
            if self.AreaList[index][11][1] >= 1 and self.AreaList[index][11][6] >= 1:
                buildings = self.AreaList[index][11]
                if self.AreaList[index][4][mine][0]*2 >= self.AreaList[index][4][mine][1]: temp = (self.AreaList[index][6]/100)*self.AreaList[index][4][mine][1]*self.AreaList[index][4][mine][2]/1000
                else: temp = (2/5)*((self.AreaList[index][4][mine][0]**2)/self.AreaList[index][4][mine][1])*(self.AreaList[index][6]/100)*(self.AreaList[index][4][mine][2]/100)
                bonus = temp*0.02*buildings[1] + temp*0.02*buildings[2] + temp*0.02*buildings[3]
                if temp + bonus < 1:
                    pass
                else:
                    mined += int(temp + bonus)
                    self.AreaList[index][4][mine][0] = self.AreaList[index][4][mine][0] - int(temp)
        self.PlayerList[player][4][mine] = mined

    def UpdateCoins(self, player):
        coins = self.PlayerList[player][5]
        for index in (self.PlayerList[player][3]):
            coins += int(self.AreaList[index][10]/100*self.AreaList[index][9]*self.AreaList[index][3]*1000000)
        self.PlayerList[player][5] = coins

    def UpdateInfantry(self, player):
        for troop in (self.PlayerList[player][7]):
            self.TroopList[troop][5][0] += int(math.log(self.AreaList[self.TroopList[troop][4]][3] + 3)*self.AreaList[self.TroopList[troop][4]][6]/100)

    def UpdateIncome(self, player, food_remains):
        for area in (self.PlayerList[player][3]):
            old = income = self.AreaList[area][9]
            buildings = self.AreaList[area][11]
            production = 0
            res = self.AreaList[area][4]
            production += res[0][0]/18000
            production += res[1][0]/1200
            production += res[2][0]/6000
            production += res[3][0]/150
            production += res[4][0]/3
            production += res[5][0]/1380
            income += income*production/(200*math.log(income/1000 + 2))
            if income < 100: income = 100
            growth = income - old
            income += income*food_remains/(20*math.log(income/1000 + 1.4))
            if income < 100: income = 100
            income += income*(self.AreaList[area][6] - 70)/(1000*math.log(income/1000 + 1.4))
            if income < 100: income = 100
            income += income*(30 - self.AreaList[area][10])/(300)
            if income < 100: income = 100
            bonus = 0
            if buildings[0] == 1: bonus = 30
            bonus += buildings[0]*30 + buildings[1]*5 + buildings[2]*7 + buildings[3]*5 + buildings[7]*5
            income += growth*bonus/100
            self.AreaList[area][9] = income

    def UpdateMoral(self, player, portion):
        for area in self.PlayerList[player][3]:
            moral = self.AreaList[area][6]
            lowest_moral = 10
            if self.AreaList[area][11][0] == 1: lowest_moral = 35
            else: lowest_moral += 4*self.AreaList[area][11][5]
            if portion:
                moral = moral - portion*100
            elif portion == 0:
                moral += 2
            if self.AreaList[area][11][0] == 1:
                moral += 2
                for neib in self.AreaList[area][7]:
                    if neib in self.PlayerList[player][3]:
                        self.AreaList[neib][6] += 1
            moral += self.AreaList[area][11][4]*0.2
            moral -= self.AreaList[area][10]/33
            if moral < lowest_moral: moral = lowest_moral
            if moral > 100: moral = 100
            self.AreaList[area][6] = moral
            
            
