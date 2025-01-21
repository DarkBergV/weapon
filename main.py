import pygame
import sys
from sprites import Body, Player
from tilemap import Tilemap
from utils import load_image, load_images, Animation


WINDTH = 640

LENGTH = 480

RENDER_SCALE = 2.0


COYOTE_JUMP_EVENT = pygame.USEREVENT + 1




class Main():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('weapon game')
        self.screen = pygame.display.set_mode((WINDTH, LENGTH))
        self.display_screen = pygame.surface.Surface((WINDTH // 2 , LENGTH // 2))
        self.movement = [0,0,0,0]
        self.scroll = [0,0]
        self.running = True
        self.clock = pygame.time.Clock()
       
        self.tilemap = Tilemap(self, 32)
        self.scene = []
        self.assets = {'ground/ground': load_images('ground'),
                       'player/attack':Animation(load_images('player/attack')),
                       'player/iddle':Animation(load_images('player/iddle')),
                       'player/run':Animation(load_images('player/run'))}
        self.load_level()

        self.player = Player(self, [0,0], [32,32], (255,0,0), 'player')
    def load_level(self):
        self.tilemap.load('map.json')
        for ground in self.tilemap.extract([('ground/ground', 0)], keep = True):
            self.scene.append(pygame.Rect(ground['pos'][0], ground['pos'][1],32,32))


    def run(self):
        while self.running:
            
            self.display_screen.fill((255,255,255))
            self.tilemap.render(self.display_screen, self.scroll)
            self.scroll[0] += (self.player.rect().centerx - self.display_screen.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display_screen.get_height() / 2 - self.scroll[1]) / 30

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == COYOTE_JUMP_EVENT:
                    print('aaaaaaaaaaaaaaaaaaaaa')
                    self.player.was_on_floor = False
                    self.player.jumps -=1
                    pygame.time.set_timer(COYOTE_JUMP_EVENT,0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movement[0] = True
                        self.player.velocity[0] = min(5, self.player.velocity[0] + 1)
                    if event.key == pygame.K_a:
                        self.movement[1] = True
                        self.player.velocity[0] = min(5, self.player.velocity[0] + 1) * -1
                    if event.key == pygame.K_w:
                        
                        self.player.jump()
                    if event.key == pygame.K_s:
                        self.movement[2] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0] = False
                        self.player.velocity[0] = 0
                    if event.key == pygame.K_a:
                        self.movement[1] = False 
                        self.player.velocity[0] = 0
                    if event.key == pygame.K_w:
                        self.player.release_jump()
                    if event.key == pygame.K_s:
                        self.movement[2] = False


            self.player.update(self.tilemap,[self.movement[0] - self.movement[1], self.movement[2] - self.movement[3]])
            self.player.render(self.display_screen, render_scroll)


            self.screen.blit(pygame.transform.scale(self.display_screen, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
g = Main()

while g.running:
    g.run()

pygame.quit()
sys.exit()