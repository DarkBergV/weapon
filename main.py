import pygame
import sys
from sprites import Body, Player, Enemy
from tilemap import Tilemap
from utils import load_image, load_images, Animation


WINDTH = 640

LENGTH = 480

RENDER_SCALE = 2.0


COYOTE_JUMP_EVENT = pygame.USEREVENT + 1
ATTACK_EVENT = pygame.USEREVENT + 2




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
       
        self.tilemap = Tilemap(self, 64)
        self.scene = []
        self.assets = {'ground/ground': load_images('ground'),
                       'player/ceiling': Animation(load_images('player/ceiling')),
                       'player/attack':Animation(load_images('player/attack')),
                       'player/iddle':Animation(load_images('player/iddle')),
                       'player/run':Animation(load_images('player/run')),
                       'player/fall_attack':Animation(load_images('player/fall_attack'))}
        
        self.enemy = Enemy(self,[50,50], [46,46], [15,20,70], "enemy")
        self.enemies = []
        self.load_level()

        self.player = Player(self, [0,0], [46,46], (255,0,0), 'player')
    def load_level(self):
        self.tilemap.load('map.json')
        self.enemies.append(self.enemy)
        for ground in self.tilemap.extract([('ground/ground', 0)], keep = True):
            self.scene.append(pygame.Rect(ground['pos'][0], ground['pos'][1],64,64))


    def run(self):
        while self.running:
            
            self.display_screen.fill((100,25,50))
            self.tilemap.render(self.display_screen, self.scroll)
            self.scroll[0] += (self.player.rect().centerx - self.display_screen.get_width() / 2 - self.scroll[0]) 
            self.scroll[1] += (self.player.rect().centery - self.display_screen.get_height() / 2 - self.scroll[1])


            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == COYOTE_JUMP_EVENT:
                   
                    self.player.was_on_floor = False
                    self.player.jumps -=1
                    pygame.time.set_timer(COYOTE_JUMP_EVENT,0)

                if event.type == ATTACK_EVENT:
                    self.player.is_attacking = False

                

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.attack(self.display_screen, self.scroll)
                        
                       
                        
                       
              

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movement[0] = True
                        self.movement[1] = False
                        self.player.velocity[0] = min(5, self.player.velocity[0] + 1)
                    if event.key == pygame.K_a:
                        self.movement[0] = False
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
            self.enemy.update(self.tilemap, [0,0], [0,0])
            self.enemy.render(self.display_screen, render_scroll)


            self.screen.blit(pygame.transform.scale(self.display_screen, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
g = Main()

while g.running:
    g.run()

pygame.quit()
sys.exit()