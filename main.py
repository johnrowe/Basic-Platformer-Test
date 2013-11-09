"""
    My test for 2D platformer movement.
    Here we have collision detection, smooth accelerated movement,
    seperate world and window coordinates, and camera movement.
"""

import pygame
from pygame.locals import *
pygame.init()

import sys
import time

from lib import (entities, 
                camera, 
                draw, 
                level,
                hud)
 
class main():
    # Screen Constants
    FPS = 60
    FPS_limit = True
    WINDOWWIDTH = 800
    WINDOWHEIGHT = 600
    FLAGS = HWSURFACE|DOUBLEBUF
    showText = False
    
    def play_game(self):
        # Set up screen
        self.screen = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT), self.FLAGS)
        pygame.display.set_caption('2D Platforming Test')
        self.clock = pygame.time.Clock()
        
        # Set up objects
        self.currentLevel = level.Level("levels\\level_1.lvl")
        self.player = entities.Player(self.currentLevel, (4, 57, 60, 90))
        
        # original speed settings for 30 FPS
        if self.FPS == 30:
            self.player.maxSpeed = 16
            self.player.accel_amt = 3
            self.player.airaccel_amt = 2
            self.player.deaccel_amt = 10
            self.player.fallAccel = 4
            self.animation_speed = 0.015
            
        self.cameraObj = camera.Camera(self.player.rect, 
                                       self.WINDOWWIDTH, 
                                       self.WINDOWHEIGHT)
        self.OSD_text = hud.OSD()

        # Game loop
        while True:
            self.keys = self.collect_input()
            self.player.update(self.keys, self.currentLevel)
            self.cameraObj.update(self.player.cameraRect, self.currentLevel)
            self.OSD_text.update(self)
           
            draw.draw_level(self.screen, self.currentLevel, self.cameraObj)
            draw.draw_entities(self.screen, (self.player,), self.cameraObj)
            if self.showText:
                draw.draw_OSD(self.screen, self.OSD_text.text)

            pygame.display.update()
            self.clock.tick(self.FPS)
            
    def collect_input(self):
        for event in pygame.event.get():
            if event.type == QUIT or\
            (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_x:
                    self.showText = not self.showText
                # repurposed the 'z' key to frame limit to 30 fps
                if event.key == K_z:
                    if self.FPS > 30:
                        self.FPS = 30
                    else:
                        self.FPS = 60

        keys = pygame.key.get_pressed()
        return keys

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('main().play_game()')
    main().play_game()
