
import pygame
import sys

from tilemap import Tilemap
from utils import load_image, load_images

WIN_WIDTH = 640
WIND_HEIGHT = 480
PATH_IMG = 'img/'
RENDER_SCALE = 2.0
class Editor:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('game editor')
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIND_HEIGHT))
        self.display = pygame.surface.Surface((WIN_WIDTH//2, WIND_HEIGHT//2))
        self.running = True
        self.movement = [0,0,0,0]
        self.scroll = [0,0]
        
        self.clock = pygame.time.Clock()

        self.assets = {'ground/ground': load_images('tiles/ground'),
                       'spawners': load_images('tiles/spawner')}

        self.tilemap = Tilemap(self, 32)
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        
        self.tile_list = list(self.assets)
        self.tile_group = 0 
        self.tile_variant = 0

        self.clicking = False

        self.right_clicking = False

        self.shift = False

        self.ongrind = True

        #enemies
        self.enemies = []

    def run(self):
        while self.running:
            self.display.fill((155,155,155))

            self.scroll[0] += (self.movement[0] - self.movement[1]) * 2
            self.scroll[1] += (self.movement[2] - self.movement[3]) * 2

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            self.tilemap.render(self.display, offset=render_scroll)
            
            
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
          
            current_tile_img.set_alpha(100)
            mpos = pygame.mouse.get_pos()

            mpos = ((mpos[0]/RENDER_SCALE , mpos[1]/RENDER_SCALE))
            
            tile_pos = (int(mpos[0] + self.scroll[0])//self.tilemap.tile_size,int(mpos[1] + self.scroll[1])//self.tilemap.tile_size)
            #tile_pos_wrong = (int(mpos[0] + self.scroll[0]//self.tilemap.tile_size),int(mpos[1] + self.scroll[1]//self.tilemap.tile_size))
            
            if self.ongrind:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0]  , tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))

            else:
                self.display.blit(current_tile_img, mpos)

            if self.clicking and self.ongrind:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {"type": self.tile_list[self.tile_group], "variant": self.tile_variant, "pos": tile_pos}
            

            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' +  str(tile_pos[1])

                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]

                
                for tile  in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    
                    tile_r = pygame.Rect(tile["pos"][0] - self.scroll[0], tile["pos"][1] - self.scroll[1],tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5,5))


         
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit

                keys = pygame.key.get_pressed()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        
                        self.clicking = True
                        if not self.ongrind:
                            self.tilemap.offgrid_tiles.append({"type": self.tile_list[self.tile_group], "variant": self.tile_variant, "pos": (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 2:
                        pass
                    if event.button == 3:
                        
                        self.right_clicking = True

                    if self.shift:
                        if event.button == 4:
                            
                            self.tile_variant = (self.tile_variant + 1 ) % len(self.assets[self.tile_list[self.tile_group]])
                            
                        if event.button == 5:
                            
                            self.tile_variant = (self.tile_variant - 1 ) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                           
                            self.tile_group = (self.tile_group + 1) % len(self.assets)  
                            
                        if event.button == 5:
                            self.tile_group = (self.tile_group - 1)% len(self.assets)
                            

            

                    

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False

                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.ongrind = not self.ongrind

                

                
                if keys[pygame.K_d]:
                    self.movement[0] = True
                elif keys[pygame.K_a]:
                    self.movement[1] = True
                
                elif keys[pygame.K_w]:
                    self.movement[3] = True

                elif keys[pygame.K_s]:
                    self.movement[2] = True

                elif keys[pygame.K_LSHIFT]:
                    self.shift = True
                elif keys[pygame.K_o]:
                    self.tilemap.save('map.json')

                

                


                else:
                    self.movement[0] = False
                    self.movement[1] = False
                    self.movement[2] = False
                    self.movement[3] = False
                    self.shift = False
                   


            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),[0,0])
            pygame.display.update()
            self.clock.tick(60)





e = Editor()

while e.running:
    e.run()


pygame.quit()
sys.exit()