# This file was created by Carter Godinez

'''
New and Improved Video Game
Goals:
Use some elements of past game
insert some new elements not previously used
More interactive with more aspects than just surviving
'''

# content from kids can code: http://kidscancode.org/blog/
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
# import all settings
from settings import *
# import all sprites
from sprites import *
import math
import time

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')


class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
        self.start_time = pg.time.get_ticks()
    
    def new(self): 
        # create a group for all sprites
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)

        for p in PLATFORM_LIST:
            # instantiation of the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        # insert mobs into random spots on screen
        for m in range(0,10):
            # range of where mob can spawn and size of mobs
            m = Mob(randint(10, WIDTH-30), randint(0, math.floor(HEIGHT-50)), 20, 20, "moving")
            # add mobs onto screen
            self.all_sprites.add(m)
            self.all_mobs.add(m)
        self.run()
    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

        # this is what prevents the player from falling through the platform when falling down...
        if self.player.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5

                    
         # this prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.acc.y = 5
                self.player.vel.y = 0
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom

    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(WHITE)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        # count number of ticks 
        current_time = pg.time.get_ticks()
        # display time by dividing number of ticks by 1000
        self.draw_text("Time: " + str(current_time/1000), 22, BLACK, WIDTH/2, HEIGHT/10)
        # buffer - after drawing everything, flip display
        pg.display.flip()
    
    # set settings for text
    def draw_text(self, text, size, color, x, y):
        # font settings
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass

g = Game()
while g.running:
    g.new()


pg.quit()