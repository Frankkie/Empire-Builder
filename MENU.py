import ctypes, pygame, sys, os, random, datetime, math
from pygame import font
import MAIN1 as MAIN


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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
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
                        self.SwitchToScene(MAIN.MainScene(screen, self.NumPlayers, "MenuScene", 180.9, 0))
            

            pygame.display.flip()

    def SwitchToScene(self, scene):
        active_scene = scenes[scene]

    def DrawButton(self, rect, text, textloc):
        label = self.medfont.render(text, 1, self.white)
        self.screen.fill(self.black, rect)
        self.screen.blit(label, textloc)
