import pygame, sys, os, random, datetime, math
from pygame import font

class MenuScene():
    def __init__(self, screen):
        self.screen = screen
        self.black = (0, 0, 0)
        self.grey = (40, 40, 40)
        self.white = (255, 255, 255)
        screen.fill(self.grey)
        infoObject = pygame.display.Info()
        self.w = int(infoObject.current_w)
        self.h = int(infoObject.current_h)
        background1 = pygame.image.load("half1.png")
        background1 = pygame.transform.scale(background1, (int(self.w/2 - 300), self.h))
        screen.blit(background1, [0,0])
        background2 = pygame.image.load("half2.png")
        background2 = pygame.transform.scale(background2, (int(self.w/2 - 300), self.h))
        screen.blit(background2, [int(self.w/2 + 300),0])
        
        self.NumPlayers = 1
        self.largefont = pygame.font.SysFont("times", 75)
        self.medfont = pygame.font.SysFont("times", 40)
        self.smallfont = pygame.font.SysFont("times", 20)
        self.title = self.largefont.render("Empire Builder 0.2", 1, self.white)
        self.labelselect = self.medfont.render("Select number of players:  ", 1, self.white)
        screen.blit(self.title, (self.w/2 - 285, 80))
        screen.blit(self.labelselect, (self.w/2 - 240, 300))
        self.button = pygame.Rect((self.w/2 + 200, 305, 50, 40))
        self.startbutton = pygame.Rect((self.w/2 - 150, 440, 300, 100))
        self.loadbutton = pygame.Rect((self.w/2 - 150, 640, 300, 100))
                
        while 1:
            self.DrawButton((self.w/2 + 200, 305, 50, 40), "^", (self.w/2 + 215, 310))
            self.DrawButton((self.w/2 - 150, 440, 300, 100), "Start Game", (self.w/2 - 90, 465))
            self.DrawButton((self.w/2 - 150, 640, 300, 100), "Load Game", (self.w/2 - 90, 665))
            self.labelnum = self.medfont.render(str(self.NumPlayers), 1, self.white)
            screen.blit(self.labelnum, (self.w/2 + 170, 300))
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
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button.collidepoint(mouse_pos):
                        screen.fill(self.grey, (self.w/2 + 170, 300, 30, 50))
                        self.NumPlayers += 1
                        self.NumPlayers = self.NumPlayers%6
                        if self.NumPlayers == 0:
                            self.NumPlayers = 6
                    if self.startbutton.collidepoint(mouse_pos):
                        self.SwitchToScene(MainScene(screen, self.NumPlayers, "MenuScene", 180.9, 0))
            

            pygame.display.flip()

    def SwitchToScene(self, scene):
        active_scene = scenes[scene]

    def DrawButton(self, rect, text, textloc):
        label = self.medfont.render(text, 1, self.white)
        self.screen.fill(self.black, rect)
        self.screen.blit(label, textloc)

class MainScene():
    def __init__(self, screen, NumPlayers, previous, clock, year):
        self.NumPlayers = NumPlayers
        self.screen = screen
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
            temp.append(int(line[1]))
            temp.append(int(line[2]))
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
        if player == self.NumPlayers: playername = "c"
        else:
            playername = "p"+str(player + 1)
        
        self.pause = False
        infoObject = pygame.display.Info()
        self.w = int(infoObject.current_w)
        self.h = int(infoObject.current_h)
        self.background = pygame.image.load("Colored Map, black sea.bmp")
        self.background = pygame.transform.scale(self.background, (int(self.w/1.05), int(self.h/1.05)))

        self.verylargefont = pygame.font.SysFont("Times", 50)
        self.largefont = pygame.font.SysFont("Times", 40)
        self.mediumfont = pygame.font.SysFont("Times", 25)
        
        self.areadotlist = []
        self.troopdotlist = []
        
        x = 0
        for i in range(len(self.AreaList)):
            self.areadotlist.append(Area(self.AreaList[x]))
            x += 1

        x = 0
        for i in range(len(self.TroopList)):
            self.troopdotlist.append(Troop(self.TroopList[x], self.AreaList[self.TroopList[x][4]][2]))
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

            self.current_player = Player(self.PlayerList[player], self.pause)
            yearlabel = self.mediumfont.render("Year: "+str(year), 1, (255, 255, 255))
            screen.blit(yearlabel, [10, 10])

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
            screen.blit(clock_label, (1680, 10))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause == False:
                        for i in range(len(self.AreaList)):
                            if self.areadotlist[i].button.collidepoint(mouse_pos):
                                self.WriteInfo()
                                if self.AreaList[i][5] == playername: currentplayer = True
                                else: currentplayer = False
                                self.activescene = AreaScene(self.screen, self.AreaList[i], self.Clock, self.NumPlayers, year, currentplayer)
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
                        
            #pygame.image.save(screen, "Final Map.bmp")
            pygame.display.flip()
        return

    def UpdateStatistics(self, player):
        total = 0
        food = self.UpdateFood(player)
        for index in range(len(self.AreaList)):
            if self.AreaList[index][5] == self.PlayerList[player][2]:
                self.AreaList[index][3] = self.UpdatePopulation(self.AreaList[index][3], self.AreaList[index][6], self.AreaList[index][8])
                total += self.AreaList[index][3]
        self.PlayerList[player][6] = total
        food_needs = int(total*10)
        if food >= food_needs:
            food = food - food_needs
        else:
            dead = (food_needs - food)/17
            food = 0
            portion = dead/total
        self.PlayerList[player][4][5] = food
        try:
            for index in self.PlayerList[player][3]:
                self.AreaList[index][3] = round(self.AreaList[index][3] - portion*self.AreaList[index][3], 2)
                self.AreaList[index][6] = self.AreaList[index][6] - portion*100
                
                if self.AreaList[index][6] < 10: self.AreaList[index][6] = 10

        except UnboundLocalError:
            for index in self.PlayerList[player][3]:
                self.AreaList[index][6] += 3
                if self.AreaList[index][6] > 100: self.AreaList[index][6] = 100
        newtotal = 0
       
        for index in self.PlayerList[player][3]:
            newtotal += self.AreaList[index][3]
         
        self.PlayerList[player][6] = round(newtotal, 2)
        
        self.UpdateMetal(player)
        self.UpdateTimber(player)
        self.UpdateFossilFuels(player, 2)
        self.UpdateUranium(player, 3)
        self.UpdateCoins(player)
        self.UpdateInfantry(player)
        

    def UpdatePopulation(self, old_pop, moral, basic_gdp):
        new_pop = old_pop + old_pop*(moral - 50)/100*(1/16)
        return round(new_pop, 2)

    def UpdateFood(self, player):
        food =  self.PlayerList[player][4][5]
        for index in (self.PlayerList[player][3]):
            temp = self.AreaList[index][4][5][0]*self.AreaList[index][4][5][2]*(1/500)*(math.sin(3.14/200*self.AreaList[index][6]) + 0.24)
            food += int(temp)
            self.AreaList[index][4][5][0] = self.AreaList[index][4][5][0] - int(temp) + self.AreaList[index][4][5][1]/5
        self.PlayerList[player][4][5] = food
        return food

    def UpdateMetal(self, player):
        metal = self.PlayerList[player][4][0]
        for index in (self.PlayerList[player][3]):
            if self.AreaList[index][4][0][0]*2 >= self.AreaList[index][4][0][1]: temp = (self.AreaList[index][6]/100)*self.AreaList[index][4][0][1]*self.AreaList[index][4][0][2]/1000
            else: temp = (2/5)*((self.AreaList[index][4][0][0]**2)/self.AreaList[index][4][0][1])*(self.AreaList[index][6]/100)*(self.AreaList[index][4][0][2]/100)
            if temp < 1:
                pass
            else:
                metal += int(temp)
                self.AreaList[index][4][0][0] = self.AreaList[index][4][0][0] - int(temp)
        self.PlayerList[player][4][0] = metal

    def UpdateTimber(self, player):
        timber = self.PlayerList[player][4][1]
        for index in (self.PlayerList[player][3]):
            temp = self.AreaList[index][4][1][0]*self.AreaList[index][4][1][2]*(1/500)*(math.sin(3.14/200*self.AreaList[index][6]) + 0.24)
            timber += int(temp)
            self.AreaList[index][4][1][0] = self.AreaList[index][4][1][0] - int(temp) + self.AreaList[index][4][1][1]/5
        self.PlayerList[player][4][1] = timber

    def UpdateFossilFuels(self, player, mine = 2):
        mined = self.PlayerList[player][4][mine]
        for index in (self.PlayerList[player][3]):
            if self.AreaList[index][4][mine][0]*2 >= self.AreaList[index][4][mine][1]: temp = (self.AreaList[index][6]/100)*self.AreaList[index][4][mine][1]*self.AreaList[index][4][mine][2]/1000
            else: temp = (2/5)*((self.AreaList[index][4][mine][0]**2)/self.AreaList[index][4][mine][1])*(self.AreaList[index][6]/100)*(self.AreaList[index][4][mine][2]/100)
            if temp < 1:
                pass
            else:
                mined += int(temp)
                self.AreaList[index][4][mine][0] = self.AreaList[index][4][mine][0] - int(temp)
        self.PlayerList[player][4][mine] = mined

    def UpdateUranium(self, player, mine = 3):
        mined = self.PlayerList[player][4][mine]
        for index in (self.PlayerList[player][3]):
            if self.AreaList[index][4][mine][0]*2 >= self.AreaList[index][4][mine][1]: temp = (self.AreaList[index][6]/100)*self.AreaList[index][4][mine][1]*self.AreaList[index][4][mine][2]/1000
            else: temp = (2/5)*((self.AreaList[index][4][mine][0]**2)/self.AreaList[index][4][mine][1])*(self.AreaList[index][6]/100)*(self.AreaList[index][4][mine][2]/100)
            if temp < 1:
                pass
            else:
                mined += int(temp)
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


class AreaScene():
    def __init__(self, screen, arealist, clock, numplayers, year, currentplayer):
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
        infoObject = pygame.display.Info()
        self.w = int(infoObject.current_w)
        self.h = int(infoObject.current_h)
        self.screen = screen
        self.hugefont = pygame.font.SysFont("Times", 80)
        self.verylargefont = pygame.font.SysFont("Times", 50)
        self.largefont = pygame.font.SysFont("Times", 40)
        self.medfont = pygame.font.SysFont("Times", 25)
        self.ButtonDict = {}
        self.BackToMain = pygame.Rect((1600, 20, 180, 50))
        
        self.bar = pygame.image.load("bar.png")
        self.bar = pygame.transform.scale(self.bar, (400, 10))
        self.point = pygame.image.load("point.png")
        self.point = pygame.transform.scale(self.point, (40, 40))
        self.playerdot = pygame.image.load(self.area[5]+".png")
        self.playerdot = pygame.transform.scale(self.playerdot, (50, 50))
        self.barlist = []
        
        self.taxesbar = Bar(self.screen, [50, 200], "Taxes", [60, 220], [0, 100], self.area[10])
        self.barlist.append(self.taxesbar)
        self.foodbar = Bar(self.screen, [50, 280], "Food", [60, 300], [0, 200], self.area[4][5][2])
        self.barlist.append(self.foodbar)
        self.metalbar = Bar(self.screen, [50, 360], "Metal", [60, 380], [0, 100], self.area[4][0][2])
        self.barlist.append(self.metalbar)
        self.timberbar = Bar(self.screen, [50, 440], "Timber", [60, 460], [0, 100], self.area[4][1][2])
        self.barlist.append(self.timberbar)
        self.fossilbar = Bar(self.screen, [50, 520], "Fossils", [60, 540], [0, 100], self.area[4][2][2])
        self.barlist.append(self.fossilbar)
        self.uraniumbar = Bar(self.screen, [50, 600], "Uranium", [60, 620], [0, 100], self.area[4][3][2])
        self.barlist.append(self.uraniumbar)
        self.renewbar = Bar(self.screen, [50, 680], "Renewables", [60, 700], [0, 100], self.area[4][4][1])
        self.barlist.append(self.renewbar)

        if self.area[11][0] == 0: capital = "- Not Capital"
        else: capital = "- Capital"

        self.labellist = [Label(self.area[1], self.hugefont, [int(self.w/2 - len(self.area[1])*19), 20]), Label("- Moral: "+str(round(self.area[6]))+"%", self.largefont, [660, 175]),
                          Label("- Population: "+str(round(self.area[3], 3))+" million people", self.largefont, [660, 225]), Label("- Per Capita Income:"+str(int(self.area[9]))+" coins", self.largefont, [660, 275]),
                          Label("- Resources", self.verylargefont, [660, 340]),
                          Label("- Food: "+str(int(self.area[4][5][0]))+"/"+str(self.area[4][5][1]), self.largefont, [660, 400]),
                          Label("- Metal: "+str(self.area[4][0][0])+"/"+str(self.area[4][0][1]), self.largefont, [660, 450]),
                          Label("- Timber: "+str(int(self.area[4][1][0]))+"/"+str(self.area[4][1][1]), self.largefont, [660, 500]),
                          Label("- Fossil Fuels: "+str(self.area[4][2][0])+"/"+str(self.area[4][2][1]), self.largefont, [660, 550]),
                          Label(" -Uranium: "+str(self.area[4][3][0])+"/"+str(self.area[4][3][1]), self.largefont, [660, 600]),
                          Label(" -Renewables: "+"| "+(self.area[4][4][0] + 1)*"+"+(6 - self.area[4][4][0])*" "+"|", self.largefont, [660, 650]),
                          Label(capital, self.largefont, [1360, 175])]
        
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
                active_scene = MainScene(self.screen, self.NumPlayers, "AreaScene", self.Clock, self.year)
            clock_ = str(int(self.Clock/60))+":"+str(int(self.Clock%60))
            if self.Clock%60 < 10: clock_ = str(int(self.Clock/60))+":0"+str(int(self.Clock%60))            
            clock_label = self.largefont.render(clock_, 1, (255, 255, 255))
            self.screen.blit(clock_label, (1820, 20))
            
            self.DrawButton((1600, 20, 180, 50), "Back to Map >>", [1610, 30])
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
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BackToMain.collidepoint(mouse_pos):
                        self.WriteInfo()
                        active_scene = MainScene(self.screen, self.NumPlayers, "AreaScene", self.Clock, self.year)
                    for bar in self.barlist:
                        if bar.pointrect.collidepoint(mouse_pos) and self.currentplayer:
                            temp = bar.drag
                            if temp == True: bar.drag = False
                            if temp == False: bar.drag = True
                    
            pygame.display.flip()
        
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

#=============================================================================================
#
#
#=============================================================================================

class Bar():
    def __init__(self, screen, pos, text, textpos, limits, num):
        self.screen = screen
        self.white = (255, 255, 255)
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
        self.label = self.medfont.render(self.text+": "+str(num)+"%", 1, self.white)
        self.screen.blit(self.label, self.textpos)
        
    def Drag(self, mouse_pos):
        point_pos = mouse_pos[0]
        if mouse_pos[0] < self.pos[0]: point_pos = self.pos[0]
        if mouse_pos[0] > self.pos[0] + self.barsize : point_pos = self.pos[0] + self.barsize
        num = int((point_pos - self.pos[0])/(self.barsize/self.range))
        self.pointrect = pygame.Rect((point_pos, self.pos[1] - 15, 40, 40))
        return num

class Label():
    def __init__(self, text, font, pos):
        self.pos = pos
        self.label = font.render(text, 1, (255, 255, 255))
    def DrawLabel(self, screen):
        screen.blit(self.label, self.pos)
    
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
        self.ratio = 270/size
        rect = [self.location[0] + 20, self.location[1] + 20, size, int(size*self.ratio)]
        self.rect = rect

        if rect[0] + rect[2] > w - 100: rect[0] = self.location[0] - 20 - size
        if rect[1] + rect[3] > h - 100: rect[1] = self.location[1] - 20 - int(size*self.ratio)
        
        if self.buildings[0]: capital = "***"
        else: capital = ""
        if self.country == "c": player = "Computer"
        if self.country[0] == "p": player = "Player "+self.country[1]
        if self.country == "o": player = "Unclaimed waters"
        
        self.LabelList = [Label(self.name+capital, self.myfont, (rect[0] + 10, rect[1] + 5)), Label(player, self.medfont, (rect[0] + 10, rect[1] + 38)),
                          Label("Population: "+str(self.population/1000000)[:5]+" million", self.mysmallfont, (rect[0] + 10, rect[1] + 74)),
                          Label("Moral: "+str(int(self.moral))+"%", self.mysmallfont, (rect[0] + 10, rect[1] + 96)),
                          Label("Food: "+str(int(self.resources[5][0])), self.mysmallfont, (rect[0] + 10, rect[1] + 118)),
                          Label("Metal: "+str(int(self.resources[0][0])), self.mysmallfont, (rect[0] + 10, rect[1] + 140)),
                          Label("Timber: "+str(int(self.resources[1][0])), self.mysmallfont, (rect[0] + 10, rect[1] + 162)),
                          Label("Fossil fuels: "+str(int(self.resources[2][0])), self.mysmallfont, (rect[0] + 10, rect[1] + 184)),
                          Label("Uranium: "+str(int(self.resources[3][0])), self.mysmallfont, (rect[0] + 10, rect[1] + 206)),
                          Label("Renewables: "+(self.resources[4][0]+1)*"#", self.mysmallfont, (rect[0] + 10, rect[1] + 228))]

    def draw_area(self, screen):
        screen.blit(self.area_point, self.location)
        
    def hover_display(self, screen, rect):
        screen.fill([50, 50, 50, 50], tuple(rect))
        pygame.draw.rect(screen, [0, 0, 0, 0], tuple(rect), 3)

        for label in self.LabelList:
            label.DrawLabel(screen)

class Building():
    pass

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
                
def playgame():
    os.chdir(".\\InitGame")
    pygame.init()
    pygame.font.init()
    infoObject = pygame.display.Info()
    w = int(infoObject.current_w)
    h = int(infoObject.current_h)
    screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
    active_scene = MenuScene(screen)

playgame()
