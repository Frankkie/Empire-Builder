import ctypes, pygame, sys, os
from pygame import font
import MAIN1 as MAIN
import GENERAL as GEN


class MenuScene():
    def __init__(self, screen):
        self.screen = screen
        self.black = (0, 0, 0)
        self.grey = (40, 40, 40)
        self.white = (255, 255, 255)
        screen.fill(self.grey)
        metrics = GEN.screen_metrics()
        self.w = metrics[0]
        self.h = metrics[1]
        self.ratiow = metrics[2]
        self.ratioh = metrics[3]
        background1 = pygame.image.load("half1.png")
        background1 = pygame.transform.scale(background1, (int(self.w/2 - 300*self.ratiow), self.h))
        screen.blit(background1, [0,0])
        background2 = pygame.image.load("half2.png")
        background2 = pygame.transform.scale(background2, (int(self.w/2 - 300*self.ratiow), self.h))
        screen.blit(background2, [int(self.w/2 + 300*self.ratiow),0])
        
        self.NumPlayers = 1
        self.largefont = pygame.font.SysFont("times", int(75*self.ratiow))
        self.medfont = pygame.font.SysFont("times", int(40*self.ratiow))
        self.smallfont = pygame.font.SysFont("times", int(20*self.ratiow))
        self.title = self.largefont.render("Empire Builder 0.3", 1, self.white)
        self.labelselect = self.medfont.render("Select number of players:  ", 1, self.white)
        screen.blit(self.title, (int(self.w/2 - 285*self.ratiow), int(80*self.ratioh)))
        screen.blit(self.labelselect, (int(self.w/2 - 240*self.ratiow), int(300*self.ratioh)))
        self.button = pygame.Rect((int(self.w/2 + 200*self.ratiow), int(305*self.ratioh), int(50*self.ratiow), int(40*self.ratioh)))
        self.startbutton = pygame.Rect((int(self.w/2 - 150*self.ratiow), int(440*self.ratioh), int(300*self.ratiow), int(100*self.ratioh)))
        self.loadbutton = pygame.Rect((int(self.w/2 - 150*self.ratiow), int(640*self.ratioh), int(300*self.ratiow), int(100*self.ratioh)))
                
        while 1:
            self.DrawButton((int(self.w/2 + 200*self.ratiow), int(305*self.ratioh), int(50*self.ratiow), int(40*self.ratioh)), "^", (int(self.w/2 + 215*self.ratiow), int(310*self.ratioh)))
            self.DrawButton((int(self.w/2 - 150*self.ratiow), int(440*self.ratioh), int(300*self.ratiow), int(100*self.ratioh)), "Start Game", (int(self.w/2 - 90*self.ratiow), int(465*self.ratioh)))
            self.DrawButton((int(self.w/2 - 150*self.ratiow), int(640*self.ratioh), int(300*self.ratiow), int(100*self.ratioh)), "Load Game", (int(self.w/2 - 90*self.ratiow), int(665*self.ratioh)))
            self.labelnum = self.medfont.render(str(self.NumPlayers), 1, self.white)
            screen.blit(self.labelnum, (int(self.w/2 + 170*self.ratiow), int(300*self.ratioh)))
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
                        screen.fill(self.grey, (int(self.w/2 + 170*self.ratiow), int(300*self.ratioh), int(30*self.ratiow), int(50*self.ratioh)))
                        self.NumPlayers += 1
                        self.NumPlayers = self.NumPlayers%6
                        if self.NumPlayers == 0:
                            self.NumPlayers = 6
                    if self.startbutton.collidepoint(mouse_pos):
                        self.SwitchToScene(MAIN.MainScene(screen, self.NumPlayers, "MenuScene", 180.9, 0))
            

            pygame.display.flip()

    def SwitchToScene(self, scene):
        active_scene = scenes[scene]

    def DrawButton(self, rect, text, textloc):
        label = self.medfont.render(text, 1, self.white)
        self.screen.fill(self.black, rect)
        self.screen.blit(label, textloc)
