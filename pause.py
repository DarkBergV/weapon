from random import choice, gammavariate
import pygame
import random
import sys



WINDTH = 640
LENGHT = 480

RENDER_SCALE = 2.0
CARD_SIZE = (160,280)

RESUME_BUTTON = {'pos':(350,20), 'size': (120, 60)}
EQUIP_BUTTONS = {'pos': (150,400), 'size':(180,60)}

class Pause(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.display = pygame.Surface(RESUME_BUTTON['size'])
        self.display_equip = pygame.Surface(RESUME_BUTTON['size'])
        self.font = pygame.font.Font(None, 25)
        self.color_button = (0,0,0)        
        self.color_font = (255,255,255)

        self.color_button_equip = (0,0,0)        
        self.color_font_equip = (255,255,255)

    def rect(self):
        return pygame.Rect(RESUME_BUTTON['pos'][0],300, RESUME_BUTTON['size'][0],RESUME_BUTTON['size'][1]).copy()
    
    def equip_rect(self):
        return pygame.Rect(EQUIP_BUTTONS['pos'][0],300, RESUME_BUTTON['size'][0],RESUME_BUTTON['size'][1]).copy()
    
    def render(self, surf, offset):
        self.display.fill(self.color_button)
        button = self.font.render('Resume', True,self.color_font)
        self.display.blit(button, (26,20))

        rect = self.rect()
        surf.blit(self.display, (rect[0]-offset[0],rect[1] - offset[1]))

        self.display_equip.fill(self.color_button_equip)
        button = self.font.render('Aspects', True, self.color_font_equip)
        self.display_equip.blit(button, (26,20))

        equip_rect = self.equip_rect()
        surf.blit(self.display_equip, (equip_rect[0]-offset[0], rect[1] - offset[1]))

    def update(self,click):
        rect = self.rect()
        equip_rect = self.equip_rect()
        self.color_button = (0,0,0)        
        self.color_font = (255,255,255)
        self.color_button_equip = (0,0,0)        
        self.color_font_equip = (255,255,255)


        if rect.collidepoint(pygame.mouse.get_pos()):
            self.color_button = (255,255,255)     
            self.color_font = (0,0,0) 

            if click:
                self.game.running = True
                self.game.pause_menu = False
                print('run')

        if equip_rect.collidepoint(pygame.mouse.get_pos()):

            self.color_button_equip = (255,255,255)   
            self.color_font_equip = (0,0,0) 

            if click:
                pass

        
        