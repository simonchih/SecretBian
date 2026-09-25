import threading
import pygame
import copy

b_loc = [(298, 275), (399, 275), (500, 275), (298, 351), (399, 351)]
g_loc = [(800, 275), (901, 275), (1002, 275), (800, 351), (901, 351), (1002, 351)]
        
class mythread (threading.Thread):
    def __init__(self, threadID, surface, b_img_name, g_img_name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.surface = surface
        self.b_img = pygame.image.load(b_img_name).convert_alpha()
        self.g_img = pygame.image.load(g_img_name).convert_alpha()
        self.img_alpha = 0
        #party, 0:blue, 1:green, -1: ini
        self.party = -1
        self.index = 0
    
    def run(self):
        global b_loc, g_loc
        
        if -1 == self.party:
            return
        
        # if party == blue
        if 0 == self.party:
            new_policy_img = self.b_img
            loc = b_loc[self.index]
        # else party == green
        else:
            new_policy_img = self.g_img
            loc = g_loc[self.index]
            
        if self.img_alpha < 255:
            self.img_alpha = min(255, self.img_alpha + 9)
            new_policy_img.set_alpha(self.img_alpha)
            self.surface.blit(new_policy_img, loc)